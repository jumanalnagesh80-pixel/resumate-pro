"""Auth endpoints: register, login, me, profile update, password change."""

from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from ..auth import create_access_token, hash_password, verify_password
from ..database import get_db
from ..deps import get_current_user
from ..models import ActivityLog, User
from ..schemas import (
    PasswordChange, ProfileUpdate,
    TokenResponse, UserCreate, UserLogin, UserOut,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])


def _log(db: Session, user: User, action: str, detail: str = "", ip: str = "") -> None:
    db.add(ActivityLog(user_id=user.id, action=action, detail=detail, ip_address=ip))


def _get_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else ""


@router.post("/register", response_model=TokenResponse, status_code=201)
def register(payload: UserCreate, request: Request, db: Session = Depends(get_db)):
    email = payload.email.lower().strip()
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )
    user = User(
        email=email,
        name=payload.name.strip() or email.split("@")[0],
        password_hash=hash_password(payload.password),
        last_login=datetime.utcnow(),
        login_count=1,
    )
    db.add(user)
    db.flush()
    _log(db, user, "register", f"Joined from {_get_ip(request)}", _get_ip(request))
    db.commit()
    db.refresh(user)
    token = create_access_token(subject=str(user.id))
    return TokenResponse(access_token=token, user=UserOut.model_validate(user))


@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin, request: Request, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email.lower().strip()).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is disabled. Contact support.")
    user.last_login = datetime.utcnow()
    user.login_count = (user.login_count or 0) + 1
    _log(db, user, "login", "", _get_ip(request))
    db.commit()
    db.refresh(user)
    token = create_access_token(subject=str(user.id))
    return TokenResponse(access_token=token, user=UserOut.model_validate(user))


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return UserOut.model_validate(user)


@router.put("/profile", response_model=UserOut)
def update_profile(
    payload: ProfileUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if payload.name is not None:
        user.name = payload.name.strip() or user.name
    if payload.avatar_color is not None:
        user.avatar_color = payload.avatar_color
    db.commit()
    db.refresh(user)
    return UserOut.model_validate(user)


@router.post("/change-password", status_code=200)
def change_password(
    payload: PasswordChange,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not verify_password(payload.current_password, user.password_hash):
        raise HTTPException(status_code=400, detail="Current password is incorrect.")
    user.password_hash = hash_password(payload.new_password)
    db.add(ActivityLog(user_id=user.id, action="password_changed", detail=""))
    db.commit()
    return {"message": "Password updated successfully."}
