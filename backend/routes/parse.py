"""Resume file upload + parse endpoint."""

from __future__ import annotations

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from ..deps import get_current_user
from ..models import User
from core import resume_parser

router = APIRouter(prefix="/api/parse", tags=["parse"])

ALLOWED_EXT = {".pdf", ".docx", ".txt", ".md"}
MAX_SIZE = 5 * 1024 * 1024  # 5 MB


@router.post("")
async def parse_upload(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
):
    name = (file.filename or "").lower()
    ext = "." + name.rsplit(".", 1)[-1] if "." in name else ""
    if ext not in ALLOWED_EXT:
        raise HTTPException(400, f"Unsupported file type. Use: {', '.join(sorted(ALLOWED_EXT))}.")
    data = await file.read()
    if len(data) > MAX_SIZE:
        raise HTTPException(413, "File too large (max 5 MB).")
    parsed = resume_parser.parse_resume(data, file.filename or "resume")
    # Strip the raw text before returning — it's just for debugging.
    parsed.pop("_raw_text", None)
    return {"resume": parsed}
