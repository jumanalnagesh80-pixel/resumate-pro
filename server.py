"""AI Resume Builder — FastAPI entry point (enhanced).

Run with:
    uvicorn server:app --reload --port 8000

Or directly:
    python server.py
"""

from __future__ import annotations

import os
import sys

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from backend.database import init_db
from backend.routes import (
    ai as ai_routes,
    analyze as analyze_routes,
    auth as auth_routes,
    export as export_routes,
    parse as parse_routes,
    resumes as resume_routes,
    admin as admin_routes,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    # Ensure first user is admin
    _ensure_first_admin()
    yield


def _ensure_first_admin() -> None:
    """Make the first registered user an admin automatically."""
    from backend.database import SessionLocal
    from backend.models import User
    db = SessionLocal()
    try:
        first = db.query(User).order_by(User.id).first()
        if first and not first.is_admin:
            first.is_admin = True
            db.commit()
    finally:
        db.close()


app = FastAPI(
    title="ResuMate AI API",
    description="Full-stack AI resume builder with admin panel, real-time save, ATS scoring and JD matching.",
    version="3.0.0",
    lifespan=lifespan,
)

allowed_origins = os.environ.get("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

app.include_router(auth_routes.router)
app.include_router(resume_routes.router)
app.include_router(ai_routes.router)
app.include_router(analyze_routes.router)
app.include_router(export_routes.router)
app.include_router(parse_routes.router)
app.include_router(admin_routes.router)


@app.get("/api/health", tags=["meta"])
def health():
    from backend.database import SessionLocal
    from backend.models import User, Resume
    db = SessionLocal()
    try:
        user_count = db.query(User).count()
        resume_count = db.query(Resume).count()
    finally:
        db.close()
    return {
        "status": "ok",
        "version": app.version,
        "openai_enabled": bool(os.environ.get("OPENAI_API_KEY")),
        "users": user_count,
        "resumes": resume_count,
    }


# ---------------------------------------------------------------------------
# Static frontend
# ---------------------------------------------------------------------------

FRONTEND_DIR = os.path.join(HERE, "frontend")

if os.path.isdir(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

    @app.get("/", include_in_schema=False)
    def root():
        return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

    @app.get("/login", include_in_schema=False)
    @app.get("/register", include_in_schema=False)
    def auth_page():
        return FileResponse(os.path.join(FRONTEND_DIR, "auth.html"))

    @app.get("/app", include_in_schema=False)
    def app_page():
        return FileResponse(os.path.join(FRONTEND_DIR, "app.html"))

    @app.get("/admin", include_in_schema=False)
    def admin_page():
        return FileResponse(os.path.join(FRONTEND_DIR, "admin.html"))

    @app.get("/share/{token}", include_in_schema=False)
    def share_page(token: str):
        return FileResponse(os.path.join(FRONTEND_DIR, "share.html"))

else:
    @app.get("/", include_in_schema=False)
    def _no_frontend():
        return JSONResponse({"detail": "Frontend not built. API is up at /docs."}, status_code=200)


# ---------------------------------------------------------------------------
# Direct-run helper
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)
