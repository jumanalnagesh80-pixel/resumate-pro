"""ATS (Applicant Tracking System) analyzer.

Scores a resume out of 100 across 6 weighted dimensions:

  1. Contact completeness    (15)
  2. Section coverage        (15)
  3. Keyword density         (20)
  4. Action verb strength    (15)
  5. Quantification          (15)
  6. Length & formatting     (20)

Returns a structured report with per-dimension scores, the overall score,
and human-readable suggestions.
"""

from __future__ import annotations

import re
from typing import Any

from data.action_verbs import all_verbs, WEAK_VERBS
from data.industry_keywords import detect_industry, keywords_for
from data.skills_db import extract_skills
from utils.helpers import flatten_bullets, has_number, tokenize


# ---------------------------------------------------------------------------
# Dimension scorers
# ---------------------------------------------------------------------------

def _score_contact(resume: dict) -> tuple[float, list[str]]:
    p = resume.get("personal", {}) or {}
    issues: list[str] = []
    points = 0.0
    weight_per = 15 / 5  # 5 fields

    if p.get("name"):
        points += weight_per
    else:
        issues.append("Add your full name to the contact section.")
    if p.get("email") and re.match(r"[^@]+@[^@]+\.[^@]+", p["email"]):
        points += weight_per
    else:
        issues.append("Add a valid email address.")
    if p.get("phone"):
        points += weight_per
    else:
        issues.append("Add a phone number.")
    if p.get("location"):
        points += weight_per
    else:
        issues.append("Add your city / region (recruiters filter on location).")
    if p.get("linkedin") or p.get("github") or p.get("website"):
        points += weight_per
    else:
        issues.append("Add at least one professional link (LinkedIn, GitHub, or portfolio).")
    return round(points, 1), issues


def _score_sections(resume: dict) -> tuple[float, list[str]]:
    weight_per = 15 / 5
    issues: list[str] = []
    points = 0.0

    if resume.get("summary"):
        points += weight_per
    else:
        issues.append("Add a short professional summary at the top.")
    if resume.get("experience"):
        points += weight_per
    else:
        issues.append("Add at least one experience entry.")
    if resume.get("education"):
        points += weight_per
    else:
        issues.append("Add an education entry.")
    if resume.get("skills"):
        points += weight_per
    else:
        issues.append("Add a Skills section — ATS parsers heavily rely on it.")
    if resume.get("projects") or resume.get("certifications") or resume.get("awards"):
        points += weight_per
    else:
        issues.append("Add Projects, Certifications, or Awards to differentiate yourself.")
    return round(points, 1), issues


def _all_text(resume: dict) -> str:
    parts: list[str] = []
    p = resume.get("personal", {}) or {}
    parts.append(p.get("title", "") or "")
    parts.append(resume.get("summary", "") or "")
    for j in resume.get("experience", []) or []:
        parts.append(j.get("role", "") or "")
        parts.append(j.get("company", "") or "")
        parts.extend(j.get("bullets", []) or [])
    for proj in resume.get("projects", []) or []:
        parts.append(proj.get("description", "") or "")
        parts.extend(proj.get("bullets", []) or [])
    parts.extend(resume.get("skills", []) or [])
    return "\n".join(parts)


def _score_keywords(resume: dict) -> tuple[float, list[str], dict]:
    text = _all_text(resume)
    industry = detect_industry(text)
    keywords = keywords_for(industry)

    lowered = text.lower()
    hits = [kw for kw in keywords if kw.lower() in lowered]
    coverage = len(hits) / max(len(keywords), 1)

    skills_in_resume = extract_skills(text)
    # Bonus for having a healthy number of recognised skills
    skill_bonus = min(len(skills_in_resume) / 12.0, 1.0)

    score = (coverage * 0.7 + skill_bonus * 0.3) * 20

    issues: list[str] = []
    missing = [kw for kw in keywords if kw.lower() not in lowered][:6]
    if missing:
        issues.append(
            f"Consider adding industry keywords ({industry.replace('_',' ')}): "
            + ", ".join(missing)
        )
    if len(skills_in_resume) < 8:
        issues.append("Your Skills section is light — aim for 10–15 recognised skills.")

    meta = {
        "industry": industry,
        "keyword_hits": hits,
        "missing_keywords": missing,
        "recognized_skills": skills_in_resume,
    }
    return round(score, 1), issues, meta


