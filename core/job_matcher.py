"""Job-description matcher.

Given a resume dict and a job description string, returns:

  - ``match_score``       — TF-IDF cosine similarity scaled to 0–100.
  - ``matched_keywords``  — keywords present in both texts.
  - ``missing_keywords``  — keywords in the JD but not in the resume.
  - ``skill_gap``         — recognised skills in the JD missing from the resume.
  - ``top_jd_terms``      — most informative terms in the JD (TF-IDF top-K).
  - ``recommendations``   — actionable bullet suggestions.

Falls back to a pure-Python TF-IDF if scikit-learn is unavailable so the
prototype remains runnable.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from typing import Any

from data.skills_db import extract_skills
from utils.helpers import tokenize


# ---------------------------------------------------------------------------
# TF-IDF (sklearn first, then a tiny pure-python fallback)
# ---------------------------------------------------------------------------

STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "from",
    "has", "have", "in", "is", "it", "its", "of", "on", "or", "that", "the",
    "to", "was", "were", "will", "with", "this", "these", "those", "you",
    "your", "we", "our", "they", "their", "i", "me", "my", "if", "so",
    "do", "does", "doing", "than", "then", "there", "here", "about",
    "into", "over", "under", "while", "during", "between", "such", "any",
    "each", "every", "all", "some", "no", "not", "only", "own", "same",
    "should", "would", "could", "can", "may", "might", "must", "via",
    "etc", "vs", "per", "across", "within", "among",
}


def _cosine_sklearn(a: str, b: str) -> float | None:
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_features=4000)
        m = vec.fit_transform([a, b])
        return float(cosine_similarity(m[0], m[1])[0, 0])
    except Exception:
        return None


def _cosine_local(a: str, b: str) -> float:
    """Pure-python TF-IDF cosine fallback."""
    docs = [_tokens_no_stop(a), _tokens_no_stop(b)]
    df: Counter[str] = Counter()
    for d in docs:
        df.update(set(d))
    n = len(docs)
    vecs = []
    for d in docs:
        tf = Counter(d)
        v: dict[str, float] = {}
        for term, count in tf.items():
            idf = math.log((1 + n) / (1 + df[term])) + 1
            v[term] = (count / max(len(d), 1)) * idf
        vecs.append(v)
    a_v, b_v = vecs
    common = set(a_v) & set(b_v)
    dot = sum(a_v[t] * b_v[t] for t in common)
    na = math.sqrt(sum(x * x for x in a_v.values()))
    nb = math.sqrt(sum(x * x for x in b_v.values()))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def _tokens_no_stop(text: str) -> list[str]:
    return [t for t in tokenize(text) if t not in STOP_WORDS and len(t) > 1]


def _cosine(a: str, b: str) -> float:
    sk = _cosine_sklearn(a, b)
    return sk if sk is not None else _cosine_local(a, b)


# ---------------------------------------------------------------------------
# Top JD terms
# ---------------------------------------------------------------------------

def _top_jd_terms(jd: str, k: int = 15) -> list[str]:
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        vec = TfidfVectorizer(
            stop_words="english", ngram_range=(1, 2), max_features=2000
        )
        m = vec.fit_transform([jd])
        scores = m.toarray()[0]
        terms = vec.get_feature_names_out()
        order = scores.argsort()[::-1]
        return [terms[i] for i in order[:k] if scores[i] > 0]
    except Exception:
        # Fallback: most frequent non-stopword tokens
        toks = _tokens_no_stop(jd)
        return [w for w, _ in Counter(toks).most_common(k)]


# ---------------------------------------------------------------------------
# Resume-as-text
# ---------------------------------------------------------------------------

def _resume_to_text(resume: dict) -> str:
    parts: list[str] = []
    p = resume.get("personal", {}) or {}
    parts.append(p.get("title", "") or "")
    parts.append(resume.get("summary", "") or "")
    for j in resume.get("experience", []) or []:
        parts.append(j.get("role", "") or "")
        parts.append(j.get("company", "") or "")
        parts.extend(j.get("bullets", []) or [])
    for proj in resume.get("projects", []) or []:
        parts.append(proj.get("name", "") or "")
        parts.append(proj.get("description", "") or "")
        parts.extend(proj.get("bullets", []) or [])
        parts.extend(proj.get("tech", []) or [])
    parts.extend(resume.get("skills", []) or [])
    for c in resume.get("certifications", []) or []:
        parts.append(c.get("name", "") or "")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def match(resume: dict, job_description: str) -> dict[str, Any]:
    """Return a structured match report."""
    jd = (job_description or "").strip()
    if not jd:
        return {
            "match_score": 0.0,
            "matched_keywords": [],
            "missing_keywords": [],
            "skill_gap": [],
            "top_jd_terms": [],
            "recommendations": ["Paste a job description to run a match."],
        }

    resume_text = _resume_to_text(resume)
    resume_text_lower = resume_text.lower()
    cosine = _cosine(resume_text, jd)

    # Skill gap (recognised skills only — high-precision)
    jd_skills = extract_skills(jd)
    resume_skills = set(s.lower() for s in resume.get("skills", []) or [])
    matched_skills = [
        s for s in jd_skills
        if s.lower() in resume_skills or s.lower() in resume_text_lower
    ]
    missing_skills = [s for s in jd_skills if s not in matched_skills]

    # Top JD terms with matched/missing classification (broader than the skills DB)
    top_terms = _top_jd_terms(jd, k=20)
    matched_kw, missing_kw = [], []
    for t in top_terms:
        if all(part in resume_text_lower for part in t.split()):
            matched_kw.append(t)
        else:
            missing_kw.append(t)

    # Hybrid score: cosine + directional JD-coverage. The latter answers
    # "what fraction of the JD's most informative terms appear in the resume?"
    # and is more meaningful to a job-seeker than raw cosine similarity.
    coverage = (
        len(matched_kw) / len(top_terms) if top_terms else 0.0
    )
    skill_coverage = (
        len(matched_skills) / len(jd_skills) if jd_skills else coverage
    )
    blended = (cosine * 0.3) + (coverage * 0.4) + (skill_coverage * 0.3)
    score = round(min(blended * 100, 100), 1)

    recommendations = _recommendations(score, missing_skills, missing_kw)

    return {
        "match_score": score,
        "cosine_similarity": round(cosine * 100, 1),
        "keyword_coverage": round(coverage * 100, 1),
        "skill_coverage": round(skill_coverage * 100, 1),
        "matched_keywords": matched_kw,
        "missing_keywords": missing_kw,
        "skill_gap": missing_skills,
        "matched_skills": matched_skills,
        "top_jd_terms": top_terms,
        "recommendations": recommendations,
    }


def _recommendations(score: float, missing_skills: list[str], missing_kw: list[str]) -> list[str]:
    recs: list[str] = []
    if score < 30:
        recs.append(
            "Match is low. Tailor your summary and top 3 bullets to mirror the JD's language."
        )
    elif score < 60:
        recs.append("Decent match — target 70+ by aligning phrasing to the JD.")
    else:
        recs.append("Strong match. Polish bullets and quantify impact for a final boost.")

    if missing_skills:
        recs.append(
            "Add these JD-mentioned skills (only if you genuinely have them): "
            + ", ".join(missing_skills[:8])
        )
    if missing_kw:
        recs.append(
            "Consider weaving these JD phrases into your bullets: "
            + ", ".join(missing_kw[:6])
        )
    recs.append(
        "Use the AI Bullet Enhancer on each experience bullet after editing."
    )
    return recs


def keyword_density(text: str, keywords: list[str]) -> dict[str, int]:
    """Return how many times each keyword appears in `text` (case-insensitive)."""
    lowered = (text or "").lower()
    return {kw: len(re.findall(re.escape(kw.lower()), lowered)) for kw in keywords}
