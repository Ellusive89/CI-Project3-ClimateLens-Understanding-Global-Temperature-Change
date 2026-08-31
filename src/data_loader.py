"""Cached data-loading functions for the ClimateLens dashboard."""

from pathlib import Path

import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FOLDER = PROJECT_ROOT / "data" / "processed" / "v1"


def _validate_columns(dataframe, required_columns, dataset_name):
    """Raise a helpful error when required columns are unavailable."""
    missing_columns = set(required_columns).difference(
        dataframe.columns
    )

    if missing_columns:
        raise ValueError(
            f"{dataset_name} is missing required columns: "
            f"{sorted(missing_columns)}"
        )


@st.cache_data(show_spinner=False)
def load_global_annual():
    """Load annual global temperature summaries."""
    file_path = DATA_FOLDER / "global_annual_summary.csv"

    if not file_path.exists():
        raise FileNotFoundError(
            f"Required file was not found: {file_path}"
        )

    dataframe = pd.read_csv(file_path)

    _validate_columns(
        dataframe,
        [
            "year",
            "land_ocean_average_temperature_c",
            "land_ocean_anomaly_c",
            "land_ocean_months",
        ],
        "Global annual summary",
    )

    return dataframe


@st.cache_data(show_spinner=False)
def load_country_annual():
    """Load complete country-year temperature summaries."""
    file_path = DATA_FOLDER / "country_annual_summary.csv"

    if not file_path.exists():
        raise FileNotFoundError(
            f"Required file was not found: {file_path}"
        )

    dataframe = pd.read_csv(file_path)

    _validate_columns(
        dataframe,
        [
            "country",
            "year",
            "average_temperature_c",
            "average_uncertainty_c",
            "months_observed",
            "baseline_temperature_c",
            "baseline_years",
            "temperature_anomaly_c",
        ],
        "Country annual summary",
    )

    return dataframe


@st.cache_data(show_spinner=False)
def load_hypothesis_results():
    """Load the project hypothesis results."""
    file_path = DATA_FOLDER / "hypothesis_results.csv"

    if not file_path.exists():
        raise FileNotFoundError(
            f"Required file was not found: {file_path}"
        )

    dataframe = pd.read_csv(file_path)

    _validate_columns(
        dataframe,
        [
            "hypothesis",
            "conclusion",
        ],
        "Hypothesis results",
    )

    return dataframe


@st.cache_data(show_spinner=False)
def load_model_metrics():
    """Load predictive-model evaluation metrics."""
    file_path = DATA_FOLDER / "model_metrics.csv"

    if not file_path.exists():
        raise FileNotFoundError(
            f"Required file was not found: {file_path}"
        )

    dataframe = pd.read_csv(file_path)

    _validate_columns(
        dataframe,
        [
            "model",
            "mae_c",
            "rmse_c",
            "r2",
        ],
        "Model metrics",
    )

    return dataframe
