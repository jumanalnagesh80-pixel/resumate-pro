"""AI engine for the Resume Builder.

Provides three primary capabilities:

1. ``enhance_bullet`` — rewrites a weak resume bullet point into a stronger,
   action-verb-led version with a quantification hint where appropriate.
2. ``generate_summary`` — produces a 3-line professional summary from a
   resume dict.
3. ``generate_cover_letter`` — produces a tailored cover letter for a job
   description.

The engine prefers the OpenAI API when ``OPENAI_API_KEY`` is set, but always
ships with a deterministic local fallback so the prototype works offline.
"""

from __future__ import annotations

import os
import re
import random
from typing import Optional

from data.action_verbs import (
    ACTION_VERBS, WEAK_VERBS, WEAK_TO_CATEGORY, pick_verb,
)
from data.skills_db import extract_skills
from data.industry_keywords import detect_industry, keywords_for
from utils.helpers import has_number, tokenize


# ---------------------------------------------------------------------------
# OpenAI helper (optional)
# ---------------------------------------------------------------------------

def _openai_client():
    """Return an OpenAI client if the key is available, else None."""
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        return None
    try:
        from openai import OpenAI
        return OpenAI(api_key=key)
    except Exception:
        return None


def _openai_chat(prompt: str, system: str, max_tokens: int = 400) -> Optional[str]:
    client = _openai_client()
    if client is None:
        return None
    try:
        resp = client.chat.completions.create(
            model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
            max_tokens=max_tokens,
        )
        return (resp.choices[0].message.content or "").strip()
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Bullet enhancement
# ---------------------------------------------------------------------------

QUANT_HINTS = [
    "(consider adding a metric: %, $, # of users, time saved)",
    "(quantify impact: by X%, $K saved, N users reached)",
    "(add a number: how many, how much, how fast)",
]


def _strip_weak_prefix(bullet: str) -> tuple[str, Optional[str]]:
    """Remove a weak phrase from the start of the bullet.

    Returns (cleaned_bullet, weak_phrase_or_None).
    """
    lowered = bullet.lower().lstrip("-* •\t")
    for phrase in sorted(WEAK_VERBS, key=len, reverse=True):
        if lowered.startswith(phrase):
            cleaned = bullet.lstrip("-* •\t")[len(phrase):].lstrip(" ,:;-")
            # Keep capitalisation natural
            if cleaned:
                cleaned = cleaned[0].lower() + cleaned[1:]
            return cleaned, phrase
    return bullet.lstrip("-* •\t"), None


def _local_enhance_bullet(bullet: str, role_hint: str = "") -> str:
    """Deterministic local rewrite for a single bullet."""
    if not bullet or not bullet.strip():
        return bullet

    text = bullet.strip().rstrip(".")
    cleaned, weak = _strip_weak_prefix(text)

    # Pick a strong verb: based on the weak phrase if we recognise one,
    # otherwise based on the bullet's content.
    if weak and weak in WEAK_TO_CATEGORY:
        category = WEAK_TO_CATEGORY[weak]
    else:
        category = _infer_category(cleaned + " " + role_hint)

    seed = sum(ord(c) for c in cleaned[:40]) if cleaned else 0
    verb = pick_verb(category, seed=seed)

    # Lowercase first word of cleaned (we are about to put a verb in front).
    body = cleaned.strip()
    if body:
        body = body[0].lower() + body[1:]
    new_bullet = f"{verb} {body}".strip()

    # Add a quantification hint if no number is present.
    if not has_number(new_bullet):
        hint = QUANT_HINTS[seed % len(QUANT_HINTS)]
        new_bullet = f"{new_bullet} {hint}"

    if not new_bullet.endswith("."):
        # Avoid a period if we appended a parenthetical hint
        if not new_bullet.endswith(")"):
            new_bullet += "."
    return new_bullet


