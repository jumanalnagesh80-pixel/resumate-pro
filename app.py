"""AI Resume Builder — Streamlit entry point."""

from __future__ import annotations

import os
import sys

import streamlit as st

# Make the app importable when run via `streamlit run app.py` from any cwd.
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from ui.styles import CSS
from ui import pages


PAGES = {
    "🏠 Dashboard":      pages.page_dashboard,
    "🛠 Builder":         pages.page_builder,
    "✨ AI Enhance":      pages.page_enhance,
    "📊 ATS Score":      pages.page_ats,
    "🎯 Job Match":      pages.page_match,
    "🎨 Templates":      pages.page_templates,
    "📝 Cover Letter":   pages.page_cover_letter,
    "📥 Import":         pages.page_import,
    "📤 Export":         pages.page_export,
}


def main() -> None:
    st.set_page_config(
        page_title="AI Resume Builder",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(CSS, unsafe_allow_html=True)

    st.sidebar.title("AI Resume Builder")
    st.sidebar.caption("Advanced prototype")
    choice = st.sidebar.radio(" ", list(PAGES.keys()), label_visibility="collapsed")

    st.sidebar.markdown("---")
    st.sidebar.checkbox(
        "Use OpenAI (if API key set)",
        value=st.session_state.get("use_ai", True),
        key="use_ai",
        help="Falls back to the local engine when the key is missing or AI is disabled.",
    )
    has_key = bool(os.environ.get("OPENAI_API_KEY"))
    st.sidebar.caption(
        ("🟢 OpenAI key detected" if has_key else "⚪ No OpenAI key — using local engine")
    )

    st.sidebar.markdown("---")
    if st.sidebar.button("Load sample resume"):
        import json
        from utils.helpers import empty_resume
        sample_path = os.path.join(HERE, "samples", "sample_resume.json")
        if os.path.exists(sample_path):
            with open(sample_path) as f:
                data = json.load(f)
            base = empty_resume()
            base.update({k: data[k] for k in base if k in data})
            st.session_state.resume = base
            st.sidebar.success("Sample loaded.")
            st.rerun()
    if st.sidebar.button("Reset resume"):
        from utils.helpers import empty_resume
        st.session_state.resume = empty_resume()
        st.sidebar.success("Cleared.")
        st.rerun()

    st.sidebar.markdown(
        "<div class='kr-foot'>Built with Streamlit, ReportLab, scikit-learn, Plotly.</div>",
        unsafe_allow_html=True,
    )

    PAGES[choice]()


if __name__ == "__main__":
    main()
