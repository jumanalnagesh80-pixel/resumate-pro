"""PDF generation with multiple templates.

Renders a resume dict to a PDF byte stream using ReportLab's platypus
flowables. All templates are single-column to remain ATS-friendly.
"""

from __future__ import annotations

import io
from typing import Any

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, KeepTogether,
)
from reportlab.platypus.flowables import HRFlowable, Flowable

from core.templates import get_template


# ---------------------------------------------------------------------------
# Custom flowables
# ---------------------------------------------------------------------------

class HeaderBanner(Flowable):
    """Coloured band used by the 'modern' template."""

    def __init__(self, name: str, title: str, contact: str,
                 width: float, height: float, tpl: dict):
        super().__init__()
        self.name = name
        self.title = title
        self.contact = contact
        self.width = width
        self.height = height
        self.tpl = tpl

    def draw(self):
        c = self.canv
        c.setFillColor(HexColor(self.tpl["primary"]))
        c.rect(-0.5 * inch, -0.2 * inch, self.width + 1.0 * inch,
               self.height + 0.2 * inch, stroke=0, fill=1)
        c.setFillColor(HexColor("#FFFFFF"))
        c.setFont(self.tpl["font_bold"], self.tpl["title_size"])
        c.drawString(0, self.height - 0.35 * inch, self.name or "")
        if self.title:
            c.setFont(self.tpl["font_main"], 12)
            c.drawString(0, self.height - 0.55 * inch, self.title)
        if self.contact:
            c.setFont(self.tpl["font_main"], 9)
            c.drawString(0, self.height - 0.78 * inch, self.contact)


class SidebarHeader(Flowable):
    """Accent bar on the left of the name (creative template)."""

    def __init__(self, name: str, title: str, contact: str,
                 width: float, height: float, tpl: dict):
        super().__init__()
        self.name = name
        self.title = title
        self.contact = contact
        self.width = width
        self.height = height
        self.tpl = tpl

    def draw(self):
        c = self.canv
        c.setFillColor(HexColor(self.tpl["primary"]))
        c.rect(0, 0, 0.08 * inch, self.height, stroke=0, fill=1)
        c.setFillColor(HexColor(self.tpl["primary"]))
        c.setFont(self.tpl["font_bold"], self.tpl["title_size"])
        c.drawString(0.25 * inch, self.height - 0.35 * inch, self.name or "")
        if self.title:
            c.setFillColor(HexColor(self.tpl["secondary"]))
            c.setFont(self.tpl["font_main"], 12)
            c.drawString(0.25 * inch, self.height - 0.6 * inch, self.title)
        if self.contact:
            c.setFillColor(HexColor(self.tpl["muted"]))
            c.setFont(self.tpl["font_main"], 9)
            c.drawString(0.25 * inch, self.height - 0.85 * inch, self.contact)


# ---------------------------------------------------------------------------
# Style helpers
# ---------------------------------------------------------------------------

def _styles(tpl: dict) -> dict[str, ParagraphStyle]:
    return {
        "name": ParagraphStyle(
            "Name", fontName=tpl["font_bold"], fontSize=tpl["title_size"],
            textColor=HexColor(tpl["primary"]), spaceAfter=2, leading=tpl["title_size"] + 2,
        ),
        "title": ParagraphStyle(
            "Title", fontName=tpl["font_main"], fontSize=12,
            textColor=HexColor(tpl["secondary"]), spaceAfter=2,
        ),
        "contact": ParagraphStyle(
            "Contact", fontName=tpl["font_main"], fontSize=9,
            textColor=HexColor(tpl["muted"]), spaceAfter=10,
        ),
        "section": ParagraphStyle(
            "Section", fontName=tpl["font_bold"], fontSize=tpl["section_size"],
            textColor=HexColor(tpl["primary"]), spaceBefore=10, spaceAfter=4,
        ),
        "role": ParagraphStyle(
            "Role", fontName=tpl["font_bold"], fontSize=tpl["body_size"] + 1,
            textColor=HexColor("#000000"), spaceAfter=1,
        ),
        "company": ParagraphStyle(
            "Company", fontName=tpl["font_main"], fontSize=tpl["body_size"],
            textColor=HexColor(tpl["secondary"]), spaceAfter=2,
        ),
        "meta": ParagraphStyle(
            "Meta", fontName=tpl["font_main"], fontSize=9,
            textColor=HexColor(tpl["muted"]), spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "Body", fontName=tpl["font_main"], fontSize=tpl["body_size"],
            textColor=HexColor("#222222"), leading=tpl["body_size"] + 3, spaceAfter=2,
        ),
        "bullet": ParagraphStyle(
            "Bullet", fontName=tpl["font_main"], fontSize=tpl["body_size"],
            textColor=HexColor("#222222"), leading=tpl["body_size"] + 3,
            leftIndent=12, bulletIndent=2, spaceAfter=1,
        ),
    }


