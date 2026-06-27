"""Pydantic request / response schemas — enhanced."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, EmailStr, Field


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field("", max_length=120)
    password: str = Field(min_length=6, max_length=128)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(min_length=6, max_length=128)


class ProfileUpdate(BaseModel):
    name: str | None = Field(None, max_length=120)
    avatar_color: str | None = None


class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    is_admin: bool
    created_at: datetime
    last_login: datetime | None
    login_count: int
    avatar_color: str

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# ---------------------------------------------------------------------------
# Resume
# ---------------------------------------------------------------------------

class ResumeBase(BaseModel):
    title: str = "Untitled Resume"
    template: str = "modern"
    data: dict[str, Any] = {}


class ResumeCreate(ResumeBase):
    pass


class ResumeUpdate(BaseModel):
    title: str | None = None
    template: str | None = None
    data: dict[str, Any] | None = None
    is_public: bool | None = None
    ats_score: int | None = None


class ResumeSummary(BaseModel):
    id: int
    title: str
    template: str
    updated_at: datetime
    created_at: datetime
    is_public: bool
    share_token: str
    view_count: int
    ats_score: int | None

    class Config:
        from_attributes = True


class ResumeOut(ResumeSummary):
    data: dict[str, Any]


# ---------------------------------------------------------------------------
# Admin
# ---------------------------------------------------------------------------

class AdminUserOut(BaseModel):
    id: int
    email: str
    name: str
    is_active: bool
    is_admin: bool
    created_at: datetime
    last_login: datetime | None
    login_count: int
    resume_count: int

    class Config:
        from_attributes = True


class AdminStats(BaseModel):
    total_users: int
    total_resumes: int
    active_users: int
    new_today: int
    new_this_week: int
    public_resumes: int
    total_logins: int


class AdminUserUpdate(BaseModel):
    is_active: bool | None = None
    is_admin: bool | None = None


class ActivityLogOut(BaseModel):
    id: int
    user_id: int
    user_email: str
    user_name: str
    action: str
    detail: str
    created_at: datetime

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# AI
# ---------------------------------------------------------------------------

class BulletEnhanceRequest(BaseModel):
    bullet: str
    role_hint: str = ""


class BulletEnhanceResponse(BaseModel):
    original: str
    enhanced: str


class SummaryRequest(BaseModel):
    resume: dict[str, Any]


class SummaryResponse(BaseModel):
    summary: str


class CoverLetterRequest(BaseModel):
    resume: dict[str, Any]
    job_description: str
    company: str = ""


class CoverLetterResponse(BaseModel):
    letter: str


class ChatRequest(BaseModel):
    message: str
    resume: dict[str, Any] = {}


class ChatResponse(BaseModel):
    reply: str


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

class AtsRequest(BaseModel):
    resume: dict[str, Any]


class MatchRequest(BaseModel):
    resume: dict[str, Any]
    job_description: str
