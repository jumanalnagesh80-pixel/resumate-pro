"""Admin panel endpoints — requires is_admin=True."""

from __future__ import annotations

from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_admin_user
from ..models import ActivityLog, Resume, User
from ..schemas import (
    AdminStats, AdminUserOut, AdminUserUpdate, ActivityLogOut,
)

router = APIRouter(prefix="/api/admin", tags=["admin"])


# ---------------------------------------------------------------------------
# Dashboard statistics
# ---------------------------------------------------------------------------

@router.get("/stats", response_model=AdminStats)
def get_stats(db: Session = Depends(get_db), _: User = Depends(get_admin_user)):
    now = datetime.utcnow()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = now - timedelta(days=7)

    total_users    = db.query(func.count(User.id)).scalar() or 0
    total_resumes  = db.query(func.count(Resume.id)).scalar() or 0
    active_users   = db.query(func.count(User.id)).filter(User.is_active == True).scalar() or 0
    new_today      = db.query(func.count(User.id)).filter(User.created_at >= today_start).scalar() or 0
    new_this_week  = db.query(func.count(User.id)).filter(User.created_at >= week_start).scalar() or 0
    public_resumes = db.query(func.count(Resume.id)).filter(Resume.is_public == True).scalar() or 0
    total_logins   = db.query(func.sum(User.login_count)).scalar() or 0

    return AdminStats(
        total_users=total_users,
        total_resumes=total_resumes,
        active_users=active_users,
        new_today=new_today,
        new_this_week=new_this_week,
        public_resumes=public_resumes,
        total_logins=total_logins,
    )


@router.get("/growth")
def user_growth(days: int = 30, db: Session = Depends(get_db), _: User = Depends(get_admin_user)):
    """Return daily signup counts for the past N days."""
    cutoff = datetime.utcnow() - timedelta(days=days)
    rows = (
        db.query(
            func.date(User.created_at).label("day"),
            func.count(User.id).label("count"),
        )
        .filter(User.created_at >= cutoff)
        .group_by(func.date(User.created_at))
        .order_by(func.date(User.created_at))
        .all()
    )
    return {"data": [{"day": str(r.day), "count": r.count} for r in rows]}


# ---------------------------------------------------------------------------
# User management
# ---------------------------------------------------------------------------

@router.get("/users")
def list_users(
    skip: int = 0,
    limit: int = 50,
    search: str = "",
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user),
):
    q = db.query(User)
    if search:
        q = q.filter(
            (User.email.ilike(f"%{search}%")) | (User.name.ilike(f"%{search}%"))
        )
    total = q.count()
    users = q.order_by(User.created_at.desc()).offset(skip).limit(limit).all()

    result = []
    for u in users:
        resume_count = db.query(func.count(Resume.id)).filter(Resume.user_id == u.id).scalar() or 0
        result.append({
            "id": u.id,
            "email": u.email,
            "name": u.name,
            "is_active": u.is_active,
            "is_admin": u.is_admin,
            "created_at": u.created_at.isoformat(),
            "last_login": u.last_login.isoformat() if u.last_login else None,
            "login_count": u.login_count or 0,
            "resume_count": resume_count,
        })
    return {"total": total, "users": result}


@router.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found.")
    resume_count = db.query(func.count(Resume.id)).filter(Resume.user_id == user_id).scalar() or 0
    logs = (
        db.query(ActivityLog)
        .filter(ActivityLog.user_id == user_id)
        .order_by(ActivityLog.created_at.desc())
        .limit(20)
        .all()
    )
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "is_active": user.is_active,
        "is_admin": user.is_admin,
        "created_at": user.created_at.isoformat(),
        "last_login": user.last_login.isoformat() if user.last_login else None,
        "login_count": user.login_count or 0,
        "resume_count": resume_count,
        "activity": [
            {"action": l.action, "detail": l.detail, "created_at": l.created_at.isoformat()}
            for l in logs
        ],
    }


@router.patch("/users/{user_id}")
def update_user(
    user_id: int,
    payload: AdminUserUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found.")
    if user.id == admin.id and payload.is_admin is False:
        raise HTTPException(400, "You cannot remove your own admin privileges.")
    if payload.is_active is not None:
        user.is_active = payload.is_active
    if payload.is_admin is not None:
        user.is_admin = payload.is_admin
    db.add(ActivityLog(
        user_id=admin.id,
        action="admin_user_updated",
        detail=f"Updated user {user.email}: active={user.is_active} admin={user.is_admin}",
    ))
    db.commit()
    db.refresh(user)
    return {"id": user.id, "is_active": user.is_active, "is_admin": user.is_admin}


@router.delete("/users/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    if user_id == admin.id:
        raise HTTPException(400, "You cannot delete your own account via admin panel.")
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found.")
    email = user.email
    db.delete(user)
    db.add(ActivityLog(
        user_id=admin.id,
        action="admin_user_deleted",
        detail=f"Deleted user {email}",
    ))
    db.commit()
    return None


# ---------------------------------------------------------------------------
# Resume management
# ---------------------------------------------------------------------------

@router.get("/resumes")
def list_all_resumes(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user),
):
    total = db.query(func.count(Resume.id)).scalar() or 0
    rows = (
        db.query(Resume, User.email, User.name)
        .join(User, Resume.user_id == User.id)
        .order_by(Resume.updated_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return {
        "total": total,
        "resumes": [
            {
                "id": r.Resume.id,
                "title": r.Resume.title,
                "template": r.Resume.template,
                "is_public": r.Resume.is_public,
                "ats_score": r.Resume.ats_score,
                "view_count": r.Resume.view_count,
                "updated_at": r.Resume.updated_at.isoformat(),
                "owner_email": r.email,
                "owner_name": r.name,
            }
            for r in rows
        ],
    }


@router.delete("/resumes/{resume_id}", status_code=204)
def admin_delete_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    resume = db.get(Resume, resume_id)
    if not resume:
        raise HTTPException(404, "Resume not found.")
    db.add(ActivityLog(
        user_id=admin.id,
        action="admin_resume_deleted",
        detail=f"Deleted resume '{resume.title}' (id={resume_id})",
    ))
    db.delete(resume)
    db.commit()
    return None


# ---------------------------------------------------------------------------
# Activity log
# ---------------------------------------------------------------------------

@router.get("/activity")
def get_activity(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user),
):
    total = db.query(func.count(ActivityLog.id)).scalar() or 0
    rows = (
        db.query(ActivityLog, User.email, User.name)
        .join(User, ActivityLog.user_id == User.id)
        .order_by(ActivityLog.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return {
        "total": total,
        "logs": [
            {
                "id": r.ActivityLog.id,
                "user_id": r.ActivityLog.user_id,
                "user_email": r.email,
                "user_name": r.name,
                "action": r.ActivityLog.action,
                "detail": r.ActivityLog.detail,
                "created_at": r.ActivityLog.created_at.isoformat(),
            }
            for r in rows
        ],
    }
