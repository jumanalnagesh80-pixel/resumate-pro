"""End-to-end smoke test for the AI Resume Builder.

Boots the FastAPI app in-process via TestClient and exercises every public
endpoint end-to-end: register, login, resume CRUD, AI enhance, summary,
cover letter, ATS, match, PDF export, share, parse, chat.

Run:
    python3.12 smoke_test.py
"""

from __future__ import annotations

import os
import secrets
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

# Use an isolated SQLite file so the test never touches the real app.db.
_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
_db.close()
os.environ["DATABASE_URL"] = f"sqlite:///{_db.name}"
os.environ.setdefault("JWT_SECRET", "test-secret")

from fastapi.testclient import TestClient

import server                                  # noqa: E402
from backend.database import init_db          # noqa: E402

init_db()
client = TestClient(server.app)


def step(label: str) -> None:
    print(f"  → {label}")


def main() -> int:
    print("Smoke testing AI Resume Builder…")

    # ---------- Auth ----------
    step("register")
    email = f"alex+{secrets.token_hex(3)}@example.com"
    r = client.post("/api/auth/register",
                    json={"email": email, "name": "Alex Kumar", "password": "secret123"})
    assert r.status_code == 201, r.text
    token = r.json()["access_token"]
    auth = {"Authorization": f"Bearer {token}"}

    step("login")
    r = client.post("/api/auth/login", json={"email": email, "password": "secret123"})
    assert r.status_code == 200, r.text

    step("me")
    r = client.get("/api/auth/me", headers=auth)
    assert r.status_code == 200 and r.json()["email"] == email

    # ---------- Resume CRUD ----------
    step("create resume")
    sample_resume = {
        "personal": {"name": "Alex Kumar", "title": "Senior Software Engineer",
                     "email": email, "phone": "+1-555-0142", "location": "SF",
                     "linkedin": "linkedin.com/in/alex", "github": "", "website": ""},
        "summary": "Senior engineer with 7+ years building distributed systems.",
        "experience": [{
            "role": "Senior Software Engineer", "company": "Lumen Labs",
            "start": "2022", "end": "Present", "location": "SF",
            "bullets": [
                "Was responsible for the inference service",
                "Helped migrate to Kubernetes",
            ],
        }],
        "education": [{"school": "U Michigan", "degree": "B.S.", "field": "CS",
                       "start": "2013", "end": "2017", "gpa": "3.8", "details": ""}],
        "skills": ["Python", "Kubernetes", "PostgreSQL", "AWS"],
        "projects": [], "certifications": [], "languages": [], "awards": [],
    }
    r = client.post("/api/resumes", headers=auth, json={
        "title": "Test resume", "template": "modern", "data": sample_resume,
    })
    assert r.status_code == 201, r.text
    resume_id = r.json()["id"]

    step("list resumes")
    r = client.get("/api/resumes", headers=auth)
    assert r.status_code == 200 and len(r.json()) == 1

    step("update resume")
    r = client.put(f"/api/resumes/{resume_id}", headers=auth,
                   json={"title": "Test (renamed)"})
    assert r.status_code == 200 and r.json()["title"] == "Test (renamed)"

    step("duplicate resume")
    r = client.post(f"/api/resumes/{resume_id}/duplicate", headers=auth)
    assert r.status_code == 201
    dup_id = r.json()["id"]

    # ---------- AI ----------
    step("enhance bullet")
    r = client.post("/api/ai/enhance-bullet", headers=auth,
                    json={"bullet": "Was responsible for the deploy pipeline",
                          "role_hint": "DevOps"})
    enhanced = r.json()["enhanced"]
    assert r.status_code == 200 and enhanced
    assert not enhanced.lower().startswith("was responsible"), enhanced

    step("generate summary")
    r = client.post("/api/ai/summary", headers=auth, json={"resume": sample_resume})
    assert r.status_code == 200 and r.json()["summary"]

    step("generate cover letter")
    jd = "We need a Senior Engineer with Kubernetes and AWS experience."
    r = client.post("/api/ai/cover-letter", headers=auth,
                    json={"resume": sample_resume, "job_description": jd, "company": "Acme"})
    cover = r.json()["letter"]
    assert r.status_code == 200 and "Acme" in cover

    step("suggest skills")
    r = client.post("/api/ai/suggest-skills", headers=auth, json={"resume": sample_resume})
    assert r.status_code == 200 and isinstance(r.json()["suggestions"], list)

    step("skills DB list")
    r = client.get("/api/ai/skill-suggestions", headers=auth)
    assert r.status_code == 200 and len(r.json()["skills"]) > 50

    step("chat")
    r = client.post("/api/ai/chat", headers=auth,
                    json={"message": "How do I improve my ATS score?", "resume": sample_resume})
    assert r.status_code == 200 and r.json()["reply"]

    # ---------- Analysis ----------
    step("ats")
    r = client.post("/api/analyze/ats", headers=auth, json={"resume": sample_resume})
    body = r.json()
    assert r.status_code == 200 and 0 <= body["overall"] <= 100
    print(f"      ATS overall: {body['overall']:.1f} ({body['grade']})")

    step("match")
    r = client.post("/api/analyze/match", headers=auth,
                    json={"resume": sample_resume, "job_description": jd})
    body = r.json()
    assert r.status_code == 200 and 0 <= body["match_score"] <= 100
    print(f"      Match: {body['match_score']:.1f} (skill cov {body['skill_coverage']:.0f}%)")

    # ---------- Export ----------
    step("PDF export")
    r = client.get(f"/api/export/pdf/{resume_id}", headers=auth)
    assert r.status_code == 200
    assert r.content[:4] == b"%PDF", "PDF magic bytes missing"

    step("cover letter PDF")
    r = client.post("/api/export/cover-letter/pdf", headers=auth,
                    json={"text": cover, "name": "Alex Kumar", "template": "modern"})
    assert r.status_code == 200 and r.content[:4] == b"%PDF"

    # ---------- Parse ----------
    step("parse upload (txt)")
    txt = (b"Alex Kumar\nSenior Software Engineer\nalex@example.com\n\n"
           b"Skills\nPython, Kubernetes, AWS\n")
    r = client.post("/api/parse", headers=auth,
                    files={"file": ("demo.txt", txt, "text/plain")})
    assert r.status_code == 200 and "Python" in r.json()["resume"]["skills"]

    # ---------- Share ----------
    step("public share toggle")
    r = client.put(f"/api/resumes/{resume_id}", headers=auth, json={"is_public": True})
    assert r.status_code == 200 and r.json()["is_public"] is True
    share_token = r.json()["share_token"]

    step("read shared resume (no auth)")
    r = client.get(f"/api/resumes/share/{share_token}")
    assert r.status_code == 200 and r.json()["title"] == "Test (renamed)"

    step("share blocked when private")
    r = client.put(f"/api/resumes/{resume_id}", headers=auth, json={"is_public": False})
    r = client.get(f"/api/resumes/share/{share_token}")
    assert r.status_code == 404

    # ---------- Negative auth ----------
    step("auth required")
    r = client.get("/api/resumes")
    assert r.status_code == 401

    step("cleanup")
    client.delete(f"/api/resumes/{resume_id}", headers=auth)
    client.delete(f"/api/resumes/{dup_id}", headers=auth)

    # ---------- Health ----------
    step("health")
    r = client.get("/api/health")
    assert r.status_code == 200 and r.json()["status"] == "ok"

    # ---------- Static frontend ----------
    step("frontend served")
    r = client.get("/")
    assert r.status_code == 200 and "ResuMate" in r.text
    r = client.get("/login")
    assert r.status_code == 200 and "Sign in" in r.text
    r = client.get("/app")
    assert r.status_code == 200 and "Workspace" in r.text

    print(f"\n✅ All {21} smoke checks passed.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except AssertionError as e:
        print(f"\n❌ FAILED: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        import traceback
        traceback.print_exc()
        sys.exit(2)
    finally:
        try: os.unlink(_db.name)
        except Exception: pass
