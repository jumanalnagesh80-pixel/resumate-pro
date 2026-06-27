"""Streamlit page renderers.

Each function below is a self-contained page. ``app.py`` dispatches to one
of them based on the sidebar selection.
"""

from __future__ import annotations

import json
import os
from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from core import ai_engine, ats_analyzer, job_matcher, pdf_generator, resume_parser
from core.templates import list_templates, get_template
from data.skills_db import all_skills, categorize
from utils.helpers import empty_resume


# ---------------------------------------------------------------------------
# Session helpers
# ---------------------------------------------------------------------------

def _resume() -> dict:
    if "resume" not in st.session_state:
        st.session_state.resume = empty_resume()
    return st.session_state.resume


def _save(resume: dict):
    st.session_state.resume = resume


def _ai_on() -> bool:
    return bool(os.environ.get("OPENAI_API_KEY")) and st.session_state.get("use_ai", True)


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------

def page_dashboard():
    st.markdown(
        "<div class='kr-hero'><h1>AI Resume Builder</h1>"
        "<p>Build, optimize, and tailor a high-impact resume powered by AI.</p></div>",
        unsafe_allow_html=True,
    )

    resume = _resume()
    report = ats_analyzer.analyze(resume)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("ATS Score", f"{report['overall']:.0f}/100", report["grade"].split("—")[0].strip())
    exp_count = len(resume.get("experience", []) or [])
    c2.metric("Experience entries", exp_count)
    c3.metric("Skills listed", len(resume.get("skills", []) or []))
    c4.metric("Industry detected", (report.get("industry") or "—").replace("_", " ").title())

    st.markdown("### Get started")
    cc1, cc2, cc3 = st.columns(3)
    with cc1:
        st.markdown(
            "<div class='kr-card'><h4>1. Build</h4>"
            "<p>Fill in your details on the <b>Builder</b> page. "
            "Already have a resume? Upload it on <b>Import</b>.</p></div>",
            unsafe_allow_html=True,
        )
    with cc2:
        st.markdown(
            "<div class='kr-card'><h4>2. Optimize</h4>"
            "<p>Use <b>AI Enhance</b> to rewrite weak bullets, generate a summary, "
            "and check your <b>ATS Score</b>.</p></div>",
            unsafe_allow_html=True,
        )
    with cc3:
        st.markdown(
            "<div class='kr-card'><h4>3. Tailor & Export</h4>"
            "<p>Match a job description on <b>Job Match</b>, then export a "
            "polished PDF in your favourite template.</p></div>",
            unsafe_allow_html=True,
        )

    if not _ai_on():
        st.info(
            "💡 Optional: set the `OPENAI_API_KEY` environment variable to enable richer "
            "AI rewrites. The app works fully offline using a built-in rule-based engine."
        )


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------

