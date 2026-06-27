"""PDF export endpoints — auth-protected, by resume id."""

from __future__ import annotations

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user
from ..models import Resume, User
from core import pdf_generator

router = APIRouter(prefix="/api/export", tags=["export"])


def _safe_filename(title: str) -> str:
    keep = "".join(c if c.isalnum() else "_" for c in (title or "resume").lower())
    return keep.strip("_") or "resume"


@router.get("/pdf/{resume_id}")
def export_pdf(
    resume_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    resume = db.get(Resume, resume_id)
    if not resume or resume.user_id != user.id:
        raise HTTPException(404, "Resume not found.")
    pdf = pdf_generator.render_pdf(resume.data or {}, template_key=resume.template)
    fname = _safe_filename(resume.title) + ".pdf"
    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{fname}"'},
    )


@router.post("/cover-letter/pdf")
def export_cover_letter(
    payload: dict = Body(...),
    user: User = Depends(get_current_user),
):
    text = (payload.get("text") or "").strip()
    if not text:
        raise HTTPException(400, "Empty cover letter.")
    name = payload.get("name") or user.name
    template = payload.get("template") or "modern"
    pdf = pdf_generator.render_cover_letter_pdf(text, name=name, template_key=template)
    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="cover_letter.pdf"'},
    )
