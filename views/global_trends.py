"""Interactive Global Trends page for ClimateLens."""

import streamlit as st

from src.charts import (
    build_global_temperature_chart,
    build_global_uncertainty_chart,
)
from src.data_loader import load_global_annual
from src.ui import (
    render_footer,
    render_page_header,
)


render_page_header(
    eyebrow="Global analysis",
    title="Global Temperature Trends",
    introduction=(
        "Explore annual global land-and-ocean temperatures, "
        "temperature anomalies, long-term patterns, and changes "
        "in reported measurement uncertainty."
    ),
)

try:
    global_annual = load_global_annual()

except (FileNotFoundError, ValueError) as error:
    st.error(
        "The Global Trends page could not load its data. "
        f"Details: {error}"
    )
    st.stop()


complete_temperature_data = global_annual.loc[
    global_annual["land_ocean_months"].eq(12)
].copy()

minimum_year = int(
    complete_temperature_data["year"].min()
)

maximum_year = int(
    complete_temperature_data["year"].max()
)


st.sidebar.header("Global trend controls")

metric_options = {
    "Temperature anomaly": {
        "column": "land_ocean_anomaly_c",
        "label": "Temperature anomaly",
    },
    "Absolute temperature": {
        "column": "land_ocean_average_temperature_c",
        "label": "Land-and-ocean temperature",
    },
}

selected_metric_name = st.sidebar.radio(
    "Measurement",
    options=list(metric_options),
    help=(
        "Anomalies show differences from the 1951–1980 "
        "project baseline. Absolute values show estimated "
        "global average temperature."
    ),
)

smoothing_options = {
    "Annual values only": 1,
    "5-year rolling mean": 5,
    "10-year rolling mean": 10,
}

selected_smoothing_name = st.sidebar.selectbox(
    "Trend smoothing",
    options=list(smoothing_options),
    index=2,
    help=(
        "A rolling mean reduces short-term variation but "
        "does not replace the original annual values."
    ),
)

selected_year_range = st.sidebar.slider(
    "Temperature-chart period",
    min_value=minimum_year,
    max_value=maximum_year,
    value=(minimum_year, maximum_year),
    step=1,
)

st.sidebar.caption(
    "These controls update the main temperature chart. "
    "The uncertainty chart retains its complete historical period."
)


selected_metric = metric_options[selected_metric_name]
rolling_window = smoothing_options[selected_smoothing_name]

filtered_temperature = complete_temperature_data.loc[
    complete_temperature_data["year"].between(
        selected_year_range[0],
        selected_year_range[1],
    )
].copy()

if filtered_temperature.empty:
    st.warning(
        "No complete annual observations are available for "
        "the selected period."
    )
    st.stop()


first_row = filtered_temperature.iloc[0]
last_row = filtered_temperature.iloc[-1]

selected_column = selected_metric["column"]
selected_label = selected_metric["label"]

first_value = first_row[selected_column]
last_value = last_row[selected_column]
period_change = last_value - first_value

warmest_row = filtered_temperature.loc[
    filtered_temperature[
        "land_ocean_average_temperature_c"
    ].idxmax()
]


st.subheader("Selected-period summary")

metric_columns = st.columns(4)

with metric_columns[0]:
    st.metric(
        label="Selected period",
        value=(
            f"{int(first_row['year'])}–"
            f"{int(last_row['year'])}"
        ),
        help="Years currently included in the temperature chart.",
    )

with metric_columns[1]:
    st.metric(
        label="First annual value",
        value=f"{first_value:.2f} °C",
        help=(
            f"The selected {selected_label.lower()} at the "
            "beginning of the chosen period."
        ),
    )

with metric_columns[2]:
    st.metric(
        label="Latest annual value",
        value=f"{last_value:.2f} °C",
        help=(
            f"The selected {selected_label.lower()} at the "
            "end of the chosen period."
        ),
    )

with metric_columns[3]:
    st.metric(
        label="End-to-start difference",
        value=f"{period_change:+.2f} °C",
        help=(
            "The final annual value minus the first annual value. "
            "This is not a fitted warming rate."
        ),
    )

direction_word = (
    "higher"
    if period_change >= 0
    else "lower"
)

st.info(
    f"The final annual value in the selected period was "
    f"{abs(period_change):.2f} °C {direction_word} than the "
    f"first annual value. The warmest annual value in this "
    f"selection occurred in {int(warmest_row['year'])}.",
    icon="📌",
)