def page_builder():
    st.markdown("<div class='kr-section'><h3>Resume Builder</h3></div>", unsafe_allow_html=True)
    resume = _resume()

    # ---------- Personal ----------
    with st.expander("👤 Personal & Contact", expanded=True):
        p = resume["personal"]
        c1, c2 = st.columns(2)
        p["name"]     = c1.text_input("Full name", p.get("name", ""))
        p["title"]    = c2.text_input("Headline / Title", p.get("title", ""))
        p["email"]    = c1.text_input("Email", p.get("email", ""))
        p["phone"]    = c2.text_input("Phone", p.get("phone", ""))
        p["location"] = c1.text_input("Location", p.get("location", ""))
        p["linkedin"] = c2.text_input("LinkedIn URL", p.get("linkedin", ""))
        p["github"]   = c1.text_input("GitHub URL", p.get("github", ""))
        p["website"]  = c2.text_input("Website / Portfolio", p.get("website", ""))

    # ---------- Summary ----------
    with st.expander("📝 Professional Summary", expanded=True):
        resume["summary"] = st.text_area(
            "Summary (2–4 sentences)",
            value=resume.get("summary", ""),
            height=110,
        )
        if st.button("✨ Generate with AI", key="gen_summary"):
            with st.spinner("Drafting your summary…"):
                resume["summary"] = ai_engine.generate_summary(resume, use_ai=_ai_on())
            st.success("Summary generated.")
            st.rerun()

    # ---------- Experience ----------
    with st.expander("💼 Experience", expanded=True):
        for i, job in enumerate(resume["experience"]):
            st.markdown(f"**Experience #{i + 1}**")
            c1, c2 = st.columns(2)
            job["role"]     = c1.text_input("Role", job.get("role", ""), key=f"role_{i}")
            job["company"]  = c2.text_input("Company", job.get("company", ""), key=f"co_{i}")
            job["start"]    = c1.text_input("Start (YYYY)", job.get("start", ""), key=f"st_{i}")
            job["end"]      = c2.text_input("End (YYYY or Present)", job.get("end", ""), key=f"en_{i}")
            job["location"] = c1.text_input("Location", job.get("location", ""), key=f"loc_{i}")
            bullets = "\n".join(job.get("bullets", []) or [])
            new_b = st.text_area(
                "Bullets (one per line)", value=bullets, height=140, key=f"bul_{i}"
            )
            job["bullets"] = [b.strip() for b in new_b.splitlines() if b.strip()]
            cdel, cenh, _ = st.columns([1, 1, 4])
            if cdel.button("🗑 Remove", key=f"rm_{i}"):
                resume["experience"].pop(i)
                _save(resume); st.rerun()
            if cenh.button("✨ Enhance bullets", key=f"enh_{i}"):
                with st.spinner("Rewriting bullets…"):
                    job["bullets"] = ai_engine.enhance_bullets(
                        job["bullets"], role_hint=job.get("role", ""), use_ai=_ai_on(),
                    )
                _save(resume); st.success("Bullets enhanced."); st.rerun()
            st.markdown("---")
        if st.button("➕ Add experience"):
            resume["experience"].append({
                "role": "", "company": "", "start": "", "end": "",
                "location": "", "bullets": [],
            })
            _save(resume); st.rerun()

    # ---------- Education ----------
    with st.expander("🎓 Education"):
        for i, ed in enumerate(resume["education"]):
            c1, c2 = st.columns(2)
            ed["school"] = c1.text_input("School", ed.get("school", ""), key=f"sch_{i}")
            ed["degree"] = c2.text_input("Degree", ed.get("degree", ""), key=f"deg_{i}")
            ed["field"]  = c1.text_input("Field", ed.get("field", ""), key=f"fld_{i}")
            ed["gpa"]    = c2.text_input("GPA", ed.get("gpa", ""), key=f"gpa_{i}")
            ed["start"]  = c1.text_input("Start", ed.get("start", ""), key=f"est_{i}")
            ed["end"]    = c2.text_input("End", ed.get("end", ""), key=f"een_{i}")
            ed["details"] = st.text_area("Details", ed.get("details", ""), height=70, key=f"det_{i}")
            if st.button("🗑 Remove", key=f"rm_ed_{i}"):
                resume["education"].pop(i); _save(resume); st.rerun()
            st.markdown("---")
        if st.button("➕ Add education"):
            resume["education"].append({
                "school": "", "degree": "", "field": "", "start": "",
                "end": "", "gpa": "", "details": "",
            })
            _save(resume); st.rerun()

    # ---------- Projects ----------
    with st.expander("🚀 Projects"):
        for i, pr in enumerate(resume["projects"]):
            c1, c2 = st.columns(2)
            pr["name"] = c1.text_input("Project", pr.get("name", ""), key=f"pn_{i}")
            pr["link"] = c2.text_input("Link", pr.get("link", ""), key=f"pl_{i}")
            pr["description"] = st.text_area(
                "Description", pr.get("description", ""), height=70, key=f"pd_{i}"
            )
            tech = ", ".join(pr.get("tech", []) or [])
            new_tech = st.text_input("Tech (comma-separated)", tech, key=f"pt_{i}")
            pr["tech"] = [t.strip() for t in new_tech.split(",") if t.strip()]
            bullets = "\n".join(pr.get("bullets", []) or [])
            new_b = st.text_area("Bullets", bullets, height=80, key=f"pb_{i}")
            pr["bullets"] = [b.strip() for b in new_b.splitlines() if b.strip()]
            if st.button("🗑 Remove", key=f"rm_pr_{i}"):
                resume["projects"].pop(i); _save(resume); st.rerun()
            st.markdown("---")
        if st.button("➕ Add project"):
            resume["projects"].append({
                "name": "", "description": "", "link": "", "tech": [], "bullets": [],
            })
            _save(resume); st.rerun()

    # ---------- Skills ----------
    with st.expander("🛠 Skills"):
        skills = ", ".join(resume["skills"])
        new_s = st.text_area(
            "Skills (comma-separated)", skills, height=80,
            help="Tip: aim for 12–20 relevant skills."
        )
        resume["skills"] = [s.strip() for s in new_s.split(",") if s.strip()]
        if st.button("✨ Suggest skills"):
            sug = ai_engine.suggest_skills(resume)
            if sug:
                st.info("Consider adding: " + ", ".join(sug))
            else:
                st.success("Looks good — no obvious gaps.")

    # ---------- Extras ----------
    with st.expander("🏆 Certifications, Awards, Languages"):
        certs = "\n".join(
            [f"{c.get('name','')} | {c.get('issuer','')} | {c.get('year','')}"
             for c in resume["certifications"]]
        )
        new_certs = st.text_area(
            "Certifications (one per line, format: name | issuer | year)",
            certs, height=80,
        )
        resume["certifications"] = []
        for line in new_certs.splitlines():
            parts = [p.strip() for p in line.split("|")]
            if parts and parts[0]:
                resume["certifications"].append({
                    "name": parts[0],
                    "issuer": parts[1] if len(parts) > 1 else "",
                    "year": parts[2] if len(parts) > 2 else "",
                })

        awards = "\n".join(
            [f"{a.get('name','')} | {a.get('year','')} | {a.get('description','')}"
             for a in resume["awards"]]
        )
        new_awards = st.text_area(
            "Awards (one per line, format: name | year | description)",
            awards, height=80,
        )
        resume["awards"] = []
        for line in new_awards.splitlines():
            parts = [p.strip() for p in line.split("|")]
            if parts and parts[0]:
                resume["awards"].append({
                    "name": parts[0],
                    "year": parts[1] if len(parts) > 1 else "",
                    "description": parts[2] if len(parts) > 2 else "",
                })

        langs = "\n".join(
            [f"{l.get('name','')} | {l.get('level','')}" for l in resume["languages"]]
        )
        new_langs = st.text_area(
            "Languages (one per line, format: language | level)", langs, height=70,
        )
        resume["languages"] = []
        for line in new_langs.splitlines():
            parts = [p.strip() for p in line.split("|")]
            if parts and parts[0]:
                resume["languages"].append({
                    "name": parts[0],
                    "level": parts[1] if len(parts) > 1 else "",
                })

    _save(resume)
    st.success("All changes saved to the current session.")


