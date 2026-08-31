"""Reusable Plotly chart functions for ClimateLens."""

import plotly.graph_objects as go


def build_global_anomaly_chart(global_annual):
    """Build an accessible global temperature-anomaly line chart."""
    chart_data = global_annual.loc[
        global_annual["land_ocean_months"].eq(12)
    ].copy()

    chart_data = chart_data.sort_values("year")

    chart_data["rolling_10_year_anomaly_c"] = (
        chart_data["land_ocean_anomaly_c"]
        .rolling(window=10, min_periods=10)
        .mean()
    )

    figure = go.Figure()

    figure.add_trace(
        go.Scatter(
            x=chart_data["year"],
            y=chart_data["land_ocean_anomaly_c"],
            name="Annual anomaly",
            mode="lines",
            line={
                "color": "#4C78A8",
                "width": 1.4,
            },
            hovertemplate=(
                "Year: %{x}<br>"
                "Anomaly: %{y:.2f} °C"
                "<extra></extra>"
            ),
        )
    )

    figure.add_trace(
        go.Scatter(
            x=chart_data["year"],
            y=chart_data["rolling_10_year_anomaly_c"],
            name="10-year rolling mean",
            mode="lines",
            line={
                "color": "#C45A28",
                "width": 3,
            },
            hovertemplate=(
                "Year: %{x}<br>"
                "Rolling anomaly: %{y:.2f} °C"
                "<extra></extra>"
            ),
        )
    )

    figure.add_hline(
        y=0,
        line_color="#5E6F73",
        line_dash="dash",
        annotation_text="1951–1980 baseline",
    )

    figure.update_layout(
        height=520,
        autosize=True,
        xaxis_title="Year",
        yaxis_title="Temperature anomaly (°C)",
        template="plotly_white",
        hovermode="x unified",
        legend_title="Measurement",
        margin={
            "l": 20,
            "r": 20,
            "t": 20,
            "b": 20,
        },
        font={
            "color": "#172D35",
        },
    )

    return figure