def _safe(s: Any) -> str:
    """Escape characters that ReportLab Paragraph treats as markup."""
    if s is None:
        return ""
    return (str(s)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;"))


def _contact_line(personal: dict) -> str:
    parts = [
        personal.get("email", ""),
        personal.get("phone", ""),
        personal.get("location", ""),
        personal.get("linkedin", ""),
        personal.get("github", ""),
        personal.get("website", ""),
    ]
    return "  •  ".join([_safe(p) for p in parts if p])


# ---------------------------------------------------------------------------
# Section builders
# ---------------------------------------------------------------------------

def _section_title(text: str, styles, tpl) -> list:
    out = [Paragraph(text.upper(), styles["section"])]
    out.append(HRFlowable(
        width="100%", thickness=0.6,
        color=HexColor(tpl["primary"]), spaceBefore=0, spaceAfter=4,
    ))
    return out


def _build_header(personal: dict, styles, tpl) -> list:
    name = _safe(personal.get("name") or "Your Name")
    title = _safe(personal.get("title") or "")
    contact = _contact_line(personal)

    style = tpl["header_style"]
    width = 7.0 * inch  # letter minus margins

    if style == "banner":
        return [HeaderBanner(name, title, contact, width, 1.0 * inch, tpl), Spacer(1, 12)]
    if style == "sidebar":
        return [SidebarHeader(name, title, contact, width, 1.0 * inch, tpl), Spacer(1, 12)]
    if style == "minimal":
        return [
            Paragraph(name, styles["name"]),
            Paragraph(title, styles["title"]) if title else Spacer(1, 0),
            Paragraph(contact, styles["contact"]),
            HRFlowable(width="100%", thickness=0.4, color=HexColor(tpl["muted"]), spaceAfter=8),
        ]
    # underline / classic
    return [
        Paragraph(name, styles["name"]),
        Paragraph(title, styles["title"]) if title else Spacer(1, 0),
        Paragraph(contact, styles["contact"]),
        HRFlowable(width="100%", thickness=1, color=HexColor(tpl["primary"]), spaceAfter=6),
    ]


def _build_summary(summary: str, styles, tpl) -> list:
    if not summary:
        return []
    out = _section_title("Summary", styles, tpl)
    out.append(Paragraph(_safe(summary), styles["body"]))
    return out


def _build_experience(experience: list[dict], styles, tpl) -> list:
    if not experience:
        return []
    out = _section_title("Experience", styles, tpl)
    for job in experience:
        block: list = []
        role = _safe(job.get("role", ""))
        company = _safe(job.get("company", ""))
        head = role
        if role and company:
            head = f"{role} <font color='{tpl['secondary']}'>· {company}</font>"
        elif company:
            head = company
        block.append(Paragraph(head, styles["role"]))

        meta_bits = []
        when = " – ".join([j for j in [job.get("start", ""), job.get("end", "")] if j])
        if when:
            meta_bits.append(when)
        if job.get("location"):
            meta_bits.append(_safe(job["location"]))
        if meta_bits:
            block.append(Paragraph("  ·  ".join(meta_bits), styles["meta"]))

        for b in job.get("bullets", []) or []:
            if not b:
                continue
            block.append(Paragraph(_safe(b), styles["bullet"], bulletText="•"))
        block.append(Spacer(1, 4))
        out.append(KeepTogether(block))
    return out


def _build_projects(projects: list[dict], styles, tpl) -> list:
    if not projects:
        return []
    out = _section_title("Projects", styles, tpl)
    for proj in projects:
        block: list = []
        name = _safe(proj.get("name", "")) or "Untitled"
        link = _safe(proj.get("link", ""))
        head = f"{name}" + (f" <font color='{tpl['muted']}'>({link})</font>" if link else "")
        block.append(Paragraph(head, styles["role"]))
        if proj.get("tech"):
            block.append(Paragraph(
                _safe(", ".join(proj["tech"])), styles["meta"],
            ))
        if proj.get("description"):
            block.append(Paragraph(_safe(proj["description"]), styles["body"]))
        for b in proj.get("bullets", []) or []:
            if not b:
                continue
            block.append(Paragraph(_safe(b), styles["bullet"], bulletText="•"))
        block.append(Spacer(1, 4))
        out.append(KeepTogether(block))
    return out


def _build_education(education: list[dict], styles, tpl) -> list:
    if not education:
        return []
    out = _section_title("Education", styles, tpl)
    for ed in education:
        block: list = []
        head = _safe(ed.get("school", ""))
        block.append(Paragraph(head, styles["role"]))
        line = " · ".join(
            _safe(p) for p in [
                ed.get("degree", ""),
                ed.get("field", ""),
                " – ".join([j for j in [ed.get("start", ""), ed.get("end", "")] if j]),
                f"GPA {ed['gpa']}" if ed.get("gpa") else "",
            ] if p
        )
        if line:
            block.append(Paragraph(line, styles["meta"]))
        if ed.get("details"):
            block.append(Paragraph(_safe(ed["details"]), styles["body"]))
        block.append(Spacer(1, 4))
        out.append(KeepTogether(block))
    return out


def _build_skills(skills: list[str], styles, tpl) -> list:
    if not skills:
        return []
    out = _section_title("Skills", styles, tpl)
    out.append(Paragraph(_safe(" · ".join(skills)), styles["body"]))
    return out


def _build_simple_section(title: str, items: list[dict], formatter,
                          styles, tpl) -> list:
    if not items:
        return []
    out = _section_title(title, styles, tpl)
    for it in items:
        line = formatter(it)
        if line:
            out.append(Paragraph(_safe(line), styles["body"]))
    return out


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def render_pdf(resume: dict, template_key: str = "modern") -> bytes:
    """Render a resume dict to a PDF byte stream."""
    tpl = get_template(template_key)
    styles = _styles(tpl)

    buf = io.BytesIO()
    doc = BaseDocTemplate(
        buf, pagesize=LETTER,
        leftMargin=0.7 * inch, rightMargin=0.7 * inch,
        topMargin=0.55 * inch, bottomMargin=0.55 * inch,
        title=resume.get("personal", {}).get("name", "Resume"),
    )
    frame = Frame(
        doc.leftMargin, doc.bottomMargin,
        doc.width, doc.height, id="main",
    )
    doc.addPageTemplates([PageTemplate(id="default", frames=[frame])])

    flowables: list = []
    flowables += _build_header(resume.get("personal", {}) or {}, styles, tpl)
    flowables += _build_summary(resume.get("summary", ""), styles, tpl)
    flowables += _build_experience(resume.get("experience", []) or [], styles, tpl)
    flowables += _build_projects(resume.get("projects", []) or [], styles, tpl)
    flowables += _build_education(resume.get("education", []) or [], styles, tpl)
    flowables += _build_skills(resume.get("skills", []) or [], styles, tpl)
    flowables += _build_simple_section(
        "Certifications", resume.get("certifications", []) or [],
        lambda c: " · ".join(p for p in [c.get("name"), c.get("issuer"), c.get("year")] if p),
        styles, tpl,
    )
    flowables += _build_simple_section(
        "Awards", resume.get("awards", []) or [],
        lambda a: " · ".join(p for p in [a.get("name"), a.get("year"), a.get("description")] if p),
        styles, tpl,
    )
    flowables += _build_simple_section(
        "Languages", resume.get("languages", []) or [],
        lambda l: f"{l.get('name','')}" + (f" ({l['level']})" if l.get("level") else ""),
        styles, tpl,
    )

    doc.build(flowables)
    return buf.getvalue()


def render_cover_letter_pdf(letter_text: str, name: str = "",
                            template_key: str = "modern") -> bytes:
    """Render plain cover-letter text to a PDF using the chosen template."""
    tpl = get_template(template_key)
    styles = _styles(tpl)

    buf = io.BytesIO()
    doc = BaseDocTemplate(
        buf, pagesize=LETTER,
        leftMargin=0.9 * inch, rightMargin=0.9 * inch,
        topMargin=0.9 * inch, bottomMargin=0.9 * inch,
        title=f"Cover Letter — {name}" if name else "Cover Letter",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
    doc.addPageTemplates([PageTemplate(id="default", frames=[frame])])

    flowables: list = []
    if name:
        flowables.append(Paragraph(_safe(name), styles["name"]))
        flowables.append(HRFlowable(
            width="100%", thickness=0.6,
            color=HexColor(tpl["primary"]), spaceAfter=10,
        ))

    for para in (letter_text or "").split("\n\n"):
        para = para.strip()
        if not para:
            continue
        flowables.append(Paragraph(_safe(para).replace("\n", "<br/>"), styles["body"]))
        flowables.append(Spacer(1, 8))

    doc.build(flowables)
    return buf.getvalue()