# ---------------------------------------------------------------------------
# AI Enhance
# ---------------------------------------------------------------------------

def page_enhance():
    st.markdown("<div class='kr-section'><h3>AI Enhance</h3></div>", unsafe_allow_html=True)
    resume = _resume()

    if not resume["experience"]:
        st.info("Add at least one experience entry on the Builder page first.")
        return

    st.caption(
        "Rewrite weak bullets into strong, action-led, quantified statements. "
        + ("✅ OpenAI mode" if _ai_on() else "🧠 Local engine mode")
    )

    for i, job in enumerate(resume["experience"]):
        st.markdown(f"#### {job.get('role') or 'Role'} · {job.get('company') or 'Company'}")
        bullets = job.get("bullets", []) or []
        if not bullets:
            st.write("_No bullets yet._")
            continue
        for j, b in enumerate(bullets):
            c1, c2 = st.columns([5, 1])
            c1.markdown(f"<span class='kr-old'>{b}</span>", unsafe_allow_html=True)
            if c2.button("Rewrite", key=f"rw_{i}_{j}"):
                with st.spinner("Rewriting…"):
                    new = ai_engine.enhance_bullet(
                        b, role_hint=job.get("role", ""), use_ai=_ai_on()
                    )
                bullets[j] = new
                _save(resume); st.rerun()
            if b != (bullets[j] if j < len(bullets) else b):
                st.markdown(
                    f"<span class='kr-new'>→ {bullets[j]}</span>",
                    unsafe_allow_html=True,
                )
        if st.button("✨ Rewrite all", key=f"rwall_{i}"):
            with st.spinner("Rewriting all bullets…"):
                job["bullets"] = ai_engine.enhance_bullets(
                    bullets, role_hint=job.get("role", ""), use_ai=_ai_on(),
                )
            _save(resume); st.success("Done."); st.rerun()
        st.markdown("---")

    st.markdown("#### Skill suggestions")
    sug = ai_engine.suggest_skills(resume)
    if sug:
        st.write(", ".join(f"`{s}`" for s in sug))
    else:
        st.write("No suggestions — your skill section already looks comprehensive.")


# ---------------------------------------------------------------------------
# ATS Score
# ---------------------------------------------------------------------------

