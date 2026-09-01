# ClimateLens: Understanding Global Temperature Change

[View the GitHub repository](https://github.com/Ellusive89/CI-Project3-ClimateLens-Understanding-Global-Temperature-Change)

ClimateLens is an interactive Streamlit data dashboard that explores historical
global and country-level temperature patterns, reported measurement
uncertainty, project hypotheses, and an educational predictive model.

The project was created as a capstone project for ethical practice and
communication in data analytics. It combines data analysis, visualisation,
statistical hypothesis testing, predictive modelling, accessible
communication, and responsible data governance.

The source dataset is historical. Global observations end in December 2015,
and complete country-year summaries end in 2012. ClimateLens must not be
presented as a current climate-monitoring system.

---

## Table of Contents

- [Project Purpose](#project-purpose)
- [Target Audience](#target-audience)
- [Business Requirements](#business-requirements)
- [User Stories](#user-stories)
- [Dataset](#dataset)
- [Data Quality and Cleaning](#data-quality-and-cleaning)
- [Project Hypotheses](#project-hypotheses)
- [Predictive Model](#predictive-model)
- [Dashboard Design](#dashboard-design)
- [Rationale for Visualisations](#rationale-for-visualisations)

## Project Purpose

Climate change datasets contain long time series, uncertainty measurements, geographical differences, and technical statistical results. These can be difficult for a general audience to interpret responsibly.

ClimateLens addresses this problem by providing a structured data story that:

- explains long-term global temperature patterns;
- distinguishes absolute temperature from temperature anomaly;
- communicates reported measurement uncertainty;
- supports country and area comparisons;
- validates pre-stated project hypotheses;
- evaluates a historical predictive prototype;
- provides plain-language and technical explanations;
- documents ethical, legal, social, and governance considerations.

The dashboard is designed as a public-awareness and educational analytics tool. It is not a professional climate projection or current monitoring service.

## Target Audience

The intended users are:

- students learning about climate data;
- educators communicating environmental trends;
- environmental organisations preparing public-awareness material;
- sustainability and policy teams seeking an accessible historical overview;
- data analysts interested in time-series analysis and responsible modelling;
- members of the public interested in long-term temperature change.

## Business Requirements

### BR1 — Communicate global temperature change

Users need to understand how global land-and-ocean temperature has changed over time.

The solution must:

- present annual absolute temperature and temperature anomaly;
- explain the 1951–1980 project baseline;
- support selectable year ranges;
- provide annual, five-year, and ten-year trend views;
- clearly state that the data is historical.

### BR2 — Explain measurement uncertainty

Users need to understand that historical measurements have different levels of uncertainty.

The solution must:

- visualise annual average reported uncertainty;
- compare uncertainty before 1900 with uncertainty from 1950 onward;
- explain that uncertainty does not automatically make data unusable;
- avoid presenting averaged uncertainty as a newly calculated confidence
  interval for annual temperature.

### BR3 — Support responsible country comparison

Users need to compare temperature patterns between countries and geographical areas without confusing different absolute climates.

The solution must:

- use country-specific temperature anomalies;
- use a shared complete-year comparison period;
- support selection of up to six labels;
- use colour and line style together;
- compare equal 30-year periods;
- explain that temperature change is not a measure of climate responsibility.

### BR4 — Validate project hypotheses

Users need to understand whether the project's pre-stated hypotheses were supported.

The solution must:

- show the hypothesis statements;
- display appropriate distribution visualisations;
- report group means and differences;
- report Welch test results and effect sizes;
- provide plain-language and technical interpretations;
- explain that statistical significance does not prove causation.

### BR5 — Evaluate a predictive model

Technical users need to understand how well a historical model performs and whether it improves upon a simple benchmark.

The solution must:

- use chronological training and test periods;
- avoid random train/test splitting;
- compare the model with a seasonal-naive baseline;
- report MAE, RMSE, and R²;
- use time-series cross-validation;
- display residuals and standardised coefficients;
- publish intended-use and prohibited-use limitations.

### BR6 — Demonstrate responsible data practice

All users need transparent information about data provenance, privacy, licensing, ethics, bias, governance, and model limitations.

The solution must:

- document dataset sources and licences;
- explain GDPR relevance;
- describe historical and geographical bias;
- include a project risk register;
- document data versioning and maintenance;
- disclose generative AI assistance;
- make limitations visible in the dashboard and README.

## User Stories

| ID | User story | Acceptance evidence |
|---|---|---|
| US1 | As a member of the public, I want a clear project summary so that I can understand the dashboard without reading technical documentation. | Overview page, definitions, metric cards and historical-data notice |
| US2 | As an educator, I want an interactive global trend chart so that I can explain anomalies and long-term patterns. | Global Trends page with metric, smoothing and year controls |
| US3 | As a non-technical user, I want uncertainty explained in plain language so that I do not assume all historical measurements are equally precise. | Uncertainty chart, captions and Hypothesis 2 explanation |
| US4 | As an environmental communicator, I want to compare country patterns fairly so that different absolute climates do not create misleading comparisons. | Country-specific anomalies and equal-period comparison |
| US5 | As a technical user, I want statistical outputs so that I can inspect how the hypotheses were validated. | Welch statistics, p-values, Cohen's d and box plots |
| US6 | As a data analyst, I want model and baseline metrics so that I can judge whether model complexity adds value. | Model Performance page |
| US7 | As a responsible practitioner, I want privacy, legal and governance documentation so that I can assess appropriate use. | Ethics & Governance page and risk register |
| US8 | As a dashboard user, I want responsive controls and downloadable data so that I can explore and retain relevant results. | Sidebar controls, CSV downloads and responsive layout |

## Dataset

### Source

The project uses the Kaggle dataset:

[Climate Change: Earth Surface Temperature Data](https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data)

The original temperature records were produced by:

[Berkeley Earth](https://berkeleyearth.org/data/)

The dataset was downloaded on 31 August 2026.

### Licence

The Kaggle snapshot is identified as:

**Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0).**

The project:

- attributes Kaggle and Berkeley Earth;
- uses the dataset for educational and non-commercial purposes;
- documents the licence;
- preserves provenance;
- does not claim ownership of the source temperature data.

Berkeley Earth currently describes its data more generally as CC BY-NC 4.0.
The project follows the more specific terms displayed with the downloaded Kaggle snapshot.

### Files used

| File | Purpose |
|---|---|
| `GlobalTemperatures.csv` | Monthly global land, minimum, maximum, land-and-ocean temperatures, and uncertainty |
| `GlobalLandTemperaturesByCountry.csv` | Monthly country and geographical-area temperature and uncertainty |

The larger city, state, and major-city files were not used because they were not required to answer the business requirements.

### Original dataset dimensions

| Dataset | Rows | Columns | Coverage |
|---|---:|---:|---|
| Global temperatures | 3,192 | 9 | January 1750–December 2015 |
| Country temperatures | 577,462 | 4 | November 1743–September 2013 |

### Main analytical variables

| Variable | Meaning | Unit |
|---|---|---|
| `date` | Monthly observation date | Date |
| `year` | Calendar year | Year |
| `month` | Calendar month | 1–12 |
| `land_average_temperature_c` | Global land-average temperature | °C |
| `land_average_temperature_uncertainty_c` | Reported uncertainty for global land average | °C |
| `land_ocean_average_temperature_c` | Global combined land-and-ocean average | °C |
| `land_ocean_average_temperature_uncertainty_c` | Reported uncertainty for combined average | °C |
| `country` | Source geographical label | Text |
| `average_temperature_c` | Country or area average temperature | °C |
| `average_uncertainty_c` | Reported country or area uncertainty | °C |
| `baseline_temperature_c` | Country-specific 1951–1980 mean | °C |
| `temperature_anomaly_c` | Difference from the country-specific baseline | °C |

### Versioning

Raw and derived files are separated:

```text
data/
├── raw/
│   └── v1/
└── processed/
    └── v1/
```

Raw Version 1 files remain unchanged. Notebook-generated outputs are stored in the processed Version 1 directory.

## Data Quality and Cleaning

### Initial findings

- The global dataset contained 3,192 rows and 9 columns.
- The country dataset contained 577,462 rows and 4 columns.
- No invalid dates were found.
- No duplicated global dates were found.
- No duplicated country-and-date combinations were found.
- The raw country field contained 243 distinct labels.
- Global maximum, minimum, and land-and-ocean fields contained 1,200 missing values each because those series begin in January 1850.
- Global land-average temperature and uncertainty contained 12 missing values each.
- Country average temperature contained 32,651 missing values.
- Country uncertainty contained 31,912 missing values.

### Cleaning decisions

- Raw data was preserved without modification.
- Dates were converted into datetime values.
- Columns were renamed using descriptive snake_case names.
- Temperature column names include `_c` to identify Celsius.
- No temperatures were artificially imputed.
- Twelve global rows without the primary land-average measurement were removed.
- Structurally unavailable pre-1850 land-and-ocean fields were retained.
- Country rows without an average temperature were removed.
- Antarctica was excluded from the analytical country dataset because none of its 764 records contained an average temperature measurement.
- Complete-year filters were used for annual comparisons.
- The incomplete country year 2013 was excluded.
- Cleaned exports were reloaded and validated.

### Processed data

| File | Purpose |
|---|---|
| `global_temperatures_clean.csv` | Cleaned monthly global data |
| `country_temperatures_clean.csv` | Cleaned monthly country data |
| `global_annual_summary.csv` | Annual global summaries and anomalies |
| `country_annual_summary.csv` | Complete country-year summaries and anomalies |
| `hypothesis_results.csv` | Statistical hypothesis results |
| `model_test_predictions.csv` | Held-out model predictions |
| `model_metrics.csv` | Model and baseline performance |
| `model_cross_validation.csv` | Time-series validation folds |
| `model_coefficients.csv` | Standardised linear-model coefficients |

## Project Hypotheses

### Hypothesis 1

> The mean global land-and-ocean temperature during 1986–2015 is higher than during 1956–1985.

#### Validation method

- Complete annual averages were used.
- Both comparison periods contain 30 years.
- A two-sided Welch independent-samples t-test was performed.
- Cohen's d was calculated as an effect-size measure.
- A box plot was used to compare the distributions.

#### Result

| Measurement | Result |
|---|---:|
| 1956–1985 mean | 15.318 °C |
| 1986–2015 mean | 15.701 °C |
| Later minus earlier | +0.383 °C |
| Welch t-statistic | 10.501 |
| Two-sided p-value | 3.207 × 10⁻¹⁴ |
| Cohen's d | 2.711 |
| Conclusion | Supported |

The later period was approximately 0.383 °C warmer in this dataset. The large effect size and visual distribution support the conclusion.

The statistical result describes an association with historical time. It does not independently establish the physical causes of warming.

### Hypothesis 2

> Average global land-temperature measurement uncertainty is higher before 1900 than after 1950.

#### Validation method

- Complete annual averages were used.
- Years before 1900 were compared with years from 1950 onward.
- A two-sided Welch independent-samples t-test was performed.
- Cohen's d was calculated.
- Distribution and time-series visualisations were reviewed.

#### Result

| Measurement | Result |
|---|---:|
| Mean before 1900 | 1.524 °C |
| Mean from 1950 onward | 0.100 °C |
| Earlier minus later | +1.423 °C |
| Welch t-statistic | 18.193 |
| Two-sided p-value | 1.918 × 10⁻³⁹ |
| Cohen's d | 1.806 |
| Conclusion | Supported |

Reported uncertainty was substantially higher in the earlier period.

This is consistent with changes in measurement coverage and methods, but the dataset alone cannot identify which specific historical improvements caused the reduction.

### Statistical limitations

- Annual aggregation reduces monthly pseudoreplication.
- Adjacent annual observations may still be correlated.
- Time dependence may make conventional p-values optimistic.
- Welch tests compare means but do not model the complete time-series process.
- Statistical significance is not equivalent to causal evidence.
- Effect size and visual evidence are interpreted alongside p-values.

## Predictive Model

### Purpose

The model is an educational one-month-ahead historical prediction prototype.

It predicts monthly global land-and-ocean temperature using preceding historical observations.

It is not:

- a professional climate projection;
- a physical climate simulation;
- a live forecasting system;
- a replacement for authoritative climate models;
- appropriate for policy or safety-critical decisions.

### Features

The model uses:

- a chronological time index;
- a cyclical month sine component;
- a cyclical month cosine component;
- previous-month temperature;
- temperature from the same month one year earlier;
- the previous 12-month rolling mean;
- the previous 120-month rolling mean.

Lagged and rolling variables use preceding observations. The current target is not included in its own predictors.

### Evaluation design

| Stage | Period |
|---|---|
| Feature-ready data | January 1860–December 2015 |
| Training data | January 1860–December 2005 |
| Held-out test data | January 2006–December 2015 |
| Test observations | 120 months |
| Cross-validation | Five expanding chronological folds |

A random train/test split was deliberately avoided because it could place later observations in training while earlier observations appeared in testing.

### Test performance

| Model | MAE | RMSE | R² |
|---|---:|---:|---:|
| Linear regression | 0.089 °C | 0.114 °C | 0.9916 |
| Seasonal-naive baseline | 0.133 °C | 0.172 °C | 0.9807 |

The linear model reduced:

- MAE by approximately 33%;
- RMSE by approximately 34%.

The high R² is partly explained by strong seasonal variation. MAE, RMSE, residuals, chronological validation, and benchmark comparison provide more complete evidence than R² alone.

### Model limitations

- The source data ends in December 2015.
- The model is not trained on current climate observations.
- It predicts one historical month at a time using preceding observations.
- It is not a long-range recursive forecast.
- It does not model physical climate processes.
- Its coefficients describe predictive associations, not causation.
- It must not be used for professional or safety-critical decisions.

## Dashboard Design

ClimateLens uses a multipage Streamlit interface so users can move progressively from a general overview to detailed analysis.

### Information architecture

| Dashboard page | Purpose |
|---|---|
| Overview | Introduces the project, its historical-data limitations, principal metrics, key terminology, and responsible-use notice |
| Global Trends | Explores global temperature and measurement-uncertainty patterns over a user-selected period |
| Country Explorer | Compares country-specific temperature anomalies and equal-length historical periods |
| Hypotheses | Presents the two project hypotheses, statistical results, visual evidence, and plain-language conclusions |
| Model Performance | Compares the historical prediction model with a seasonal-naive benchmark and provides technical diagnostics |
| Ethics & Governance | Documents privacy, licensing, bias, social implications, governance controls, maintenance, and project risks |

### Information hierarchy

Each page follows a consistent structure:

1. A page title and short explanation establish its purpose.
2. Controls allow users to select relevant data.
3. Summary metrics communicate the principal results.
4. Visualisations provide supporting evidence.
5. Captions and explanatory text clarify interpretation.
6. Limitations and responsible-use notices reduce the risk of misleading conclusions.
7. Detailed tables and downloads are placed later on the page for users who require further information.

This structure supports both non-technical users seeking concise findings and technical users who want supporting measurements and diagnostics.

### User control and feedback

The dashboard provides:

- sidebar navigation between pages;
- year-range and measurement selectors;
- country and area selectors;
- rolling-average controls;
- ranking-direction and ranking-size controls;
- model-series and test-period controls;
- expandable explanations for technical terminology;
- tabs for model diagnostics;
- downloadable filtered data and analytical results;
- informational, warning, and success messages that provide feedback and clarify limitations.

The dashboard does not use automatic pop-ups, audio, video, or interactions that remove user control.

### Consistency

Consistent colours, typography, spacing, metric cards, chart layouts, captions, and explanatory notices are used across the application.

Temperature series use a consistent visual language, while contrasting colours distinguish rolling averages, benchmarks, comparison periods, and uncertainty measurements.

All pages use the same wide layout and shared styling. Reusable chart, data-loading, and interface functions reduce unnecessary duplication in the code.

### Accessibility and responsive design

Accessibility decisions include:

- descriptive page headings and subheadings;
- plain-language explanations alongside technical results;
- meaningful chart titles, axis titles, legends, captions, and hover information;
- colours selected for adequate contrast against the dashboard background;
- information communicated through labels and values rather than colour alone;
- controls with visible text labels and help text;
- Celsius units displayed with temperature measurements;
- signed anomaly values that distinguish positive and negative results;
- expandable sections that reduce cognitive load;
- charts sized to their containers;
- Streamlit columns that reorganise when the available screen width is reduced.

The dashboard should still be manually tested at desktop, tablet, and mobile-width layouts before deployment.

## Rationale for Visualisations

The dashboard contains several different plot types. Each was selected according to the analytical question rather than for decoration.

| Visualisation | Location | Analytical purpose |
|---|---|---|
| Metric cards | Multiple pages | Communicate important values quickly, including anomalies, uncertainty, effect sizes, and model errors |
| Time-series line chart | Overview and Global Trends | Shows how temperature measurements and anomalies change chronologically |
| Rolling-mean line | Overview, Global Trends, and Country Explorer | Reduces short-term variation so the longer-term pattern is easier to interpret |
| Uncertainty line chart | Global Trends | Shows how reported measurement uncertainty changes through time |
| Multi-series anomaly line chart | Country Explorer | Allows selected countries or areas to be compared relative to their own 1951–1980 baselines |
| Horizontal bar chart | Country Explorer | Ranks equal-period historical temperature differences while keeping geographical labels readable |
| Box plots | Hypotheses | Compare distributions, medians, spread, and outliers between hypothesis groups |
| Observed-versus-predicted line chart | Model Performance | Shows how closely model and benchmark predictions follow held-out observations through time |
| Grouped bar chart | Model Performance | Compares model MAE and RMSE directly with the seasonal-naive benchmark |
| Residual histogram | Model Performance | Shows the distribution of prediction errors and whether residuals are centred near zero |
| Cross-validation bar chart | Model Performance | Compares prediction error across chronological validation folds |
| Coefficient bar chart | Model Performance | Shows the direction and relative magnitude of standardised predictive associations |

### Relationship to the business requirements

- Global time-series charts address **BR1** by explaining historical global temperature patterns.
- Uncertainty charts and comparison plots address **BR2** by communicating measurement reliability.
- Country anomaly lines and period-comparison bars address **BR3** by enabling geographical exploration.
- Box plots and statistical summaries address **BR4** by validating the project hypotheses.
- Prediction, benchmark, residual, validation, and coefficient charts address **BR5** by evaluating the historical predictive model.
- Captions, warnings, model limitations, and governance content address **BR6** by supporting responsible interpretation.

The dashboard therefore exceeds the requirement to display at least two different plot types. It uses line charts, bar charts, box plots, and a histogram, with each visual connected to a stated business requirement.
