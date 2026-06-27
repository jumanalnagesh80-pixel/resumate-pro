"""Resume parser.

Best-effort extraction from an uploaded resume file (PDF, DOCX, TXT).
Returns a partial resume dict matching the shape produced by
``utils.helpers.empty_resume``. Recruiters' tools are notoriously messy, so
the parser is permissive: it locates section headings heuristically and
splits content on common delimiters.
"""

from __future__ import annotations

import io
import re
from typing import Optional

from data.skills_db import extract_skills
from utils.helpers import empty_resume


# ---------------------------------------------------------------------------
# Text extraction
# ---------------------------------------------------------------------------

def extract_text(file_bytes: bytes, filename: str) -> str:
    """Dispatch on filename extension; tolerate missing libraries."""
    name = (filename or "").lower()
    if name.endswith(".pdf"):
        return _from_pdf(file_bytes)
    if name.endswith(".docx"):
        return _from_docx(file_bytes)
    if name.endswith(".txt") or name.endswith(".md"):
        return file_bytes.decode("utf-8", errors="ignore")
    # Unknown: try as utf-8 text.
    return file_bytes.decode("utf-8", errors="ignore")


def _from_pdf(data: bytes) -> str:
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(io.BytesIO(data))
        chunks = []
        for page in reader.pages:
            try:
                chunks.append(page.extract_text() or "")
            except Exception:
                continue
        return "\n".join(chunks)
    except Exception as exc:
        return f"[Could not read PDF: {exc}]"


def _from_docx(data: bytes) -> str:
    try:
        import docx  # python-docx
        d = docx.Document(io.BytesIO(data))
        return "\n".join(p.text for p in d.paragraphs)
    except Exception as exc:
        return f"[Could not read DOCX: {exc}]"


# ---------------------------------------------------------------------------
# Section splitting
# ---------------------------------------------------------------------------

SECTION_ALIASES = {
    "summary":        ["summary", "professional summary", "profile", "about", "objective"],
    "experience":     ["experience", "work experience", "professional experience", "employment", "work history"],
    "education":      ["education", "academic background", "academics"],
    "skills":         ["skills", "technical skills", "core competencies", "technologies"],
    "projects":       ["projects", "personal projects", "selected projects"],
    "certifications": ["certifications", "certificates", "licenses"],
    "awards":         ["awards", "honors", "achievements"],
    "languages":      ["languages"],
}


def _classify_heading(line: str) -> Optional[str]:
    s = line.strip().rstrip(":").lower()
    if not s or len(s) > 40:
        return None
    for canonical, names in SECTION_ALIASES.items():
        if s in names:
            return canonical
    return None


