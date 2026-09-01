"""Automated validation tests for ClimateLens processed data."""

import numpy as np
import pandas as pd
import pytest

from src.data_loader import (
    _validate_columns,
    load_country_annual,
    load_global_annual,
    load_hypothesis_results,
    load_model_coefficients,
    load_model_cross_validation,
    load_model_metrics,
    load_model_predictions,
)


def test_validate_columns_rejects_missing_fields():
    """The schema validator should report unavailable columns."""
    test_data = pd.DataFrame(
        {
            "available_column": [1, 2, 3],
        }
    )

    with pytest.raises(
        ValueError,
        match="Test dataset is missing required columns",
    ):
        _validate_columns(
            test_data,
            [
                "available_column",
                "missing_column",
            ],
            "Test dataset",
        )


def test_global_annual_summary():
    """Validate the Version 1 global annual dataset."""
    global_annual = load_global_annual()

    assert len(global_annual) == 266
    assert global_annual["year"].min() == 1750
    assert global_annual["year"].max() == 2015
    assert global_annual["year"].is_unique
    assert global_annual["year"].is_monotonic_increasing

    assert global_annual[
        "land_average_temperature_c"
    ].notna().all()

    assert global_annual[
        "land_average_uncertainty_c"
    ].notna().all()

    assert global_annual["land_months"].between(
        1,
        12,
    ).all()

    assert global_annual["land_ocean_months"].between(
        0,
        12,
    ).all()


def test_country_annual_summary():
    """Validate complete Version 1 country-year summaries."""
    country_annual = load_country_annual()

    assert len(country_annual) == 44_330
    assert country_annual["country"].nunique() == 242
    assert country_annual["year"].min() == 1753
    assert country_annual["year"].max() == 2012

    assert country_annual[
        "months_observed"
    ].eq(12).all()

    assert country_annual[
        "average_temperature_c"
    ].notna().all()

    assert not country_annual.duplicated(
        subset=["country", "year"]
    ).any()

    assert "Antarctica" not in set(
        country_annual["country"]
    )


def test_hypothesis_results():
    """Validate the two saved statistical conclusions."""
    hypothesis_results = load_hypothesis_results()

    assert len(hypothesis_results) == 2

    assert set(
        hypothesis_results["hypothesis"]
    ) == {"H1", "H2"}

    assert hypothesis_results[
        "conclusion"
    ].eq("Supported").all()

    assert hypothesis_results[
        "two_sided_p_value"
    ].lt(0.05).all()

    assert hypothesis_results[
        "cohens_d"
    ].gt(0).all()


def test_model_metrics_and_benchmark():
    """Confirm that the model beats the saved benchmark."""
    model_metrics = load_model_metrics()

    assert set(model_metrics["model"]) == {
        "Linear regression",
        "Seasonal-naive baseline",
    }

    assert model_metrics[
        ["mae_c", "rmse_c", "r2"]
    ].notna().all().all()

    model_row = model_metrics.loc[
        model_metrics["model"].eq(
            "Linear regression"
        )
    ].iloc[0]

    baseline_row = model_metrics.loc[
        model_metrics["model"].eq(
            "Seasonal-naive baseline"
        )
    ].iloc[0]

    assert model_row["mae_c"] < baseline_row["mae_c"]
    assert model_row["rmse_c"] < baseline_row["rmse_c"]
    assert model_row["r2"] > baseline_row["r2"]


def test_model_predictions():
    """Validate the chronological held-out predictions."""
    predictions = load_model_predictions()

    assert len(predictions) == 120
    assert predictions["date"].min() == pd.Timestamp(
        "2006-01-01"
    )
    assert predictions["date"].max() == pd.Timestamp(
        "2015-12-01"
    )
    assert predictions["date"].is_monotonic_increasing
    assert predictions["date"].is_unique

    required_values = [
        "actual_temperature_c",
        "predicted_temperature_c",
        "seasonal_naive_temperature_c",
        "residual_c",
        "absolute_error_c",
    ]

    assert predictions[
        required_values
    ].notna().all().all()

    assert np.allclose(
        predictions["absolute_error_c"],
        predictions["residual_c"].abs(),
    )


def test_cross_validation_results():
    """Validate the expanding-window evaluation results."""
    cross_validation = load_model_cross_validation()

    assert len(cross_validation) == 5

    assert cross_validation[
        "fold"
    ].tolist() == [1, 2, 3, 4, 5]

    assert cross_validation[
        ["mae_c", "rmse_c", "r2"]
    ].notna().all().all()

    assert cross_validation["mae_c"].gt(0).all()
    assert cross_validation["rmse_c"].gt(0).all()


def test_standardised_coefficients():
    """Validate the saved linear-model coefficients."""
    coefficients = load_model_coefficients()

    assert len(coefficients) == 7
    assert coefficients["feature"].is_unique

    assert coefficients[
        [
            "standardised_coefficient",
            "absolute_coefficient",
        ]
    ].notna().all().all()

    assert np.allclose(
        coefficients["absolute_coefficient"],
        coefficients[
            "standardised_coefficient"
        ].abs(),
    )