st.divider()

st.subheader(selected_metric_name)

if selected_metric_name == "Temperature anomaly":
    st.write(
        "Anomalies show differences from the project's "
        "1951–1980 global land-and-ocean baseline. A value "
        "above zero represents a warmer year relative to that "
        "reference period."
    )

else:
    st.write(
        "Absolute temperature estimates describe the global "
        "land-and-ocean annual average. They should not be "
        "interpreted as the temperature experienced at every "
        "individual location."
    )

temperature_figure = build_global_temperature_chart(
    chart_data=filtered_temperature,
    value_column=selected_column,
    value_label=selected_label,
    rolling_window=rolling_window,
)

st.plotly_chart(
    temperature_figure,
    use_container_width=True,
    config={
        "displayModeBar": False,
    },
)

st.caption(
    "Rolling means are included as a visual aid. Hover over "
    "the chart to inspect individual years."
)

st.divider()

st.subheader("How has measurement uncertainty changed?")

st.write(
    "The source dataset includes a reported uncertainty value "
    "for each monthly land-temperature estimate. The chart shows "
    "the annual average of those reported monthly uncertainty values."
)

complete_uncertainty_data = global_annual.loc[
    global_annual["land_months"].eq(12)
].copy()

early_uncertainty = complete_uncertainty_data.loc[
    complete_uncertainty_data["year"] < 1900,
    "land_average_uncertainty_c",
]

recent_uncertainty = complete_uncertainty_data.loc[
    complete_uncertainty_data["year"] >= 1950,
    "land_average_uncertainty_c",
]

uncertainty_difference = (
    early_uncertainty.mean()
    - recent_uncertainty.mean()
)

uncertainty_columns = st.columns(3)

with uncertainty_columns[0]:
    st.metric(
        label="Before 1900",
        value=f"{early_uncertainty.mean():.3f} °C",
        help=(
            "Mean annual reported uncertainty across complete "
            "years before 1900."
        ),
    )

with uncertainty_columns[1]:
    st.metric(
        label="1950 onward",
        value=f"{recent_uncertainty.mean():.3f} °C",
        help=(
            "Mean annual reported uncertainty across complete "
            "years from 1950 through 2015."
        ),
    )

with uncertainty_columns[2]:
    st.metric(
        label="Difference",
        value=f"{uncertainty_difference:.3f} °C",
        help=(
            "Earlier-period mean minus the later-period mean."
        ),
    )

uncertainty_figure = build_global_uncertainty_chart(
    global_annual
)

st.plotly_chart(
    uncertainty_figure,
    use_container_width=True,
    config={
        "displayModeBar": False,
    },
)

st.caption(
    "The plotted value is the annual average of reported monthly "
    "uncertainties. It should not be interpreted as a newly "
    "calculated confidence interval for each annual mean."
)

st.success(
    "Reported uncertainty was substantially higher in the "
    "earlier period. This supports Hypothesis 2, while the data "
    "alone cannot identify which specific historical improvements "
    "caused the reduction.",
    icon="✅",
)

st.divider()

st.subheader("Download and inspect the selected data")

export_columns = [
    "year",
    "land_ocean_average_temperature_c",
    "land_ocean_average_uncertainty_c",
    "land_ocean_anomaly_c",
    "land_ocean_months",
]

export_data = filtered_temperature[
    export_columns
].copy()

csv_data = export_data.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download selected global data as CSV",
    data=csv_data,
    file_name=(
        f"climatelens_global_"
        f"{selected_year_range[0]}_"
        f"{selected_year_range[1]}.csv"
    ),
    mime="text/csv",
    help=(
        "Downloads the annual data currently selected by "
        "the year-range control."
    ),
)

with st.expander("Preview the selected data"):
    st.dataframe(
        export_data,
        use_container_width=True,
        hide_index=True,
    )

with st.expander("Technical interpretation notes"):
    st.markdown(
        """
        - Only years containing 12 land-and-ocean monthly
          observations are used in the temperature chart.
        - Land-and-ocean values begin in 1850.
        - Rolling means are calculated only for visual communication.
        - The end-to-start difference compares two individual years;
          it is not a fitted trend or causal estimate.
        - Reported uncertainty describes uncertainty in the source
          measurements, not uncertainty in this dashboard's code.
        """
    )

render_footer()
