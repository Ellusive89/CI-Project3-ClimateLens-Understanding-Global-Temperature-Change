"""Tests for reusable ClimateLens Plotly charts."""

import pandas as pd
import plotly.graph_objects as go

from src.charts import (
    build_coefficient_chart,
    build_country_change_bar_chart,
    build_country_comparison_chart,
    build_cross_validation_chart,
    build_global_anomaly_chart,
    build_global_temperature_chart,
    build_global_uncertainty_chart,
    build_hypothesis_box_chart,
    build_model_metric_chart,
    build_model_prediction_chart,
    build_residual_histogram,
)
from src.data_loader import (
    load_country_annual,
    load_global_annual,
    load_model_coefficients,
    load_model_cross_validation,
    load_model_metrics,
    load_model_predictions,
)


def assert_valid_figure(figure):
    """Check shared properties expected from dashboard charts."""
    assert isinstance(figure, go.Figure)
    assert len(figure.data) > 0
    assert figure.layout.height >= 520
    assert figure.layout.xaxis.title.text
    assert figure.layout.yaxis.title.text


def test_global_charts():
    """Global chart functions should return populated figures."""
    global_annual = load_global_annual()

    anomaly_figure = build_global_anomaly_chart(
        global_annual
    )

    temperature_figure = build_global_temperature_chart(
        chart_data=global_annual,
        value_column="land_average_temperature_c",
        value_label="Land-average temperature",
        rolling_window=10,
    )

    uncertainty_figure = build_global_uncertainty_chart(
        global_annual
    )

    assert_valid_figure(anomaly_figure)
    assert_valid_figure(temperature_figure)
    assert_valid_figure(uncertainty_figure)

    assert len(anomaly_figure.data) == 2
    assert len(temperature_figure.data) == 2
    assert len(uncertainty_figure.data) == 1


def test_country_charts():
    """Country comparison functions should create valid figures."""
    country_annual = load_country_annual()

    selected_data = country_annual.loc[
        country_annual["country"].isin(
            ["Sweden", "United Kingdom"]
        )
        & country_annual["year"].between(1950, 2012)
    ].copy()

    comparison_figure = build_country_comparison_chart(
        chart_data=selected_data,
        rolling_window=10,
    )

    ranking_data = pd.DataFrame(
        {
            "country": [
                "Example A",
                "Example B",
                "Example C",
            ],
            "temperature_change_c": [
                0.45,
                0.62,
                0.31,
            ],
        }
    )

    ranking_figure = build_country_change_bar_chart(
        ranking_data
    )

    assert_valid_figure(comparison_figure)
    assert_valid_figure(ranking_figure)

    assert len(comparison_figure.data) == 2
    assert len(ranking_figure.data) == 1
    assert ranking_figure.data[0].orientation == "h"


def test_hypothesis_box_chart():
    """Hypothesis periods should appear as separate box traces."""
    hypothesis_data = pd.DataFrame(
        {
            "period": [
                "Earlier",
                "Earlier",
                "Later",
                "Later",
            ],
            "temperature_c": [
                14.9,
                15.1,
                15.5,
                15.7,
            ],
        }
    )

    figure = build_hypothesis_box_chart(
        chart_data=hypothesis_data,
        value_column="temperature_c",
        y_axis_label="Temperature (°C)",
        period_order=["Earlier", "Later"],
        colour_map={
            "Earlier": "#4C78A8",
            "Later": "#C45A28",
        },
    )

    assert_valid_figure(figure)
    assert len(figure.data) == 2
    assert all(
        trace.type == "box"
        for trace in figure.data
    )


def test_model_charts():
    """Model chart functions should return populated figures."""
    predictions = load_model_predictions()
    metrics = load_model_metrics()
    cross_validation = load_model_cross_validation()
    coefficients = load_model_coefficients()

    prediction_figure = build_model_prediction_chart(
        prediction_data=predictions,
        selected_series=[
            "Observed",
            "Linear regression",
            "Seasonal-naive baseline",
        ],
    )

    metric_figure = build_model_metric_chart(metrics)

    residual_figure = build_residual_histogram(
        predictions
    )

    validation_figure = build_cross_validation_chart(
        cross_validation
    )

    coefficient_figure = build_coefficient_chart(
        coefficients
    )

    figures = [
        prediction_figure,
        metric_figure,
        residual_figure,
        validation_figure,
        coefficient_figure,
    ]

    for figure in figures:
        assert_valid_figure(figure)

    assert len(prediction_figure.data) == 3
    assert len(metric_figure.data) == 2
    assert len(residual_figure.data) == 1
    assert len(validation_figure.data) == 2
    assert len(coefficient_figure.data) == 1
