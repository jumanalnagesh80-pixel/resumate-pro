"""ORM models — enhanced with admin, activity log, and notifications."""

from __future__ import annotations

import secrets
from datetime import datetime

from sqlalchemy import (
    Boolean, DateTime, ForeignKey, Integer, JSON, String, Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


def _now() -> datetime:
    return datetime.utcnow()


def _share_token() -> str:
    return secrets.token_urlsafe(16)


class User(Base):
    __tablename__ = "users"

    id:            Mapped[int]      = mapped_column(Integer, primary_key=True)
    email:         Mapped[str]      = mapped_column(String(255), unique=True, index=True, nullable=False)
    name:          Mapped[str]      = mapped_column(String(120), default="")
    password_hash: Mapped[str]      = mapped_column(String(255), nullable=False)
    created_at:    Mapped[datetime] = mapped_column(DateTime, default=_now)
    updated_at:    Mapped[datetime] = mapped_column(DateTime, default=_now, onupdate=_now)
    is_active:     Mapped[bool]     = mapped_column(Boolean, default=True)
    is_admin:      Mapped[bool]     = mapped_column(Boolean, default=False)
    last_login:    Mapped[datetime] = mapped_column(DateTime, nullable=True)
    login_count:   Mapped[int]      = mapped_column(Integer, default=0)
    avatar_color:  Mapped[str]      = mapped_column(String(20), default="#6366f1")

    resumes:       Mapped[list["Resume"]]      = relationship(back_populates="owner", cascade="all, delete-orphan")
    activity_logs: Mapped[list["ActivityLog"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Resume(Base):
    __tablename__ = "resumes"

    id:         Mapped[int]      = mapped_column(Integer, primary_key=True)
    user_id:    Mapped[int]      = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    title:      Mapped[str]      = mapped_column(String(160), default="Untitled Resume")
    template:   Mapped[str]      = mapped_column(String(40), default="modern")
    data:       Mapped[dict]     = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=_now, onupdate=_now)
    view_count: Mapped[int]      = mapped_column(Integer, default=0)
    ats_score:  Mapped[int]      = mapped_column(Integer, nullable=True)

    # Public read-only share
    is_public:   Mapped[bool]   = mapped_column(Boolean, default=False)
    share_token: Mapped[str]    = mapped_column(String(40), default=_share_token, unique=True, index=True)

    owner: Mapped["User"] = relationship(back_populates="resumes")


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id:         Mapped[int]      = mapped_column(Integer, primary_key=True)
    user_id:    Mapped[int]      = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    action:     Mapped[str]      = mapped_column(String(80), nullable=False)   # e.g. "resume_created"
    detail:     Mapped[str]      = mapped_column(String(255), default="")
    ip_address: Mapped[str]      = mapped_column(String(45), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now, index=True)

    user: Mapped["User"] = relationship(back_populates="activity_logs")
