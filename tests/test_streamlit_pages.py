"""Smoke tests for the ClimateLens Streamlit application."""

from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest


PROJECT_ROOT = Path(__file__).resolve().parents[1]

STREAMLIT_FILES = [
    "app.py",
    "views/overview.py",
    "views/global_trends.py",
    "views/country_explorer.py",
    "views/hypotheses.py",
    "views/model_performance.py",
    "views/ethics_governance.py",
]


@pytest.mark.parametrize(
    "relative_path",
    STREAMLIT_FILES,
)
def test_streamlit_script_runs_without_exception(
    relative_path,
):
    """Each application script should complete without errors."""
    script_path = PROJECT_ROOT / relative_path

    app_test = AppTest.from_file(
        str(script_path),
        default_timeout=30,
    )

    app_test.run()

    assert len(app_test.exception) == 0
