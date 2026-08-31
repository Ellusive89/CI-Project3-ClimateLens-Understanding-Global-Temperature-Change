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

def build_global_temperature_chart(
    chart_data,
    value_column,
    value_label,
    rolling_window,
):
    """Build an interactive annual global-temperature chart."""
    data = chart_data.sort_values("year").copy()

    data["rolling_value"] = (
        data[value_column]
        .rolling(
            window=rolling_window,
            min_periods=rolling_window,
        )
        .mean()
    )

    figure = go.Figure()

    figure.add_trace(
        go.Scatter(
            x=data["year"],
            y=data[value_column],
            name="Annual value",
            mode="lines",
            line={
                "color": "#4C78A8",
                "width": 1.5,
            },
            hovertemplate=(
                "Year: %{x}<br>"
                f"{value_label}: "
                "%{y:.2f} °C"
                "<extra></extra>"
            ),
        )
    )

    if rolling_window > 1:
        figure.add_trace(
            go.Scatter(
                x=data["year"],
                y=data["rolling_value"],
                name=f"{rolling_window}-year rolling mean",
                mode="lines",
                line={
                    "color": "#C45A28",
                    "width": 3,
                },
                hovertemplate=(
                    "Year: %{x}<br>"
                    f"{rolling_window}-year mean: "
                    "%{y:.2f} °C"
                    "<extra></extra>"
                ),
            )
        )

    if value_column == "land_ocean_anomaly_c":
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
        yaxis_title=f"{value_label} (°C)",
        template="plotly_white",
        hovermode="x unified",
        legend={
            "title": "Series",
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "left",
            "x": 0,
        },
        margin={
            "l": 20,
            "r": 20,
            "t": 60,
            "b": 20,
        },
        font={
            "color": "#172D35",
        },
    )

    return figure


def build_global_uncertainty_chart(global_annual):
    """Build the historical measurement-uncertainty chart."""
    data = global_annual.loc[
        global_annual["land_months"].eq(12)
    ].copy()

    data = data.sort_values("year")

    figure = go.Figure()

    figure.add_trace(
        go.Scatter(
            x=data["year"],
            y=data["land_average_uncertainty_c"],
            name="Average reported uncertainty",
            mode="lines",
            line={
                "color": "#6F4E7C",
                "width": 2,
            },
            hovertemplate=(
                "Year: %{x}<br>"
                "Average uncertainty: %{y:.3f} °C"
                "<extra></extra>"
            ),
        )
    )

    figure.add_vrect(
        x0=1753,
        x1=1899,
        fillcolor="#F2CF5B",
        opacity=0.18,
        line_width=0,
        annotation_text="Before 1900",
        annotation_position="top left",
    )

    figure.add_vrect(
        x0=1950,
        x1=2015,
        fillcolor="#4C78A8",
        opacity=0.10,
        line_width=0,
        annotation_text="1950 onward",
        annotation_position="top right",
    )

    figure.update_layout(
        height=520,
        autosize=True,
        xaxis_title="Year",
        yaxis_title="Average reported uncertainty (°C)",
        template="plotly_white",
        hovermode="x unified",
        showlegend=False,
        margin={
            "l": 20,
            "r": 20,
            "t": 50,
            "b": 20,
        },
        font={
            "color": "#172D35",
        },
    )

    return figure
