"""Resume template metadata.

Each template defines colours, font choices, and a layout key consumed by
``core.pdf_generator``. Templates intentionally keep ATS-friendly single-
column layouts (no tables, no graphics behind text).
"""

TEMPLATES = {
    "modern": {
        "name": "Modern",
        "description": "Clean, blue accent header with bold section titles.",
        "primary": "#1F4E79",
        "secondary": "#2E75B6",
        "muted": "#6B6B6B",
        "font_main": "Helvetica",
        "font_bold": "Helvetica-Bold",
        "title_size": 22,
        "section_size": 12,
        "body_size": 10,
        "header_style": "banner",     # full-width coloured band behind name
    },
    "classic": {
        "name": "Classic",
        "description": "Traditional, serif, conservative layout for legal/finance/academia.",
        "primary": "#000000",
        "secondary": "#444444",
        "muted": "#777777",
        "font_main": "Times-Roman",
        "font_bold": "Times-Bold",
        "title_size": 20,
        "section_size": 12,
        "body_size": 10,
        "header_style": "underline",  # name + horizontal rule
    },
    "minimal": {
        "name": "Minimal",
        "description": "Lots of whitespace, thin rules, perfect for designers/PMs.",
        "primary": "#111111",
        "secondary": "#333333",
        "muted": "#888888",
        "font_main": "Helvetica",
        "font_bold": "Helvetica-Bold",
        "title_size": 24,
        "section_size": 11,
        "body_size": 10,
        "header_style": "minimal",    # name only, generous spacing
    },
    "creative": {
        "name": "Creative",
        "description": "Magenta accents, slightly larger headings — for design and marketing.",
        "primary": "#B83280",
        "secondary": "#D53F8C",
        "muted": "#666666",
        "font_main": "Helvetica",
        "font_bold": "Helvetica-Bold",
        "title_size": 24,
        "section_size": 13,
        "body_size": 10,
        "header_style": "sidebar",    # accent bar on the left of the name
    },
}


def list_templates() -> list[dict]:
    return [{"key": k, **v} for k, v in TEMPLATES.items()]


def get_template(key: str) -> dict:
    return TEMPLATES.get(key, TEMPLATES["modern"])
