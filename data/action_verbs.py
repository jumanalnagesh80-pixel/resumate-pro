"""Power-verb library used by the AI engine to rewrite weak bullet points.

Verbs are grouped by impact category so we can pick a contextually
appropriate replacement for whatever weak verb the user wrote.
"""

ACTION_VERBS = {
    "leadership": [
        "Led", "Directed", "Spearheaded", "Orchestrated", "Championed",
        "Mentored", "Coached", "Mobilized", "Galvanized", "Pioneered",
        "Headed", "Chaired", "Guided", "Supervised", "Coordinated",
    ],
    "achievement": [
        "Achieved", "Delivered", "Exceeded", "Surpassed", "Attained",
        "Accomplished", "Secured", "Earned", "Won", "Outperformed",
    ],
    "improvement": [
        "Optimized", "Streamlined", "Enhanced", "Improved", "Refined",
        "Accelerated", "Boosted", "Elevated", "Upgraded", "Revamped",
        "Transformed", "Modernized", "Overhauled",
    ],
    "creation": [
        "Built", "Designed", "Architected", "Engineered", "Developed",
        "Created", "Established", "Founded", "Launched", "Initiated",
        "Implemented", "Deployed", "Pioneered", "Formulated", "Devised",
    ],
    "analysis": [
        "Analyzed", "Evaluated", "Investigated", "Researched", "Audited",
        "Assessed", "Diagnosed", "Examined", "Identified", "Quantified",
        "Forecasted", "Modeled", "Benchmarked",
    ],
    "communication": [
        "Presented", "Communicated", "Negotiated", "Persuaded", "Authored",
        "Published", "Briefed", "Influenced", "Facilitated", "Articulated",
    ],
    "management": [
        "Managed", "Oversaw", "Administered", "Executed", "Monitored",
        "Controlled", "Governed", "Operated", "Maintained", "Owned",
    ],
    "collaboration": [
        "Collaborated", "Partnered", "Liaised", "Aligned", "Unified",
        "Engaged", "Integrated", "Consulted", "Cross-functionally led",
    ],
    "growth": [
        "Scaled", "Grew", "Expanded", "Increased", "Generated",
        "Drove", "Doubled", "Tripled", "Multiplied", "Cultivated",
    ],
    "reduction": [
        "Reduced", "Cut", "Decreased", "Minimized", "Eliminated",
        "Consolidated", "Saved", "Slashed", "Trimmed",
    ],
}

# Words that signal a bullet point is weak and needs rewriting.
WEAK_VERBS = {
    "did", "made", "got", "helped", "worked on", "worked", "responsible for",
    "was responsible", "in charge of", "duties included", "tasked with",
    "handled", "dealt with", "took care of", "involved in", "participated",
    "assisted", "supported", "wrote", "used", "had", "have",
}

# Mapping of weak phrases to a recommended impact category.
WEAK_TO_CATEGORY = {
    "responsible for": "management",
    "in charge of": "leadership",
    "duties included": "management",
    "helped": "collaboration",
    "assisted": "collaboration",
    "supported": "collaboration",
    "worked on": "creation",
    "worked": "creation",
    "did": "achievement",
    "made": "creation",
    "got": "achievement",
    "handled": "management",
    "dealt with": "management",
    "took care of": "management",
    "involved in": "collaboration",
    "participated": "collaboration",
    "tasked with": "management",
    "wrote": "creation",
    "used": "creation",
}


def all_verbs():
    """Flat list of every action verb (used for spell/strength checks)."""
    flat = []
    for verbs in ACTION_VERBS.values():
        flat.extend(v.lower() for v in verbs)
    return flat


def pick_verb(category: str, seed: int = 0) -> str:
    """Pick a deterministic verb from a category."""
    verbs = ACTION_VERBS.get(category, ACTION_VERBS["creation"])
    return verbs[seed % len(verbs)]
