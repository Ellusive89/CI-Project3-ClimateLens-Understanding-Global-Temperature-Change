"""Hypothesis-validation page for ClimateLens."""

import pandas as pd
import streamlit as st

from src.charts import build_hypothesis_box_chart
from src.data_loader import (
    load_global_annual,
    load_hypothesis_results,
)
from src.ui import (
    render_footer,
    render_page_header,
)


def describe_effect_size(value):
    """Return an accessible description of absolute Cohen's d."""
    absolute_value = abs(value)

    if absolute_value < 0.2:
        return "very small"

    if absolute_value < 0.5:
        return "small"

    if absolute_value < 0.8:
        return "medium"

    return "large"


render_page_header(
    eyebrow="Evidence",
    title="Project Hypotheses",
    introduction=(
        "Review the two pre-stated hypotheses, compare their "
        "historical periods, and explore both plain-language "
        "conclusions and technical statistical results."
    ),
)

st.info(
    "The hypotheses were defined before completing the analysis. "
    "Both use complete annual observations rather than treating "
    "every monthly value as an independent result.",
    icon="ℹ️",
)

try:
    global_annual = load_global_annual()
    hypothesis_results = load_hypothesis_results()

except (FileNotFoundError, ValueError) as error:
    st.error(
        "The Hypotheses page could not load its data. "
        f"Details: {error}"
    )
    st.stop()


h1_rows = hypothesis_results.loc[
    hypothesis_results["hypothesis"].eq("H1")
]

h2_rows = hypothesis_results.loc[
    hypothesis_results["hypothesis"].eq("H2")
]

if len(h1_rows) != 1 or len(h2_rows) != 1:
    st.error(
        "Expected exactly one saved result for H1 and H2."
    )
    st.stop()

h1_result = h1_rows.iloc[0]
h2_result = h2_rows.iloc[0]


supported_count = (
    hypothesis_results["conclusion"]
    .str.casefold()
    .eq("supported")
    .sum()
)

summary_columns = st.columns(3)

with summary_columns[0]:
    st.metric(
        label="Hypotheses tested",
        value=str(len(hypothesis_results)),
    )

with summary_columns[1]:
    st.metric(
        label="Hypotheses supported",
        value=(
            f"{supported_count}/"
            f"{len(hypothesis_results)}"
        ),
    )

with summary_columns[2]:
    st.metric(
        label="Significance threshold",
        value="p < 0.05",
        help=(
            "The project uses 0.05 as its statistical "
            "significance threshold. Statistical significance "
            "does not automatically imply practical importance."
        ),
    )

st.warning(
    "A statistical test can describe differences in this dataset, "
    "but it cannot by itself prove why the difference occurred.",
    icon="⚠️",
)

st.divider()

# ------------------------------------------------------------------
# Hypothesis 1
# ------------------------------------------------------------------

st.header("Hypothesis 1 — Later global temperatures")

st.markdown(
    "> The mean global land-and-ocean temperature during "
    "1986–2015 is higher than during 1956–1985."
)

st.write(
    "The two periods contain 30 complete annual observations each. "
    "Using equal-length periods reduces the risk that one period "
    "dominates the comparison simply because it contains more years."
)

complete_ocean = global_annual.loc[
    global_annual["land_ocean_months"].eq(12)
].copy()

h1_chart_data = complete_ocean.loc[
    complete_ocean["year"].between(1956, 2015)
].copy()

h1_chart_data["period"] = h1_chart_data[
    "year"
].apply(
    lambda year: (
        "1956–1985"
        if year <= 1985
        else "1986–2015"
    )
)

h1_columns = st.columns(4)

with h1_columns[0]:
    st.metric(
        label="1956–1985 mean",
        value=f"{h1_result['group_1_mean_c']:.3f} °C",
    )

with h1_columns[1]:
    st.metric(
        label="1986–2015 mean",
        value=f"{h1_result['group_2_mean_c']:.3f} °C",
    )

with h1_columns[2]:
    st.metric(
        label="Difference",
        value=(
            f"{h1_result['directional_difference_c']:+.3f} °C"
        ),
        help="Later-period mean minus earlier-period mean.",
    )

with h1_columns[3]:
    st.metric(
        label="Conclusion",
        value=h1_result["conclusion"],
    )

h1_figure = build_hypothesis_box_chart(
    chart_data=h1_chart_data,
    value_column="land_ocean_average_temperature_c",
    y_axis_label=(
        "Annual land-and-ocean temperature (°C)"
    ),
    period_order=[
        "1956–1985",
        "1986–2015",
    ],
    colour_map={
        "1956–1985": "#4C78A8",
        "1986–2015": "#C45A28",
    },
    show_all_points=True,
)

st.plotly_chart(
    h1_figure,
    use_container_width=True,
    config={
        "displayModeBar": False,
    },
)

st.caption(
    "Each point represents one complete annual average. "
    "The box shows the distribution within each 30-year period."
)

st.success(
    f"Hypothesis 1 is supported. The 1986–2015 mean was "
    f"{h1_result['directional_difference_c']:.3f} °C higher "
    f"than the 1956–1985 mean.",
    icon="✅",
)

with st.expander("Technical details for Hypothesis 1"):
    h1_effect_description = describe_effect_size(
        h1_result["cohens_d"]
    )

    st.markdown(
        f"- Test: two-sided Welch independent-samples t-test\n"
        f"- Welch t-statistic: "
        f"{h1_result['welch_t_statistic']:.4f}\n"
        f"- Two-sided p-value: "
        f"{h1_result['two_sided_p_value']:.3e}\n"
        f"- Cohen's d: {h1_result['cohens_d']:.3f}\n"
        f"- Effect-size description: "
        f"{h1_effect_description}\n"
        f"- Annual observations per period: 30"
    )

    st.write(
        "Welch's test does not require the two periods to have "
        "equal variance. Cohen's d describes the size of the "
        "difference in standard-deviation units."
    )

