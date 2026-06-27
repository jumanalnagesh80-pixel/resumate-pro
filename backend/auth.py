"""Password hashing and JWT helpers.

Uses ``bcrypt`` directly to avoid the well-known passlib + bcrypt 4.x
incompatibility (passlib reads ``bcrypt.__about__`` which no longer exists).
"""

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt
from jose import JWTError, jwt


# IMPORTANT: in production, set JWT_SECRET to a strong random value.
JWT_SECRET = os.environ.get("JWT_SECRET", "change-me-in-prod-please-use-a-long-random-string")
JWT_ALGO = "HS256"
JWT_EXPIRE_HOURS = int(os.environ.get("JWT_EXPIRE_HOURS", "24"))

# bcrypt hard-limits passwords to 72 bytes; longer inputs raise. We truncate
# at the byte level to make this safe while preserving the leading characters
# (which is what bcrypt would have hashed anyway).
_BCRYPT_MAX = 72


def _to_bytes(plain: str) -> bytes:
    b = plain.encode("utf-8", "ignore")
    return b[:_BCRYPT_MAX]


def hash_password(plain: str) -> str:
    """Return a bcrypt hash as a UTF-8 string."""
    return bcrypt.hashpw(_to_bytes(plain), bcrypt.gensalt(rounds=12)).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    if not hashed:
        return False
    try:
        return bcrypt.checkpw(_to_bytes(plain), hashed.encode("utf-8"))
    except (ValueError, TypeError):
        return False


def create_access_token(subject: str, extra: dict[str, Any] | None = None) -> str:
    now = datetime.now(timezone.utc)
    payload: dict[str, Any] = {
        "sub": subject,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(hours=JWT_EXPIRE_HOURS)).timestamp()),
    }
    if extra:
        payload.update(extra)
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)


def decode_token(token: str) -> dict[str, Any] | None:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
    except JWTError:
        return None
