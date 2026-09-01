"""Predictive-model performance page for ClimateLens."""

import streamlit as st

from src.charts import (
    build_coefficient_chart,
    build_cross_validation_chart,
    build_model_metric_chart,
    build_model_prediction_chart,
    build_residual_histogram,
)
from src.data_loader import (
    load_model_coefficients,
    load_model_cross_validation,
    load_model_metrics,
    load_model_predictions,
)
from src.ui import (
    render_footer,
    render_page_header,
)


render_page_header(
    eyebrow="Predictive prototype",
    title="Model Performance",
    introduction=(
        "Evaluate an educational one-month-ahead historical "
        "temperature model, compare it with a seasonal benchmark, "
        "and inspect its errors, stability, and limitations."
    ),
)

st.warning(
    "This model is a historical educational prototype. It is not "
    "a professional climate projection and must not be used for "
    "current monitoring, policy, or safety-critical decisions.",
    icon="⚠️",
)

try:
    model_metrics = load_model_metrics()
    predictions = load_model_predictions()
    cross_validation = load_model_cross_validation()
    coefficients = load_model_coefficients()

except (FileNotFoundError, ValueError) as error:
    st.error(
        "The Model Performance page could not load its data. "
        f"Details: {error}"
    )
    st.stop()


linear_rows = model_metrics.loc[
    model_metrics["model"].eq("Linear regression")
]

baseline_rows = model_metrics.loc[
    model_metrics["model"].eq(
        "Seasonal-naive baseline"
    )
]

if len(linear_rows) != 1 or len(baseline_rows) != 1:
    st.error(
        "Expected one linear-model row and one baseline row."
    )
    st.stop()

linear_metrics = linear_rows.iloc[0]
baseline_metrics = baseline_rows.iloc[0]


mae_improvement = (
    (
        baseline_metrics["mae_c"]
        - linear_metrics["mae_c"]
    )
    / baseline_metrics["mae_c"]
    * 100
)

rmse_improvement = (
    (
        baseline_metrics["rmse_c"]
        - linear_metrics["rmse_c"]
    )
    / baseline_metrics["rmse_c"]
    * 100
)


minimum_test_year = int(
    predictions["date"].dt.year.min()
)

maximum_test_year = int(
    predictions["date"].dt.year.max()
)


st.sidebar.header("Model chart controls")

selected_test_years = st.sidebar.slider(
    "Historical test period",
    min_value=minimum_test_year,
    max_value=maximum_test_year,
    value=(minimum_test_year, maximum_test_year),
    step=1,
)

available_series = [
    "Observed",
    "Linear regression",
    "Seasonal-naive baseline",
]

selected_series = st.sidebar.multiselect(
    "Series to display",
    options=available_series,
    default=available_series,
)

if not selected_series:
    st.warning(
        "Select at least one series in the sidebar."
    )
    st.stop()


filtered_predictions = predictions.loc[
    predictions["date"].dt.year.between(
        selected_test_years[0],
        selected_test_years[1],
    )
].copy()


st.subheader("Held-out test performance")

metric_columns = st.columns(4)

with metric_columns[0]:
    st.metric(
        label="Linear-model MAE",
        value=f"{linear_metrics['mae_c']:.3f} °C",
        help=(
            "Mean absolute error during January 2006 "
            "through December 2015."
        ),
    )

with metric_columns[1]:
    st.metric(
        label="Linear-model RMSE",
        value=f"{linear_metrics['rmse_c']:.3f} °C",
        help=(
            "Root mean squared error gives larger errors "
            "additional weight."
        ),
    )

with metric_columns[2]:
    st.metric(
        label="Linear-model R²",
        value=f"{linear_metrics['r2']:.4f}",
        help=(
            "The proportion of test-period variation captured "
            "by the model. Strong seasonality contributes "
            "substantially to this high value."
        ),
    )

with metric_columns[3]:
    st.metric(
        label="MAE improvement",
        value=f"{mae_improvement:.1f}%",
        help=(
            "Percentage reduction in MAE relative to the "
            "seasonal-naive baseline."
        ),
    )

st.success(
    f"The linear model reduced MAE by {mae_improvement:.1f}% "
    f"and RMSE by {rmse_improvement:.1f}% compared with the "
    f"seasonal-naive benchmark.",
    icon="✅",
)

st.divider()

st.subheader("Observed and predicted temperatures")

st.write(
    "The test set contains the final 120 months of the dataset. "
    "The model was trained only on earlier observations."
)

prediction_figure = build_model_prediction_chart(
    prediction_data=filtered_predictions,
    selected_series=selected_series,
)

st.plotly_chart(
    prediction_figure,
    use_container_width=True,
    config={
        "displayModeBar": False,
    },
)

st.caption(
    "The seasonal-naive benchmark predicts each month using the "
    "temperature observed in the same month one year earlier."
)

mean_residual = filtered_predictions[
    "residual_c"
].mean()

maximum_error = filtered_predictions[
    "absolute_error_c"
].max()

residual_columns = st.columns(3)

with residual_columns[0]:
    st.metric(
        label="Displayed months",
        value=f"{len(filtered_predictions):,}",
    )

