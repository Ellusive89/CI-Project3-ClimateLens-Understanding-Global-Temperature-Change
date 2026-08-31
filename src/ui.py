"""Reusable user-interface helpers for ClimateLens."""

from html import escape
from pathlib import Path

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
STYLE_FILE = PROJECT_ROOT / "assets" / "style.css"


def load_css():
    """Load the dashboard's shared CSS file."""
    if not STYLE_FILE.exists():
        st.warning(
            "The shared style file could not be found."
        )
        return

    css_content = STYLE_FILE.read_text(encoding="utf-8")

    st.markdown(
        f"<style>{css_content}</style>",
        unsafe_allow_html=True,
    )


def render_page_header(eyebrow, title, introduction):
    """Render an accessible page hero using escaped static text."""
    safe_eyebrow = escape(eyebrow)
    safe_title = escape(title)
    safe_introduction = escape(introduction)

    st.markdown(
        f"""
        <section class="hero">
            <p class="hero__eyebrow">{safe_eyebrow}</p>
            <h1>{safe_title}</h1>
            <p class="hero__intro">{safe_introduction}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_footer():
    """Render the dashboard footer."""
    st.markdown(
        """
        <footer class="dashboard-footer">
            ClimateLens is an educational analytics project.
            Its historical findings and model outputs should not be
            interpreted as current climate monitoring or professional
            climate projections.
        </footer>
        """,
        unsafe_allow_html=True,
    )