def _split_sections(text: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {"_header": []}
    current = "_header"
    for raw in text.splitlines():
        line = raw.rstrip()
        kind = _classify_heading(line)
        if kind:
            current = kind
            sections.setdefault(current, [])
            continue
        sections.setdefault(current, []).append(line)
    return {k: "\n".join(v).strip() for k, v in sections.items()}


# ---------------------------------------------------------------------------
# Field-level extractors
# ---------------------------------------------------------------------------

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(\+?\d[\d\s().-]{7,}\d)")
LINKEDIN_RE = re.compile(r"(https?://)?(www\.)?linkedin\.com/in/[A-Za-z0-9_\-./]+", re.I)
GITHUB_RE = re.compile(r"(https?://)?(www\.)?github\.com/[A-Za-z0-9_\-./]+", re.I)
URL_RE = re.compile(r"https?://[^\s)]+", re.I)
YEAR_RANGE_RE = re.compile(
    r"(?P<start>(?:19|20)\d{2})\s*[-–to]+\s*(?P<end>(?:19|20)\d{2}|present|current)",
    re.I,
)


def _extract_personal(header_text: str, full_text: str) -> dict:
    p = {"name": "", "title": "", "email": "", "phone": "",
         "location": "", "linkedin": "", "github": "", "website": ""}

    email = EMAIL_RE.search(full_text)
    if email:
        p["email"] = email.group(0)

    phone = PHONE_RE.search(full_text)
    if phone:
        p["phone"] = phone.group(0).strip()

    linkedin = LINKEDIN_RE.search(full_text)
    if linkedin:
        p["linkedin"] = linkedin.group(0)

    github = GITHUB_RE.search(full_text)
    if github:
        p["github"] = github.group(0)

    # Website: first non-linkedin, non-github URL.
    for m in URL_RE.finditer(full_text):
        u = m.group(0)
        if "linkedin.com" in u.lower() or "github.com" in u.lower():
            continue
        p["website"] = u
        break

    # Name: first non-empty line that doesn't look like a contact line.
    for line in header_text.splitlines():
        s = line.strip()
        if not s:
            continue
        if EMAIL_RE.search(s) or PHONE_RE.search(s) or URL_RE.search(s):
            continue
        if len(s.split()) <= 6 and any(c.isalpha() for c in s):
            p["name"] = s
            break

    # Title: line right after the name with reasonable length, no contact info.
    if p["name"]:
        lines = [l.strip() for l in header_text.splitlines() if l.strip()]
        try:
            idx = lines.index(p["name"])
            for cand in lines[idx + 1:idx + 4]:
                if EMAIL_RE.search(cand) or PHONE_RE.search(cand) or URL_RE.search(cand):
                    continue
                if 2 <= len(cand.split()) <= 10:
                    p["title"] = cand
                    break
        except ValueError:
            pass

    # Location: look for "City, ST" or "City, Country" patterns.
    loc = re.search(
        r"\b([A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)?,\s*[A-Z]{2,}[a-zA-Z]*)\b",
        header_text,
    )
    if loc:
        p["location"] = loc.group(0)

    return p


def _extract_experience(text: str) -> list[dict]:
    """Heuristic: split on blank lines into blocks; each block becomes a job."""
    if not text:
        return []
    blocks = re.split(r"\n\s*\n", text)
    jobs: list[dict] = []
    for block in blocks:
        lines = [l.rstrip() for l in block.splitlines() if l.strip()]
        if not lines:
            continue
        head = lines[0]
        # Try "Role at Company" or "Role - Company" or "Role | Company"
        m = re.split(r"\s+(?:at|@|\||–|-)\s+", head, maxsplit=1)
        role = m[0].strip() if m else head
        company = m[1].strip() if len(m) > 1 else ""

        # Years
        years = YEAR_RANGE_RE.search(block)
        start = years.group("start") if years else ""
        end = years.group("end") if years else ""

        # Bullets: any line starting with -, *, • or "·"
        bullets = []
        for l in lines[1:]:
            stripped = l.lstrip()
            if stripped.startswith(("-", "*", "•", "·", "●", "▪")):
                bullets.append(stripped.lstrip("-*•·●▪ ").strip())
            elif bullets and not _looks_like_header(stripped):
                # Continuation of previous bullet
                bullets[-1] = (bullets[-1] + " " + stripped).strip()

        if not bullets:
            # Fall back to sentences
            tail = " ".join(lines[1:])
            bullets = [s.strip() for s in re.split(r"(?<=[.!?])\s+", tail) if s.strip()]

        jobs.append({
            "role": role,
            "company": company,
            "start": start,
            "end": end,
            "location": "",
            "bullets": bullets[:8],
        })
    return jobs


def _looks_like_header(line: str) -> bool:
    return bool(YEAR_RANGE_RE.search(line)) and len(line.split()) < 12


def _extract_education(text: str) -> list[dict]:
    if not text:
        return []
    out: list[dict] = []
    for block in re.split(r"\n\s*\n", text):
        lines = [l.strip() for l in block.splitlines() if l.strip()]
        if not lines:
            continue
        years = YEAR_RANGE_RE.search(block)
        out.append({
            "school":  lines[0],
            "degree":  lines[1] if len(lines) > 1 else "",
            "field":   "",
            "start":   years.group("start") if years else "",
            "end":     years.group("end") if years else "",
            "gpa":     "",
            "details": " ".join(lines[2:])[:300],
        })
    return out


def _extract_skills(text: str) -> list[str]:
    if not text:
        return []
    # Split on commas, semicolons, bullets, pipes, newlines.
    raw = re.split(r"[,;|•·●▪\n]+", text)
    candidates = [r.strip() for r in raw if 1 < len(r.strip()) <= 40]
    # Prefer skills that match the known DB; keep others as plain strings.
    known = extract_skills(text)
    seen = set()
    out: list[str] = []
    for s in known + candidates:
        key = s.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(s)
        if len(out) >= 30:
            break
    return out


def _extract_simple_list(text: str) -> list[str]:
    if not text:
        return []
    out: list[str] = []
    for line in text.splitlines():
        s = line.strip().lstrip("-*•·●▪ ").strip()
        if s:
            out.append(s)
    return out[:15]


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def parse_resume(file_bytes: bytes, filename: str) -> dict:
    """Parse a resume file into a partial resume dict."""
    text = extract_text(file_bytes, filename)
    sections = _split_sections(text)

    resume = empty_resume()
    resume["personal"] = _extract_personal(sections.get("_header", ""), text)
    if sections.get("summary"):
        resume["summary"] = sections["summary"].strip()
    resume["experience"] = _extract_experience(sections.get("experience", ""))
    resume["education"] = _extract_education(sections.get("education", ""))
    resume["skills"] = _extract_skills(sections.get("skills", "") or text)
    resume["projects"] = [
        {"name": (p.split(":")[0] if ":" in p else p)[:80],
         "description": p, "link": "", "tech": [], "bullets": []}
        for p in _extract_simple_list(sections.get("projects", ""))
    ]
    resume["certifications"] = [
        {"name": c, "issuer": "", "year": ""}
        for c in _extract_simple_list(sections.get("certifications", ""))
    ]
    resume["languages"] = [
        {"name": l, "level": ""}
        for l in _extract_simple_list(sections.get("languages", ""))
    ]
    resume["awards"] = [
        {"name": a, "year": "", "description": ""}
        for a in _extract_simple_list(sections.get("awards", ""))
    ]

    resume["_raw_text"] = text  # convenient for debugging in the UI
    return resume
