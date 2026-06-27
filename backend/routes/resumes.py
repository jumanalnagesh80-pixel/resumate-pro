"""Resume CRUD + share endpoints — enhanced with view count tracking."""

from __future__ import annotations

import copy

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user
from ..models import ActivityLog, Resume, User
from ..schemas import ResumeCreate, ResumeOut, ResumeSummary, ResumeUpdate
from utils.helpers import empty_resume

router = APIRouter(prefix="/api/resumes", tags=["resumes"])


def _ensure_owner(resume: Resume | None, user: User) -> Resume:
    if not resume:
        raise HTTPException(404, "Resume not found.")
    if resume.user_id != user.id:
        raise HTTPException(404, "Resume not found.")
    return resume


def _log(db: Session, user: User, action: str, detail: str = "") -> None:
    db.add(ActivityLog(user_id=user.id, action=action, detail=detail))


@router.get("", response_model=list[ResumeSummary])
def list_resumes(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = (
        db.query(Resume)
        .filter(Resume.user_id == user.id)
        .order_by(Resume.updated_at.desc())
        .all()
    )
    return [ResumeSummary.model_validate(r) for r in rows]


@router.post("", response_model=ResumeOut, status_code=201)
def create_resume(
    payload: ResumeCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    data = payload.data or empty_resume()
    resume = Resume(
        user_id=user.id,
        title=payload.title or "Untitled Resume",
        template=payload.template or "modern",
        data=data,
    )
    db.add(resume)
    db.flush()
    _log(db, user, "resume_created", f"'{resume.title}'")
    db.commit()
    db.refresh(resume)
    return ResumeOut.model_validate(resume)


@router.get("/{resume_id}", response_model=ResumeOut)
def get_resume(resume_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    resume = _ensure_owner(db.get(Resume, resume_id), user)
    return ResumeOut.model_validate(resume)


@router.put("/{resume_id}", response_model=ResumeOut)
def update_resume(
    resume_id: int,
    payload: ResumeUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    resume = _ensure_owner(db.get(Resume, resume_id), user)
    if payload.title is not None:
        resume.title = payload.title.strip() or "Untitled Resume"
    if payload.template is not None:
        resume.template = payload.template
    if payload.data is not None:
        resume.data = payload.data
    if payload.is_public is not None:
        resume.is_public = payload.is_public
    if payload.ats_score is not None:
        resume.ats_score = payload.ats_score
    _log(db, user, "resume_updated", f"'{resume.title}'")
    db.commit()
    db.refresh(resume)
    return ResumeOut.model_validate(resume)


@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resume(resume_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    resume = _ensure_owner(db.get(Resume, resume_id), user)
    title = resume.title
    db.delete(resume)
    _log(db, user, "resume_deleted", f"'{title}'")
    db.commit()
    return None


@router.post("/{resume_id}/duplicate", response_model=ResumeOut, status_code=201)
def duplicate_resume(resume_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    src = _ensure_owner(db.get(Resume, resume_id), user)
    clone = Resume(
        user_id=user.id,
        title=f"{src.title} (Copy)",
        template=src.template,
        data=copy.deepcopy(src.data or {}),
    )
    db.add(clone)
    db.flush()
    _log(db, user, "resume_duplicated", f"'{src.title}'")
    db.commit()
    db.refresh(clone)
    return ResumeOut.model_validate(clone)


@router.get("/share/{token}", response_model=ResumeOut, tags=["share"])
def get_shared(token: str, db: Session = Depends(get_db)):
    """Public, read-only view. Increments view count."""
    resume = db.query(Resume).filter(Resume.share_token == token).first()
    if not resume or not resume.is_public:
        raise HTTPException(404, "Shared resume not found or not public.")
    resume.view_count = (resume.view_count or 0) + 1
    db.commit()
    db.refresh(resume)
    return ResumeOut.model_validate(resume)
