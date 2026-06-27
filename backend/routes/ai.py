"""AI endpoints: bullet enhance, summary, cover letter, suggest skills, chat."""

from __future__ import annotations

import os
from typing import Any

from fastapi import APIRouter, Depends

from ..deps import get_current_user
from ..models import User
from ..schemas import (
    BulletEnhanceRequest, BulletEnhanceResponse,
    ChatRequest, ChatResponse,
    CoverLetterRequest, CoverLetterResponse,
    SummaryRequest, SummaryResponse,
)
from core import ai_engine
from data.skills_db import all_skills

router = APIRouter(prefix="/api/ai", tags=["ai"])


def _use_ai() -> bool:
    return bool(os.environ.get("OPENAI_API_KEY"))


@router.post("/enhance-bullet", response_model=BulletEnhanceResponse)
def enhance_bullet(payload: BulletEnhanceRequest, user: User = Depends(get_current_user)):
    enhanced = ai_engine.enhance_bullet(
        payload.bullet, role_hint=payload.role_hint, use_ai=_use_ai(),
    )
    return BulletEnhanceResponse(original=payload.bullet, enhanced=enhanced)


@router.post("/summary", response_model=SummaryResponse)
def generate_summary(payload: SummaryRequest, user: User = Depends(get_current_user)):
    summary = ai_engine.generate_summary(payload.resume, use_ai=_use_ai())
    return SummaryResponse(summary=summary)


@router.post("/cover-letter", response_model=CoverLetterResponse)
def cover_letter(payload: CoverLetterRequest, user: User = Depends(get_current_user)):
    letter = ai_engine.generate_cover_letter(
        payload.resume, payload.job_description,
        company=payload.company, use_ai=_use_ai(),
    )
    return CoverLetterResponse(letter=letter)


@router.get("/skill-suggestions")
def skill_suggestions(user: User = Depends(get_current_user)):
    """Return the full skills DB; the frontend uses it for autocomplete."""
    return {"skills": all_skills()}


@router.post("/suggest-skills")
def suggest_skills(payload: SummaryRequest, user: User = Depends(get_current_user)):
    """Suggest skills based on the resume's content + detected industry."""
    return {"suggestions": ai_engine.suggest_skills(payload.resume)}


# ---------------------------------------------------------------------------
# Lightweight rule-based + optional-LLM career chat assistant
# ---------------------------------------------------------------------------

@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest, user: User = Depends(get_current_user)):
    if _use_ai():
        from core.ai_engine import _openai_chat  # type: ignore
        prompt = (
            "You are a friendly career coach helping a user improve their resume. "
            "Give concrete, actionable advice in 3–5 short sentences.\n\n"
            f"User question: {payload.message}\n\n"
            f"Resume snapshot (JSON, truncated):\n{str(payload.resume)[:1500]}\n"
        )
        out = _openai_chat(prompt, system="You are a helpful resume coach.", max_tokens=300)
        if out:
            return ChatResponse(reply=out)

    # Local fallback — pattern-matched advice.
    return ChatResponse(reply=_local_chat(payload.message, payload.resume))


def _local_chat(message: str, resume: dict[str, Any]) -> str:
    msg = (message or "").lower()
    bullets = [
        b for j in (resume.get("experience") or [])
        for b in (j.get("bullets") or [])
    ]

    if any(k in msg for k in ["summary", "intro", "headline", "profile"]):
        return (
            "Aim for a 3-sentence summary: who you are (title + years), what you do best "
            "(top 3 skills), and one signature outcome. Use 'AI Enhance → Generate summary' "
            "to draft one in seconds."
        )
    if any(k in msg for k in ["bullet", "experience", "weak", "rewrite"]):
        weak = sum(1 for b in bullets if any(
            b.lower().startswith(p) for p in
            ("responsible for", "helped", "worked on", "duties included", "assisted")
        ))
        return (
            f"Strong bullets follow the formula: action verb + task + measurable result. "
            f"You currently have ~{weak} weak openers. Click 'Rewrite' on each one or use "
            f"'Enhance all' to fix them in bulk."
        )
    if any(k in msg for k in ["ats", "score", "keyword"]):
        return (
            "ATS scanners weigh 6 things: contact info, section coverage, keyword density, "
            "action verb strength, quantification, and length/formatting. Target 80+ on each "
            "dimension on the ATS page; the radar chart shows which area to fix first."
        )
    if any(k in msg for k in ["match", "job", "tailor"]):
        return (
            "Paste the job description on the Job Match page. Aim for 70+. Mirror the JD's "
            "exact phrasing in your bullets and skills, but only for things you've actually done."
        )
    if any(k in msg for k in ["cover letter", "letter"]):
        return (
            "Open Cover Letter, paste the job description, and click Generate. Edit the draft "
            "to add one specific anecdote that proves a key requirement of the role."
        )
    if any(k in msg for k in ["template", "design", "format", "pretty"]):
        return (
            "Modern works for tech, Classic for finance/law/academia, Minimal for design/PM, "
            "Creative for marketing/content. All four are ATS-friendly single-column layouts."
        )

    # Generic advice
    return (
        "I can help with: summaries, rewriting bullets, raising your ATS score, tailoring to a "
        "job description, picking a template, or drafting a cover letter. Which one would you "
        "like to tackle first?"
    )
