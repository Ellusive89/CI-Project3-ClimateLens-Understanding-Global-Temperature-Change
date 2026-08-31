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


def build_country_comparison_chart(
    chart_data,
    rolling_window,
):
    """Build a multi-country temperature-anomaly chart."""
    colours = [
        "#4C78A8",
        "#F58518",
        "#54A24B",
        "#E45756",
        "#72B7B2",
        "#B279A2",
    ]

    dash_styles = [
        "solid",
        "dash",
        "dot",
        "dashdot",
        "longdash",
        "longdashdot",
    ]

    figure = go.Figure()

    countries = chart_data["country"].drop_duplicates()

    for index, country in enumerate(countries):
        country_data = chart_data.loc[
            chart_data["country"].eq(country)
        ].sort_values("year").copy()

        if rolling_window > 1:
            country_data["display_anomaly_c"] = (
                country_data["temperature_anomaly_c"]
                .rolling(
                    window=rolling_window,
                    min_periods=rolling_window,
                )
                .mean()
            )

            trace_name = (
                f"{country}: "
                f"{rolling_window}-year mean"
            )

        else:
            country_data["display_anomaly_c"] = (
                country_data["temperature_anomaly_c"]
            )

            trace_name = country

        figure.add_trace(
            go.Scatter(
                x=country_data["year"],
                y=country_data["display_anomaly_c"],
                name=trace_name,
                mode="lines",
                connectgaps=False,
                line={
                    "color": colours[index % len(colours)],
                    "dash": dash_styles[
                        index % len(dash_styles)
                    ],
                    "width": 2.3,
                },
                hovertemplate=(
                    f"Country/area: {country}<br>"
                    "Year: %{x}<br>"
                    "Anomaly: %{y:.2f} °C"
                    "<extra></extra>"
                ),
            )
        )

    figure.add_hline(
        y=0,
        line_color="#5E6F73",
        line_dash="dash",
        annotation_text="Country-specific 1951–1980 baseline",
    )

    figure.update_layout(
        height=540,
        autosize=True,
        xaxis_title="Year",
        yaxis_title="Country-specific anomaly (°C)",
        template="plotly_white",
        hovermode="x unified",
        legend={
            "title": "Country/area",
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "left",
            "x": 0,
        },
        margin={
            "l": 20,
            "r": 20,
            "t": 100,
            "b": 20,
        },
        font={
            "color": "#172D35",
        },
    )

    return figure


def build_country_change_bar_chart(ranking_data):
    """Build a horizontal chart of country-period changes."""
    chart_data = ranking_data.sort_values(
        "temperature_change_c",
        ascending=True,
    ).copy()

    figure = go.Figure()

    figure.add_trace(
        go.Bar(
            x=chart_data["temperature_change_c"],
            y=chart_data["country"],
            orientation="h",
            marker={
                "color": "#C45A28",
            },
            text=[
                f"{value:+.2f} °C"
                for value in chart_data[
                    "temperature_change_c"
                ]
            ],
            textposition="outside",
            cliponaxis=False,
            hovertemplate=(
                "Country/area: %{y}<br>"
                "1981–2010 minus 1951–1980: "
                "%{x:.3f} °C"
                "<extra></extra>"
            ),
        )
    )

    figure.add_vline(
        x=0,
        line_color="#5E6F73",
        line_dash="dash",
    )

    figure.update_layout(
        height=max(520, len(chart_data) * 34),
        autosize=True,
        xaxis_title=(
            "Difference between period averages (°C)"
        ),
        yaxis_title="Country/area",
        template="plotly_white",
        showlegend=False,
        margin={
            "l": 20,
            "r": 90,
            "t": 20,
            "b": 20,
        },
        font={
            "color": "#172D35",
        },
    )

    return figure


def build_hypothesis_box_chart(
    chart_data,
    value_column,
    y_axis_label,
    period_order,
    colour_map,
    show_all_points=False,
):
    """Build a period-comparison box plot."""
    figure = go.Figure()

    point_setting = (
        "all"
        if show_all_points
        else "outliers"
    )

    for period in period_order:
        period_data = chart_data.loc[
            chart_data["period"].eq(period),
            value_column,
        ]

        figure.add_trace(
            go.Box(
                y=period_data,
                name=period,
                boxpoints=point_setting,
                jitter=0.3,
                pointpos=0,
                fillcolor=colour_map[period],
                line={
                    "color": colour_map[period],
                    "width": 2,
                },
                marker={
                    "color": colour_map[period],
                    "opacity": 0.65,
                },
                hovertemplate=(
                    f"Period: {period}<br>"
                    "Value: %{y:.3f} °C"
                    "<extra></extra>"
                ),
            )
        )

    figure.update_layout(
        height=520,
        autosize=True,
        xaxis_title="Comparison period",
        yaxis_title=y_axis_label,
        template="plotly_white",
        showlegend=False,
        margin={
            "l": 20,
            "r": 20,
            "t": 30,
            "b": 20,
        },
        font={
            "color": "#172D35",
        },
    )

    return figure
