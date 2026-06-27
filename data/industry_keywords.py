"""Industry-specific keyword lists used to enrich ATS scoring and AI rewriting."""

INDUSTRY_KEYWORDS = {
    "software_engineering": [
        "scalable", "distributed systems", "microservices", "REST API", "GraphQL",
        "CI/CD", "unit tests", "code review", "architecture", "performance",
        "latency", "throughput", "high availability", "fault tolerance",
        "design patterns", "object-oriented", "functional programming",
        "concurrency", "multithreading", "system design",
    ],
    "data_science": [
        "predictive modeling", "feature engineering", "model evaluation",
        "hyperparameter tuning", "A/B testing", "statistical analysis",
        "data pipeline", "data wrangling", "dashboard", "insights",
        "regression", "classification", "clustering", "neural network",
        "training data", "validation set", "ROC AUC", "F1 score",
    ],
    "product_management": [
        "roadmap", "user research", "product-market fit", "stakeholder",
        "KPIs", "OKRs", "go-to-market", "user stories", "MVP", "iteration",
        "prioritization", "competitive analysis", "metrics", "retention",
        "activation", "conversion", "growth", "personas",
    ],
    "marketing": [
        "campaign", "SEO", "SEM", "content marketing", "lead generation",
        "conversion rate", "CTR", "CPA", "LTV", "ROAS", "brand awareness",
        "engagement", "social media", "analytics", "segmentation",
        "marketing funnel", "email marketing", "growth hacking",
    ],
    "finance": [
        "financial modeling", "valuation", "DCF", "forecasting", "budgeting",
        "variance analysis", "P&L", "balance sheet", "cash flow", "GAAP",
        "IFRS", "audit", "compliance", "risk management", "due diligence",
        "M&A", "equity research", "portfolio", "hedge",
    ],
    "design": [
        "user research", "wireframing", "prototyping", "usability testing",
        "design system", "accessibility", "responsive design", "user flows",
        "information architecture", "interaction design", "visual design",
        "design thinking", "Figma", "Sketch", "personas", "journey map",
    ],
    "sales": [
        "quota", "pipeline", "lead qualification", "discovery call", "demo",
        "negotiation", "closing", "account management", "upsell", "cross-sell",
        "CRM", "Salesforce", "outbound", "inbound", "MEDDIC", "BANT",
        "enterprise", "SaaS sales",
    ],
}


def detect_industry(text: str) -> str:
    """Return the most likely industry tag for a piece of text."""
    if not text:
        return "software_engineering"
    lowered = text.lower()
    scores = {
        industry: sum(1 for kw in keywords if kw.lower() in lowered)
        for industry, keywords in INDUSTRY_KEYWORDS.items()
    }
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "software_engineering"


def keywords_for(industry: str) -> list[str]:
    return INDUSTRY_KEYWORDS.get(industry, INDUSTRY_KEYWORDS["software_engineering"])