def page_ats():
    st.markdown("<div class='kr-section'><h3>ATS Score Analyzer</h3></div>", unsafe_allow_html=True)
    resume = _resume()
    report = ats_analyzer.analyze(resume)

    overall = report["overall"]
    grade = report["grade"]
    chip_class = (
        "kr-chip-good" if overall >= 80
        else "kr-chip-warn" if overall >= 60
        else "kr-chip-bad"
    )
    st.markdown(
        f"<h2>{overall:.0f}/100 "
        f"<span class='kr-chip {chip_class}'>{grade}</span></h2>",
        unsafe_allow_html=True,
    )

    # Radar chart
    cats = [d[1] for d in ats_analyzer.DIMENSIONS]
    keys = [d[0] for d in ats_analyzer.DIMENSIONS]
    maxes = [d[2] for d in ats_analyzer.DIMENSIONS]
    scores = [report["breakdown"][k]["score"] for k in keys]
    pct = [round((s / m) * 100, 1) for s, m in zip(scores, maxes)]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=pct, theta=cats, fill="toself", name="Your resume",
        line=dict(color="#2E75B6"),
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(range=[0, 100], visible=True)),
        showlegend=False, margin=dict(t=30, b=10, l=30, r=30), height=380,
    )
    c1, c2 = st.columns([1, 1])
    c1.plotly_chart(fig, use_container_width=True)

    df = pd.DataFrame({
        "Dimension": cats,
        "Score":     scores,
        "Max":       maxes,
        "Percent":   pct,
    })
    c2.dataframe(df, hide_index=True, use_container_width=True)

    st.markdown("#### Suggestions")
    for s in report["suggestions"]:
        st.markdown(f"- {s}")
    if not report["suggestions"]:
        st.success("Nothing to fix — your resume is in great shape!")

    with st.expander("Detected industry & keywords"):
        st.write(f"**Industry:** {report.get('industry','').replace('_',' ').title()}")
        st.write("**Keyword hits:**")
        st.write(", ".join(report["breakdown"]["keywords"].get("keyword_hits", [])) or "—")
        st.write("**Missing keywords:**")
        st.write(", ".join(report["breakdown"]["keywords"].get("missing_keywords", [])) or "—")


# ---------------------------------------------------------------------------
# Job Match
# ---------------------------------------------------------------------------

