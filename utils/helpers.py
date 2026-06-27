"""Small shared helpers."""

import re
from typing import Iterable


SENTENCE_END = re.compile(r"(?<=[.!?])\s+")
WORD_RE = re.compile(r"[A-Za-z][A-Za-z\-']+")


def tokenize(text: str) -> list[str]:
    """Lowercase word tokens, ignoring numbers and punctuation."""
    if not text:
        return []
    return [m.group(0).lower() for m in WORD_RE.finditer(text)]


def split_sentences(text: str) -> list[str]:
    if not text:
        return []
    return [s.strip() for s in SENTENCE_END.split(text.strip()) if s.strip()]


def has_number(text: str) -> bool:
    return bool(re.search(r"\d", text or ""))


def flatten_bullets(experience: Iterable[dict]) -> list[str]:
    out: list[str] = []
    for job in experience or []:
        for b in job.get("bullets", []) or []:
            if b and b.strip():
                out.append(b.strip())
    return out


def empty_resume() -> dict:
    """Return a blank but well-typed resume dict."""
    return {
        "personal": {
            "name": "",
            "title": "",
            "email": "",
            "phone": "",
            "location": "",
            "linkedin": "",
            "github": "",
            "website": "",
        },
        "summary": "",
        "experience": [],   # list of {company, role, start, end, location, bullets:[...]}
        "education": [],    # list of {school, degree, field, start, end, gpa, details}
        "projects": [],     # list of {name, description, link, tech:[], bullets:[...]}
        "skills": [],       # flat list of skill strings
        "certifications": [],  # list of {name, issuer, year}
        "languages": [],    # list of {name, level}
        "awards": [],       # list of {name, year, description}
    }