def _score_action_verbs(resume: dict) -> tuple[float, list[str]]:
    bullets = flatten_bullets(resume.get("experience", []) or [])
    bullets += flatten_bullets(resume.get("projects", []) or [])
    if not bullets:
        return 0.0, ["Add bullet points under your experience and projects."]

    strong_set = set(all_verbs())
    weak_phrases = WEAK_VERBS

    strong_count = 0
    weak_count = 0
    for b in bullets:
        first = (b.lstrip("-* •\t").split() or [""])[0].lower().rstrip(",.;:")
        if first in strong_set:
            strong_count += 1
        # Check the first ~3 words for a weak phrase.
        head = b.lower().lstrip("-* •\t")
        if any(head.startswith(p) for p in weak_phrases):
            weak_count += 1

    ratio_strong = strong_count / len(bullets)
    ratio_weak = weak_count / len(bullets)

    raw = max(0.0, ratio_strong - 0.5 * ratio_weak)
    score = min(raw * 1.2, 1.0) * 15  # cap at 15

    issues: list[str] = []
    if ratio_strong < 0.6:
        issues.append(
            f"Only {int(ratio_strong*100)}% of your bullets start with a strong action verb. "
            "Aim for 80%+ — use the AI Enhancer."
        )
    if ratio_weak > 0.1:
        issues.append(
            f"{int(ratio_weak*100)}% of your bullets start with a weak phrase "
            "(e.g. 'Responsible for', 'Helped with'). Rewrite them."
        )
    return round(score, 1), issues


def _score_quantification(resume: dict) -> tuple[float, list[str]]:
    bullets = flatten_bullets(resume.get("experience", []) or [])
    bullets += flatten_bullets(resume.get("projects", []) or [])
    if not bullets:
        return 0.0, ["Add quantified bullet points to your experience."]

    quantified = sum(1 for b in bullets if has_number(b))
    ratio = quantified / len(bullets)
    score = min(ratio * 1.5, 1.0) * 15

    issues: list[str] = []
    if ratio < 0.5:
        issues.append(
            f"Only {int(ratio*100)}% of your bullets contain a number. "
            "Quantify impact with %, $, time saved, or scale."
        )
    return round(score, 1), issues


def _score_formatting(resume: dict) -> tuple[float, list[str]]:
    """Length and formatting heuristics."""
    issues: list[str] = []
    points = 20.0  # start full and deduct

    text = _all_text(resume)
    words = tokenize(text)
    word_count = len(words)

    if word_count < 200:
        points -= 8
        issues.append(f"Resume is short ({word_count} words). Aim for 400–700.")
    elif word_count > 900:
        points -= 5
        issues.append(f"Resume is long ({word_count} words). Trim to 1 page (≈ 700 words).")

    # Bullet length sanity
    bullets = flatten_bullets(resume.get("experience", []) or [])
    if bullets:
        too_long = sum(1 for b in bullets if len(b.split()) > 35)
        if too_long:
            points -= 3
            issues.append(
                f"{too_long} bullet(s) exceed 35 words. Keep bullets concise (15–25 words)."
            )
        too_short = sum(1 for b in bullets if len(b.split()) < 5)
        if too_short:
            points -= 2
            issues.append(f"{too_short} bullet(s) are too short to convey impact.")

    # Summary length sanity
    summary = resume.get("summary", "") or ""
    if summary and len(summary.split()) > 90:
        points -= 2
        issues.append("Summary is too long; keep it under 60–80 words.")

    points = max(points, 0.0)
    return round(points, 1), issues


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

DIMENSIONS = [
    ("contact",       "Contact completeness", 15),
    ("sections",      "Section coverage",     15),
    ("keywords",      "Keyword density",      20),
    ("action_verbs",  "Action verb strength", 15),
    ("quantification","Quantification",       15),
    ("formatting",    "Length & formatting",  20),
]


def analyze(resume: dict) -> dict[str, Any]:
    """Return a full ATS report for a resume dict."""
    contact_score, contact_issues = _score_contact(resume)
    section_score, section_issues = _score_sections(resume)
    kw_score, kw_issues, kw_meta = _score_keywords(resume)
    verb_score, verb_issues = _score_action_verbs(resume)
    quant_score, quant_issues = _score_quantification(resume)
    fmt_score, fmt_issues = _score_formatting(resume)

    breakdown = {
        "contact":        {"score": contact_score, "max": 15, "issues": contact_issues},
        "sections":       {"score": section_score, "max": 15, "issues": section_issues},
        "keywords":       {"score": kw_score,      "max": 20, "issues": kw_issues, **kw_meta},
        "action_verbs":   {"score": verb_score,    "max": 15, "issues": verb_issues},
        "quantification": {"score": quant_score,   "max": 15, "issues": quant_issues},
        "formatting":     {"score": fmt_score,     "max": 20, "issues": fmt_issues},
    }

    overall = sum(b["score"] for b in breakdown.values())

    grade = _grade(overall)

    suggestions: list[str] = []
    for b in breakdown.values():
        suggestions.extend(b.get("issues", []) or [])

    return {
        "overall": round(overall, 1),
        "grade": grade,
        "breakdown": breakdown,
        "suggestions": suggestions[:12],
        "industry": kw_meta.get("industry"),
    }


def _grade(score: float) -> str:
    if score >= 90:
        return "A+ — Excellent"
    if score >= 80:
        return "A — Strong"
    if score >= 70:
        return "B — Good, with room to improve"
    if score >= 60:
        return "C — Needs work"
    if score >= 45:
        return "D — Weak"
    return "F — Major rework required"