def page_match():
    st.markdown("<div class='kr-section'><h3>Job Description Matcher</h3></div>", unsafe_allow_html=True)
    resume = _resume()

    jd = st.text_area("Paste the job description", height=240,
                      value=st.session_state.get("last_jd", ""))
    st.session_state.last_jd = jd

    if not jd.strip():
        st.info("Paste a job description above to see how well your resume matches.")
        return

    report = job_matcher.match(resume, jd)
    score = report["match_score"]

    chip_class = (
        "kr-chip-good" if score >= 70
        else "kr-chip-warn" if score >= 40
        else "kr-chip-bad"
    )
    st.markdown(
        f"<h2>{score:.0f}/100 "
        f"<span class='kr-chip {chip_class}'>blended match</span></h2>",
        unsafe_allow_html=True,
    )
    bc1, bc2, bc3 = st.columns(3)
    bc1.metric("Keyword coverage", f"{report['keyword_coverage']:.0f}%")
    bc2.metric("Skill coverage", f"{report['skill_coverage']:.0f}%")
    bc3.metric("Cosine similarity", f"{report['cosine_similarity']:.0f}%")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Matched JD terms")
        if report["matched_keywords"]:
            st.write(" ".join(
                f"<span class='kr-chip kr-chip-good'>{k}</span>"
                for k in report["matched_keywords"]
            ), unsafe_allow_html=True)
        else:
            st.write("—")
    with c2:
        st.markdown("#### Missing JD terms")
        if report["missing_keywords"]:
            st.write(" ".join(
                f"<span class='kr-chip kr-chip-bad'>{k}</span>"
                for k in report["missing_keywords"]
            ), unsafe_allow_html=True)
        else:
            st.write("—")

    if report["skill_gap"]:
        st.markdown("#### Skill gap")
        st.write(", ".join(report["skill_gap"]))

    st.markdown("#### Recommendations")
    for r in report["recommendations"]:
        st.markdown(f"- {r}")

    # Bar chart of matched vs missing
    df = pd.DataFrame({
        "Status": ["Matched"] * len(report["matched_keywords"])
                  + ["Missing"] * len(report["missing_keywords"]),
        "Term":   report["matched_keywords"] + report["missing_keywords"],
    })
    if not df.empty:
        counts = df.groupby("Status").size().reset_index(name="Count")
        fig = px.bar(counts, x="Status", y="Count", color="Status",
                     color_discrete_map={"Matched": "#22c55e", "Missing": "#ef4444"})
        fig.update_layout(height=300, showlegend=False, margin=dict(t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------

def page_templates():
    st.markdown("<div class='kr-section'><h3>Templates</h3></div>", unsafe_allow_html=True)
    selected = st.session_state.get("template", "modern")
    cols = st.columns(2)
    for i, t in enumerate(list_templates()):
        with cols[i % 2]:
            is_sel = t["key"] == selected
            cls = "kr-template selected" if is_sel else "kr-template"
            st.markdown(
                f"<div class='{cls}'>"
                f"<h5>{t['name']}{' ✓' if is_sel else ''}</h5>"
                f"<p>{t['description']}</p>"
                f"<span class='swatch' style='background:{t['primary']}'></span>"
                f"<span class='swatch' style='background:{t['secondary']}'></span>"
                f"<span class='swatch' style='background:{t['muted']}'></span>"
                f"<p style='margin-top:8px;color:#64748b;font-size:.85rem'>"
                f"Header: {t['header_style']} · Font: {t['font_main']}</p>"
                f"</div>",
                unsafe_allow_html=True,
            )
            if st.button(f"Use {t['name']}", key=f"sel_{t['key']}"):
                st.session_state.template = t["key"]
                st.rerun()


# ---------------------------------------------------------------------------
# Cover letter
# ---------------------------------------------------------------------------

def page_cover_letter():
    st.markdown("<div class='kr-section'><h3>Cover Letter Generator</h3></div>", unsafe_allow_html=True)
    resume = _resume()
    company = st.text_input("Company name", value=st.session_state.get("cl_company", ""))
    st.session_state.cl_company = company
    jd = st.text_area("Job description", height=200, value=st.session_state.get("last_jd", ""))

    if st.button("✨ Generate cover letter"):
        if not jd.strip():
            st.warning("Paste a job description first.")
            return
        with st.spinner("Drafting your cover letter…"):
            text = ai_engine.generate_cover_letter(
                resume, jd, company=company, use_ai=_ai_on(),
            )
        st.session_state.cover_letter = text
        st.rerun()

    text = st.session_state.get("cover_letter", "")
    text = st.text_area("Letter (editable)", value=text, height=380)
    st.session_state.cover_letter = text

    if text.strip():
        pdf = pdf_generator.render_cover_letter_pdf(
            text,
            name=resume.get("personal", {}).get("name", ""),
            template_key=st.session_state.get("template", "modern"),
        )
        ts = datetime.now().strftime("%Y%m%d")
        st.download_button(
            "⬇️ Download cover letter PDF",
            data=pdf,
            file_name=f"cover_letter_{ts}.pdf",
            mime="application/pdf",
        )


# ---------------------------------------------------------------------------
# Import
# ---------------------------------------------------------------------------

def page_import():
    st.markdown("<div class='kr-section'><h3>Import Existing Resume</h3></div>", unsafe_allow_html=True)
    file = st.file_uploader(
        "Upload a PDF, DOCX, or TXT resume",
        type=["pdf", "docx", "txt", "md"],
    )
    if file and st.button("Parse & load into builder"):
        with st.spinner("Extracting…"):
            parsed = resume_parser.parse_resume(file.getvalue(), file.name)
        st.session_state.resume = parsed
        st.success("Loaded. Head over to the Builder to review and edit.")
        with st.expander("Raw extracted text (debug)"):
            st.text(parsed.get("_raw_text", ""))


# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------

def page_export():
    st.markdown("<div class='kr-section'><h3>Export</h3></div>", unsafe_allow_html=True)
    resume = _resume()
    template_key = st.session_state.get("template", "modern")
    tpl = get_template(template_key)
    st.write(f"Active template: **{tpl['name']}**  "
             f"_(change it on the Templates page)_")

    pdf = pdf_generator.render_pdf(resume, template_key=template_key)
    ts = datetime.now().strftime("%Y%m%d")
    safe_name = (resume.get("personal", {}).get("name") or "resume").replace(" ", "_").lower()

    c1, c2 = st.columns(2)
    c1.download_button(
        "⬇️ Download PDF",
        data=pdf,
        file_name=f"{safe_name}_{ts}.pdf",
        mime="application/pdf",
    )
    c2.download_button(
        "⬇️ Download JSON (round-trip)",
        data=json.dumps({k: v for k, v in resume.items() if not k.startswith("_")},
                         indent=2),
        file_name=f"{safe_name}_{ts}.json",
        mime="application/json",
    )

    st.markdown("#### Restore from JSON")
    up = st.file_uploader("Upload a previously-saved JSON resume", type=["json"])
    if up:
        try:
            data = json.loads(up.getvalue().decode("utf-8"))
            base = empty_resume()
            base.update({k: data[k] for k in base if k in data})
            st.session_state.resume = base
            st.success("Resume loaded.")
            st.rerun()
        except Exception as exc:
            st.error(f"Invalid JSON: {exc}")
