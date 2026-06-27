"""Analysis endpoints: ATS score, JD match."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from ..deps import get_current_user
from ..models import User
from ..schemas import AtsRequest, MatchRequest
from core import ats_analyzer, job_matcher

router = APIRouter(prefix="/api/analyze", tags=["analyze"])


@router.post("/ats")
def ats(payload: AtsRequest, user: User = Depends(get_current_user)):
    return ats_analyzer.analyze(payload.resume)


@router.post("/match")
def match(payload: MatchRequest, user: User = Depends(get_current_user)):
    return job_matcher.match(payload.resume, payload.job_description)
