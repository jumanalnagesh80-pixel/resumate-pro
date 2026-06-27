"""SQLAlchemy database setup.

Uses SQLite by default; override with the ``DATABASE_URL`` environment
variable (e.g. ``postgresql+psycopg://user:pass@host/db``).
"""

from __future__ import annotations

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    f"sqlite:///{os.path.join(os.path.dirname(__file__), '..', 'app.db')}",
)

# SQLite needs ``check_same_thread=False`` so the same connection can be used
# across worker threads (FastAPI's default).
_connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=_connect_args, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


class Base(DeclarativeBase):
    """Base class for all ORM models."""


def get_db():
    """FastAPI dependency that yields a request-scoped DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Create all tables. Called once on app startup."""
    # Import models so SQLAlchemy registers them on Base.metadata.
    from . import models  # noqa: F401
    Base.metadata.create_all(bind=engine)
