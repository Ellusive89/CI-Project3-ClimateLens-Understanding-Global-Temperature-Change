"""Interactive Country Explorer page for ClimateLens."""

import pandas as pd
import streamlit as st

from src.charts import (
    build_country_change_bar_chart,
    build_country_comparison_chart,
)
from src.data_loader import load_country_annual
from src.ui import (
    render_footer,
    render_page_header,
)


render_page_header(
    eyebrow="Country analysis",
    title="Country Temperature Explorer",
    introduction=(
        "Compare country-specific temperature anomalies, "
        "explore longer-term patterns, and examine changes "
        "between equal historical periods."
    ),
)

st.info(
    "Country names are reproduced from the historical source "
    "dataset. Some labels may represent territories, historical "
    "names, or geographical groupings rather than currently "
    "recognised sovereign states.",
    icon="ℹ️",
)

try:
    country_annual = load_country_annual()

except (FileNotFoundError, ValueError) as error:
    st.error(
        "The Country Explorer could not load its data. "
        f"Details: {error}"
    )
    st.stop()


available_countries = sorted(
    country_annual["country"].unique()
)

default_countries = [
    "Sweden",
    "United Kingdom",
    "United States",
    "India",
    "Brazil",
    "Australia",
]


st.sidebar.header("Country comparison controls")

selected_countries = st.sidebar.multiselect(
    "Select up to six country/area labels",
    options=available_countries,
    default=default_countries,
    max_selections=6,
    help=(
        "Country-specific anomalies are used so locations "
        "with different absolute climates can be compared."
    ),
)

if not selected_countries:
    st.warning(
        "Select at least one country or area in the sidebar "
        "to display the comparison."
    )
    st.stop()


selected_year_range = st.sidebar.slider(
    "Comparison period",
    min_value=1951,
    max_value=2012,
    value=(1951, 2012),
    step=1,
    help=(
        "Every country/area label contains complete annual "
        "data throughout this shared comparison period."
    ),
)

smoothing_options = {
    "Annual values": 1,
    "5-year rolling mean": 5,
    "10-year rolling mean": 10,
}

selected_smoothing = st.sidebar.selectbox(
    "Trend smoothing",
    options=list(smoothing_options),
    index=2,
)

rolling_window = smoothing_options[selected_smoothing]

years_selected = (
    selected_year_range[1]
    - selected_year_range[0]
    + 1
)

if years_selected < rolling_window:
    st.info(
        "The selected period is shorter than the smoothing "
        "window, so annual values are displayed instead.",
        icon="ℹ️",
    )

    effective_rolling_window = 1

else:
    effective_rolling_window = rolling_window


st.sidebar.divider()
st.sidebar.header("Period-ranking controls")

ranking_direction = st.sidebar.radio(
    "Display",
    options=[
        "Largest increases",
        "Smallest increases",
    ],
    help=(
        "The ranking compares two equal 30-year averages. "
        "It is not a ranking of climate responsibility."
    ),
)

ranking_count = st.sidebar.select_slider(
    "Number of labels",
    options=[10, 15, 20],
    value=15,
)


filtered_countries = country_annual.loc[
    country_annual["country"].isin(
        selected_countries
    )
    & country_annual["year"].between(
        selected_year_range[0],
        selected_year_range[1],
    )
].copy()

latest_selected_year = selected_year_range[1]

latest_values = filtered_countries.loc[
    filtered_countries["year"].eq(
        latest_selected_year
    )
].copy()

mean_latest_anomaly = (
    latest_values["temperature_anomaly_c"].mean()
)

highest_latest = latest_values.loc[
    latest_values["temperature_anomaly_c"].idxmax()
]

lowest_latest = latest_values.loc[
    latest_values["temperature_anomaly_c"].idxmin()
]


st.subheader("Selected comparison")

summary_columns = st.columns(4)

with summary_columns[0]:
    st.metric(
        label="Selected labels",
        value=str(len(selected_countries)),
        help="Number of country/area series currently displayed.",
    )

with summary_columns[1]:
    st.metric(
        label="Selected period",
        value=(
            f"{selected_year_range[0]}–"
            f"{selected_year_range[1]}"
        ),
    )

with summary_columns[2]:
    st.metric(
        label=f"Mean anomaly in {latest_selected_year}",
        value=f"{mean_latest_anomaly:+.2f} °C",
        help=(
            "Unweighted mean of the selected country-specific "
            "anomalies in the final selected year."
        ),
    )

