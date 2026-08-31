"""Main entry point for the ClimateLens Streamlit dashboard."""

import streamlit as st

from src.ui import load_css


st.set_page_config(
    page_title="ClimateLens",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_css()

pages = {
    "Explore": [
        st.Page(
            "views/overview.py",
            title="Overview",
            icon="🏠",
            default=True,
        ),
        st.Page(
            "views/global_trends.py",
            title="Global Trends",
            icon="📈",
        ),
        st.Page(
            "views/country_explorer.py",
            title="Country Explorer",
            icon="🌐",
        ),
    ],
    "Evidence": [
        st.Page(
            "views/hypotheses.py",
            title="Hypotheses",
            icon="📋",
        ),
    ],
}

navigation = st.navigation(
    pages,
    position="sidebar",
    expanded=True,
)

navigation.run()