def _infer_category(text: str) -> str:
    """Pick the best ACTION_VERBS category for a piece of text."""
    lowered = text.lower()
    score = {cat: 0 for cat in ACTION_VERBS}
    rules = [
        ("leadership", ["team", "manage", "lead", "mentor", "report", "direct"]),
        ("achievement", ["award", "recognit", "exceed", "deliver", "ship"]),
        ("improvement", ["improve", "optimi", "speed", "performance", "reduce", "faster"]),
        ("creation", ["build", "develop", "design", "implement", "create", "launch"]),
        ("analysis", ["analy", "research", "investig", "evaluat", "audit"]),
        ("communication", ["present", "communicat", "negotiat", "stakeholder", "client"]),
        ("management", ["manag", "operat", "oversee", "coordinat", "schedule"]),
        ("collaboration", ["collaborat", "partner", "cross-funct", "across team"]),
        ("growth", ["grow", "scale", "increase", "expand", "double"]),
        ("reduction", ["reduc", "cut", "decrease", "eliminat", "save"]),
    ]
    for cat, kws in rules:
        for kw in kws:
            if kw in lowered:
                score[cat] += 1
    best = max(score, key=score.get)
    return best if score[best] > 0 else "creation"


def enhance_bullet(bullet: str, role_hint: str = "", use_ai: bool = True) -> str:
    """Public: rewrite a weak bullet into a strong, action-led one."""
    if not bullet or not bullet.strip():
        return bullet

    if use_ai:
        out = _openai_chat(
            prompt=(
                "Rewrite the following resume bullet point so it starts with a strong "
                "action verb, is concise (max 25 words), and includes a quantified "
                "impact when possible.\n\n"
                f"Role context: {role_hint or 'unspecified'}\n"
                f"Original bullet: {bullet}\n\n"
                "Return only the rewritten bullet, no commentary."
            ),
            system="You are an expert resume writer focused on impact and ATS optimization.",
            max_tokens=120,
        )
        if out:
            return out.strip().lstrip("-• ").strip()

    return _local_enhance_bullet(bullet, role_hint)


def enhance_bullets(bullets: list[str], role_hint: str = "", use_ai: bool = True) -> list[str]:
    return [enhance_bullet(b, role_hint, use_ai) for b in bullets]


# ---------------------------------------------------------------------------
# Summary generation
# ---------------------------------------------------------------------------

def _years_of_experience(experience: list[dict]) -> int:
    """Crude estimate from experience entries' year ranges."""
    total = 0
    for job in experience or []:
        start = _year(job.get("start", ""))
        end = _year(job.get("end", "")) or 0
        if start and end and end >= start:
            total += end - start
        elif start and not end:
            # Assume current = roughly 1 year if "Present"
            total += 1
    return total


def _year(s: str) -> Optional[int]:
    if not s:
        return None
    m = re.search(r"(19|20)\d{2}", s)
    return int(m.group(0)) if m else None


def _local_generate_summary(resume: dict) -> str:
    personal = resume.get("personal", {}) or {}
    title = personal.get("title") or "Professional"
    name = personal.get("name") or ""
    experience = resume.get("experience", []) or []
    yrs = _years_of_experience(experience)
    skills = resume.get("skills", []) or []

    # Most recent role + company for flavour.
    recent = experience[0] if experience else {}
    recent_company = recent.get("company") or "leading organizations"

    top_skills = ", ".join(skills[:5]) if skills else "modern tools and best practices"

    industry = detect_industry(
        " ".join(
            [title]
            + [b for j in experience for b in (j.get("bullets") or [])]
        )
    )
    industry_label = industry.replace("_", " ")

    yrs_phrase = f"{yrs}+ years of experience" if yrs >= 1 else "hands-on experience"

    line1 = f"{title} with {yrs_phrase} delivering impact in {industry_label}."
    line2 = f"Proven track record at {recent_company}, with expertise in {top_skills}."
    line3 = (
        "Known for translating complex problems into measurable outcomes and "
        "shipping high-quality solutions in fast-paced environments."
    )
    summary = " ".join([line1, line2, line3])
    if name:
        return summary
    return summary