with residual_columns[1]:
    st.metric(
        label="Mean residual",
        value=f"{mean_residual:+.3f} °C",
        help=(
            "Observed minus predicted. A positive value "
            "indicates average underprediction."
        ),
    )

with residual_columns[2]:
    st.metric(
        label="Largest absolute error",
        value=f"{maximum_error:.3f} °C",
    )

st.divider()

st.subheader("Model versus benchmark")

st.write(
    "MAE and RMSE are expressed in degrees Celsius. Lower values "
    "indicate smaller prediction errors."
)

metric_figure = build_model_metric_chart(
    model_metrics
)

st.plotly_chart(
    metric_figure,
    use_container_width=True,
    config={
        "displayModeBar": False,
    },
)

st.caption(
    "R² is not included in this bar chart because it uses a "
    "different scale from the temperature-error metrics."
)

st.divider()

st.subheader("Technical diagnostics")

residual_tab, validation_tab, coefficient_tab = st.tabs([
    "Residual distribution",
    "Cross-validation",
    "Model coefficients",
])

with residual_tab:
    st.write(
        "Residuals are calculated as observed temperature minus "
        "predicted temperature. Values centred near zero indicate "
        "limited overall bias."
    )

    residual_figure = build_residual_histogram(
        filtered_predictions
    )

    st.plotly_chart(
        residual_figure,
        use_container_width=True,
        config={
            "displayModeBar": False,
        },
    )

    st.caption(
        "A positive residual means the observed temperature "
        "was higher than the model prediction."
    )

with validation_tab:
    st.write(
        "Five expanding-window validation folds preserve time "
        "order. Each validation fold contains 120 months that "
        "occur after its corresponding training observations."
    )

    validation_figure = build_cross_validation_chart(
        cross_validation
    )

    st.plotly_chart(
        validation_figure,
        use_container_width=True,
        config={
            "displayModeBar": False,
        },
    )

    st.metric(
        label="Mean cross-validation MAE",
        value=(
            f"{cross_validation['mae_c'].mean():.3f} °C"
        ),
    )

with coefficient_tab:
    st.write(
        "Because the features were standardised before fitting, "
        "their coefficient magnitudes can be compared more directly."
    )

    coefficient_figure = build_coefficient_chart(
        coefficients
    )

    st.plotly_chart(
        coefficient_figure,
        use_container_width=True,
        config={
            "displayModeBar": False,
        },
    )

    strongest_feature = coefficients.loc[
        coefficients["absolute_coefficient"].idxmax()
    ]

    st.info(
        f"The largest absolute standardised coefficient belongs "
        f"to `{strongest_feature['feature']}`. Coefficient size "
        f"describes predictive association, not climate causation.",
        icon="ℹ️",
    )

st.divider()

st.subheader("Model card")

intended_column, limitations_column = st.columns(2)

with intended_column:
    st.markdown("#### Design and intended use")

    st.markdown(
        "- Model: standardised linear regression\n"
        "- Target: monthly global land-and-ocean temperature\n"
        "- Training period: January 1860–December 2005\n"
        "- Test period: January 2006–December 2015\n"
        "- Evaluation: one-month-ahead historical prediction\n"
        "- Intended use: education and analytics prototyping"
    )

with limitations_column:
    st.markdown("#### Limitations and prohibited use")

    st.markdown(
        "- The source data ends in December 2015.\n"
        "- The model is not a physical climate simulation.\n"
        "- It is not a long-range recursive forecast.\n"
        "- Test predictions use preceding observed months.\n"
        "- Coefficients do not establish causal relationships.\n"
        "- It must not support safety-critical decisions."
    )

with st.expander("Features used by the model"):
    st.markdown(
        "- Chronological time index\n"
        "- Cyclical month sine and cosine components\n"
        "- Previous-month temperature\n"
        "- Temperature from the same month one year earlier\n"
        "- Previous 12-month rolling mean\n"
        "- Previous 120-month rolling mean"
    )

st.info(
    "The model's high R² is partly caused by predictable seasonal "
    "variation. Benchmark comparison, MAE, RMSE, residuals, and "
    "chronological validation provide more complete evidence than "
    "R² alone.",
    icon="📌",
)

st.divider()

st.subheader("Download model results")

download_columns = st.columns(2)

with download_columns[0]:
    prediction_csv = filtered_predictions.to_csv(
        index=False,
        date_format="%Y-%m-%d",
    ).encode("utf-8")

    st.download_button(
        label="Download displayed predictions",
        data=prediction_csv,
        file_name=(
            "climatelens_model_predictions_"
            f"{selected_test_years[0]}_"
            f"{selected_test_years[1]}.csv"
        ),
        mime="text/csv",
    )

with download_columns[1]:
    metrics_csv = model_metrics.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download model metrics",
        data=metrics_csv,
        file_name="climatelens_model_metrics.csv",
        mime="text/csv",
    )

with st.expander("Preview displayed predictions"):
    st.dataframe(
        filtered_predictions,
        use_container_width=True,
        hide_index=True,
    )

render_footer()
