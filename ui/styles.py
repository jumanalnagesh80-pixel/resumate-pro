"""Streamlit custom CSS."""

CSS = """
<style>
.main .block-container {max-width: 1100px; padding-top: 1.2rem;}

/* Hero */
.kr-hero {
    background: linear-gradient(135deg, #1F4E79 0%, #2E75B6 100%);
    color: #ffffff;
    padding: 1.6rem 1.8rem;
    border-radius: 14px;
    margin-bottom: 1.2rem;
    box-shadow: 0 8px 24px rgba(31, 78, 121, 0.18);
}
.kr-hero h1 {color: #fff; margin: 0 0 .25rem 0;}
.kr-hero p {color: #e6f1ff; margin: 0;}

/* Cards */
.kr-card {
    background: #ffffff;
    border: 1px solid #e6e9ef;
    border-radius: 12px;
    padding: 1rem 1.1rem;
    margin-bottom: 0.8rem;
    box-shadow: 0 1px 3px rgba(15,23,42,.04);
}
.kr-card h4 {margin-top: 0;}

/* Score chip */
.kr-chip {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 999px;
    font-weight: 600;
    font-size: .85rem;
    margin-right: 6px;
    margin-bottom: 4px;
}
.kr-chip-good {background: #dcfce7; color: #166534;}
.kr-chip-warn {background: #fef9c3; color: #854d0e;}
.kr-chip-bad  {background: #fee2e2; color: #991b1b;}
.kr-chip-info {background: #e0e7ff; color: #3730a3;}

/* Bullet diff */
.kr-old {color: #991b1b; text-decoration: line-through; opacity: .85;}
.kr-new {color: #166534; font-weight: 600;}

/* Section heading */
.kr-section {
    border-left: 4px solid #2E75B6;
    padding-left: 12px;
    margin: 1.2rem 0 .6rem;
}
.kr-section h3 {margin: 0; color: #1F4E79;}

/* Templates grid */
.kr-template {
    border: 2px solid #e6e9ef;
    border-radius: 12px;
    padding: 14px;
    text-align: left;
    transition: all .2s;
}
.kr-template.selected {border-color: #2E75B6; background: #f0f7ff;}
.kr-template h5 {margin: 0 0 6px 0;}
.kr-template .swatch {
    display: inline-block; width: 16px; height: 16px;
    border-radius: 4px; margin-right: 4px; vertical-align: middle;
}

/* Footer note */
.kr-foot {color: #64748b; font-size: .85rem; margin-top: 2rem;}
</style>
"""