def generate_summary(resume: dict, use_ai: bool = True) -> str:
    """Produce a 3-sentence professional summary."""
    if use_ai:
        bullets = []
        for j in resume.get("experience", []) or []:
            bullets.extend(j.get("bullets") or [])
        prompt = (
            "Write a concise 3-sentence professional summary for the resume below. "
            "Do not invent achievements; use only the information given. "
            "Tone: confident, modern, ATS-friendly. Max 60 words.\n\n"
            f"Title: {resume.get('personal',{}).get('title','')}\n"
            f"Skills: {', '.join(resume.get('skills', [])[:12])}\n"
            f"Recent bullets: {' | '.join(bullets[:8])}\n"
        )
        out = _openai_chat(
            prompt,
            system="You are an expert resume writer.",
            max_tokens=200,
        )
        if out:
            return out.strip()
    return _local_generate_summary(resume)


# ---------------------------------------------------------------------------
# Cover letter
# ---------------------------------------------------------------------------

def _local_cover_letter(resume: dict, job_description: str, company: str = "") -> str:
    personal = resume.get("personal", {}) or {}
    name = personal.get("name") or "Candidate"
    title = personal.get("title") or "professional"

    job_skills = extract_skills(job_description)
    candidate_skills = set(s.lower() for s in resume.get("skills", []) or [])
    matching = [s for s in job_skills if s.lower() in candidate_skills][:6]
    if not matching:
        matching = (resume.get("skills") or [])[:6]

    industry = detect_industry(job_description)
    company = company or "your team"

    bullets = []
    for j in resume.get("experience", []) or []:
        bullets.extend(j.get("bullets") or [])
    highlight = bullets[0] if bullets else "delivering high-impact work end-to-end"

    body = f"""Dear Hiring Manager,

I am excited to apply for the role at {company}. As a {title} with hands-on experience in {industry.replace('_',' ')}, I was drawn to this opportunity because it aligns directly with the problems I love to solve.

In my recent work I have {highlight.lower().rstrip('.')}. I bring practical expertise in {', '.join(matching)} and a track record of turning ambiguous requirements into shipped, measurable outcomes.

What excites me most about {company} is the chance to contribute to a team that values both speed and craft. I would welcome the opportunity to discuss how my background can help you reach your next milestone.

Thank you for your time and consideration.

Sincerely,
{name}
"""
    return body.strip()


def generate_cover_letter(
    resume: dict, job_description: str, company: str = "", use_ai: bool = True
) -> str:
    if use_ai:
        prompt = (
            "Write a professional, concise cover letter (max 250 words, 3-4 paragraphs) "
            "tailored to the job description, using only facts from the resume. "
            "Do not invent achievements.\n\n"
            f"Company: {company or 'the company'}\n"
            f"Candidate name: {resume.get('personal',{}).get('name','')}\n"
            f"Candidate title: {resume.get('personal',{}).get('title','')}\n"
            f"Candidate skills: {', '.join(resume.get('skills', [])[:15])}\n"
            f"Recent experience bullets: "
            f"{' | '.join([b for j in resume.get('experience', []) for b in (j.get('bullets') or [])][:8])}\n\n"
            f"Job description:\n{job_description[:2000]}\n"
        )
        out = _openai_chat(
            prompt,
            system="You are an expert career coach who writes concise, tailored cover letters.",
            max_tokens=600,
        )
        if out:
            return out.strip()
    return _local_cover_letter(resume, job_description, company)


# ---------------------------------------------------------------------------
# Suggestions
# ---------------------------------------------------------------------------

def suggest_skills(resume: dict, top_n: int = 8) -> list[str]:
    """Suggest extra skills based on the detected industry minus the ones already listed."""
    text = " ".join(
        [resume.get("summary", "") or ""]
        + [b for j in resume.get("experience", []) or [] for b in (j.get("bullets") or [])]
        + [resume.get("personal", {}).get("title", "") or ""]
    )
    industry = detect_industry(text)
    have = {s.lower() for s in resume.get("skills", []) or []}

    extracted = extract_skills(text)
    suggestions = [s for s in extracted if s.lower() not in have]

    # Top-up with industry keywords if we still need more.
    for kw in keywords_for(industry):
        if len(suggestions) >= top_n:
            break
        if kw.lower() not in have and kw not in suggestions:
            suggestions.append(kw)
    return suggestions[:top_n]