with summary_columns[3]:
    st.metric(
        label=(
            f"Highest in {latest_selected_year}: "
            f"{highest_latest['country']}"
        ),
        value=(
            f"{highest_latest['temperature_anomaly_c']:+.2f} °C"
        ),
        help=(
            "Highest anomaly among only the currently selected "
            "labels—not among the complete dataset."
        ),
    )

st.caption(
    f"The lowest anomaly among the selected labels in "
    f"{latest_selected_year} was "
    f"{lowest_latest['temperature_anomaly_c']:+.2f} °C "
    f"for {lowest_latest['country']}."
)

st.divider()

st.subheader("Country-specific temperature anomalies")

st.write(
    "Each series is measured relative to that country or area's "
    "own 1951–1980 average. This supports more meaningful comparison "
    "than plotting absolute temperatures from different climates."
)

comparison_figure = build_country_comparison_chart(
    chart_data=filtered_countries,
    rolling_window=effective_rolling_window,
)

st.plotly_chart(
    comparison_figure,
    use_container_width=True,
    config={
        "displayModeBar": False,
    },
)

st.caption(
    "A positive value indicates that the selected year was warmer "
    "than the same country or area's 1951–1980 average."
)

st.warning(
    "This comparison does not account for population, geographical "
    "area, emissions, economic activity, or climate responsibility.",
    icon="⚠️",
)

st.divider()

st.subheader("Equal-period temperature comparison")

st.write(
    "The ranking compares mean annual temperature in 1981–2010 "
    "with mean annual temperature in 1951–1980. Both periods contain "
    "30 complete years for every included label."
)


baseline_period = (
    country_annual.loc[
        country_annual["year"].between(1951, 1980)
    ]
    .groupby("country", as_index=False)
    .agg(
        baseline_mean_c=(
            "average_temperature_c",
            "mean",
        ),
        baseline_years=(
            "year",
            "nunique",
        ),
    )
)

recent_period = (
    country_annual.loc[
        country_annual["year"].between(1981, 2010)
    ]
    .groupby("country", as_index=False)
    .agg(
        recent_mean_c=(
            "average_temperature_c",
            "mean",
        ),
        recent_years=(
            "year",
            "nunique",
        ),
    )
)

country_change = baseline_period.merge(
    recent_period,
    on="country",
    how="inner",
    validate="one_to_one",
)

country_change = country_change.loc[
    country_change["baseline_years"].eq(30)
    & country_change["recent_years"].eq(30)
].copy()

country_change["temperature_change_c"] = (
    country_change["recent_mean_c"]
    - country_change["baseline_mean_c"]
)

if ranking_direction == "Largest increases":
    ranking_data = country_change.nlargest(
        ranking_count,
        "temperature_change_c",
    )

else:
    ranking_data = country_change.nsmallest(
        ranking_count,
        "temperature_change_c",
    )

ranking_figure = build_country_change_bar_chart(
    ranking_data
)

st.plotly_chart(
    ranking_figure,
    use_container_width=True,
    config={
        "displayModeBar": False,
    },
)

leading_change = ranking_data.iloc[
    ranking_data["temperature_change_c"].argmax()
]

if ranking_direction == "Smallest increases":
    leading_change = ranking_data.iloc[
        ranking_data["temperature_change_c"].argmin()
    ]

st.info(
    f"In the current view, {leading_change['country']} has a "
    f"period-average difference of "
    f"{leading_change['temperature_change_c']:+.3f} °C. "
    f"This is a descriptive historical comparison, not a "
    f"causal or responsibility ranking.",
    icon="📊",
)

st.divider()

st.subheader("Download and inspect selected country data")

export_columns = [
    "country",
    "year",
    "average_temperature_c",
    "average_uncertainty_c",
    "temperature_anomaly_c",
    "months_observed",
]

export_data = (
    filtered_countries[export_columns]
    .sort_values(["country", "year"])
)

csv_data = export_data.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download selected country data as CSV",
    data=csv_data,
    file_name=(
        "climatelens_country_comparison_"
        f"{selected_year_range[0]}_"
        f"{selected_year_range[1]}.csv"
    ),
    mime="text/csv",
)

with st.expander("Preview selected country data"):
    st.dataframe(
        export_data,
        use_container_width=True,
        hide_index=True,
    )

with st.expander("Country comparison limitations"):
    st.markdown(
        "- Country names and boundaries may have changed over time.\n"
        "- Historical station coverage differs between regions.\n"
        "- Country averages can hide substantial local variation.\n"
        "- Each country receives equal weight in unweighted summaries.\n"
        "- Temperature change does not measure emissions or responsibility.\n"
        "- Rankings are sensitive to the selected comparison periods."
    )

render_footer()
