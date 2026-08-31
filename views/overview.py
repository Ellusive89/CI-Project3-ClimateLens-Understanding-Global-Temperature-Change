"""ClimateLens dashboard Overview page."""

import streamlit as st

from src.charts import build_global_anomaly_chart
from src.data_loader import (
    load_country_annual,
    load_global_annual,
    load_hypothesis_results,
    load_model_metrics,
)
from src.ui import (
    render_footer,
    render_page_header,
)


render_page_header(
    eyebrow="ClimateLens",
    title="Understanding Global Temperature Change",
    introduction=(
        "Explore historical temperature patterns, reported "
        "measurement uncertainty, country-level anomalies, "
        "project hypotheses, and an educational predictive model."
    ),
)

st.info(
    "Historical-data notice: the global dataset ends in December "
    "2015, while complete country-year summaries end in 2012. "
    "The dashboard must not be interpreted as a current monitoring tool.",
    icon="ℹ️",
)

try:
    global_annual = load_global_annual()
    country_annual = load_country_annual()
    hypothesis_results = load_hypothesis_results()
    model_metrics = load_model_metrics()

except (FileNotFoundError, ValueError) as error:
    st.error(
        "The dashboard could not load its processed data. "
        f"Details: {error}"
    )
    st.stop()


complete_global = global_annual.loc[
    global_annual["land_ocean_months"].eq(12)
]

latest_global = complete_global.loc[
    complete_global["year"].idxmax()
]

country_count = country_annual["country"].nunique()

supported_hypotheses = (
    hypothesis_results["conclusion"]
    .str.casefold()
    .eq("supported")
    .sum()
)

linear_model_metrics = model_metrics.loc[
    model_metrics["model"].eq("Linear regression")
].iloc[0]


st.subheader("Project at a glance")

metric_columns = st.columns(4)

with metric_columns[0]:
    st.metric(
        label="2015 anomaly",
        value=(
            f"{latest_global['land_ocean_anomaly_c']:+.2f} °C"
        ),
        help=(
            "Difference from the project's 1951–1980 "
            "global land-and-ocean baseline."
        ),
    )

with metric_columns[1]:
    st.metric(
        label="Country/area labels",
        value=f"{country_count:,}",
        help=(
            "Distinct geographical labels with complete annual "
            "temperature summaries."
        ),
    )

with metric_columns[2]:
    st.metric(
        label="Hypotheses supported",
        value=(
            f"{supported_hypotheses}/"
            f"{len(hypothesis_results)}"
        ),
        help=(
            "Number of pre-stated project hypotheses supported "
            "by the historical analysis."
        ),
    )

with metric_columns[3]:
    st.metric(
        label="Model test MAE",
        value=f"{linear_model_metrics['mae_c']:.3f} °C",
        help=(
            "Mean absolute error during the held-out "
            "2006–2015 test period."
        ),
    )

st.caption(
    "The country figure describes dataset labels, which may include "
    "territories or historical geographical names—not necessarily "
    "242 currently recognised sovereign states."
)

st.divider()

st.subheader("Global signal at a glance")

st.write(
    "The chart shows annual land-and-ocean temperature differences "
    "from the project's 1951–1980 baseline. The rolling mean reduces "
    "short-term variation and makes the longer-term pattern easier "
    "to interpret."
)

anomaly_figure = build_global_anomaly_chart(global_annual)

st.plotly_chart(
    anomaly_figure,
    use_container_width=True,
    config={
        "displayModeBar": False,
    },
)

st.caption(
    "A positive anomaly means the annual temperature was warmer "
    "than the 1951–1980 project baseline. It does not mean every "
    "location experienced the same temperature change."
)

st.divider()

st.subheader("Questions addressed by the dashboard")

question_columns = st.columns(3)

with question_columns[0]:
    st.markdown("#### How has temperature changed?")

    st.write(
        "Explore annual global anomalies and compare longer-term "
        "patterns with short-term variability."
    )

with question_columns[1]:
    st.markdown("#### How reliable are the measurements?")

    st.write(
        "Examine reported uncertainty and learn why earlier "
        "measurements carry greater uncertainty."
    )

with question_columns[2]:
    st.markdown("#### What can the model demonstrate?")

    st.write(
        "Compare a historical one-month-ahead linear model with "
        "a seasonal-naive benchmark."
    )

st.divider()

st.subheader("How to interpret key terms")

with st.expander("Temperature anomaly"):
    st.write(
        "A temperature anomaly is the difference between an "
        "observed temperature and a reference-period average. "
        "It is not the same as an absolute temperature."
    )

with st.expander("Measurement uncertainty"):
    st.write(
        "Uncertainty describes the reported range of confidence "
        "around a measurement. Higher uncertainty does not "
        "automatically make an observation useless, but it should "
        "affect how confidently the value is interpreted."
    )

with st.expander("Historical prediction model"):
    st.write(
        "The model predicts a month in the historical test period "
        "using earlier observations. It is not a professional "
        "future climate projection."
    )

st.divider()

st.subheader("Data source and responsible use")

source_html = (
    '<p>'
    'The source data was downloaded from '
    '<a '
    'href="https://www.kaggle.com/datasets/'
    'berkeleyearth/climate-change-earth-surface-temperature-data" '
    'target="_blank" '
    'rel="noopener noreferrer">'
    'Kaggle'
    '</a> '
    'and originated from the '
    '<a '
    'href="https://berkeleyearth.org/data/" '
    'target="_blank" '
    'rel="noopener noreferrer">'
    'Berkeley Earth temperature project'
    '</a>. '
    'External links open in a separate tab.'
    '</p>'
)

st.markdown(
    source_html,
    unsafe_allow_html=True,
)

st.warning(
    "The dashboard communicates patterns in a historical dataset. "
    "It does not establish climate causation, provide live sensor "
    "measurements, or replace authoritative scientific assessments.",
    icon="⚠️",
)

render_footer()
