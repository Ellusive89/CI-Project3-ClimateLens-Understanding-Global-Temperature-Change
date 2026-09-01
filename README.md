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