st.divider()

# ------------------------------------------------------------------
# Hypothesis 2
# ------------------------------------------------------------------

st.header("Hypothesis 2 — Historical uncertainty")

st.markdown(
    "> Average global land-temperature measurement uncertainty "
    "is higher before 1900 than after 1950."
)

st.write(
    "This hypothesis examines whether the source dataset reports "
    "greater uncertainty for earlier historical measurements."
)

complete_land = global_annual.loc[
    global_annual["land_months"].eq(12)
].copy()

h2_chart_data = complete_land.loc[
    (complete_land["year"] < 1900)
    | (complete_land["year"] >= 1950)
].copy()

h2_chart_data["period"] = h2_chart_data[
    "year"
].apply(
    lambda year: (
        "Before 1900"
        if year < 1900
        else "1950 onward"
    )
)

h2_columns = st.columns(4)

with h2_columns[0]:
    st.metric(
        label="Before 1900 mean",
        value=f"{h2_result['group_1_mean_c']:.3f} °C",
    )

with h2_columns[1]:
    st.metric(
        label="1950 onward mean",
        value=f"{h2_result['group_2_mean_c']:.3f} °C",
    )

with h2_columns[2]:
    st.metric(
        label="Difference",
        value=(
            f"{h2_result['directional_difference_c']:+.3f} °C"
        ),
        help="Earlier-period mean minus later-period mean.",
    )

with h2_columns[3]:
    st.metric(
        label="Conclusion",
        value=h2_result["conclusion"],
    )

h2_figure = build_hypothesis_box_chart(
    chart_data=h2_chart_data,
    value_column="land_average_uncertainty_c",
    y_axis_label=(
        "Average reported annual uncertainty (°C)"
    ),
    period_order=[
        "Before 1900",
        "1950 onward",
    ],
    colour_map={
        "Before 1900": "#F2CF5B",
        "1950 onward": "#4C78A8",
    },
    show_all_points=False,
)

st.plotly_chart(
    h2_figure,
    use_container_width=True,
    config={
        "displayModeBar": False,
    },
)

st.caption(
    "The box plot compares complete annual averages. Outlying "
    "observations are shown, while individual non-outlying years "
    "are hidden to keep the larger comparison readable."
)

st.success(
    f"Hypothesis 2 is supported. Average reported uncertainty "
    f"before 1900 was {h2_result['directional_difference_c']:.3f} °C "
    f"higher than the average from 1950 onward.",
    icon="✅",
)

with st.expander("Technical details for Hypothesis 2"):
    h2_effect_description = describe_effect_size(
        h2_result["cohens_d"]
    )

    st.markdown(
        f"- Test: two-sided Welch independent-samples t-test\n"
        f"- Welch t-statistic: "
        f"{h2_result['welch_t_statistic']:.4f}\n"
        f"- Two-sided p-value: "
        f"{h2_result['two_sided_p_value']:.3e}\n"
        f"- Cohen's d: {h2_result['cohens_d']:.3f}\n"
        f"- Effect-size description: "
        f"{h2_effect_description}\n"
        f"- Complete years before 1900: 147\n"
        f"- Complete years from 1950 onward: 66"
    )

    st.write(
        "The periods contain different numbers of years, which "
        "is why Welch's test is preferred over a test that assumes "
        "equal variance and equal sample sizes."
    )

st.divider()

# ------------------------------------------------------------------
# Interpretation limitations
# ------------------------------------------------------------------

st.header("How should these findings be interpreted?")

plain_language_tab, technical_tab = st.tabs([
    "Plain-language summary",
    "Technical cautions",
])

with plain_language_tab:
    st.markdown(
        "- Both observed differences are large and consistent "
        "with the visual evidence.\n"
        "- The later global-temperature period is warmer than "
        "the earlier period.\n"
        "- Earlier measurements carry substantially greater "
        "reported uncertainty.\n"
        "- These findings describe the historical source data.\n"
        "- Statistical results alone do not establish physical causes."
    )

with technical_tab:
    st.markdown(
        "- Annual aggregation reduces monthly pseudoreplication.\n"
        "- Adjacent annual observations may still be correlated.\n"
        "- Time dependence can make conventional p-values optimistic.\n"
        "- Welch tests compare means but do not model time-series structure.\n"
        "- Cohen's d should be read alongside the raw difference.\n"
        "- Statistical significance is not the same as causal evidence.\n"
        "- The uncertainty field comes from the source dataset."
    )

st.divider()

st.subheader("Download the statistical summary")

hypothesis_csv = hypothesis_results.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download hypothesis results as CSV",
    data=hypothesis_csv,
    file_name="climatelens_hypothesis_results.csv",
    mime="text/csv",
)

with st.expander("Preview the statistical result table"):
    display_results = hypothesis_results.copy()

    display_results = display_results.rename(
        columns={
            "hypothesis": "Hypothesis",
            "comparison": "Comparison",
            "group_1_mean_c": "Group 1 mean (°C)",
            "group_2_mean_c": "Group 2 mean (°C)",
            "directional_difference_c": "Difference (°C)",
            "welch_t_statistic": "Welch t",
            "two_sided_p_value": "Two-sided p-value",
            "cohens_d": "Cohen's d",
            "conclusion": "Conclusion",
        }
    )

    st.dataframe(
        display_results,
        use_container_width=True,
        hide_index=True,
    )

render_footer()
