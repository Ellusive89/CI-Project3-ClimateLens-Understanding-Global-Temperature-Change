# ClimateLens Testing

## Testing Approach

ClimateLens uses a combination of:

- automated processed-data validation;
- automated Plotly chart-generation tests;
- automated Streamlit page smoke tests;
- manual interaction testing;
- responsive-layout testing;
- accessibility review;
- external-link and download testing;
- post-deployment verification.

Automated tests confirm repeatable technical behaviour. Manual tests remain necessary because automated smoke tests cannot fully evaluate visual layout, usability, browser downloads, or the clarity of communication.

## Automated Testing

### Environment

| Item | Value |
|---|---|
| Operating system | macOS |
| Python | 3.12.8 |
| pytest | 9.1.1 |
| Test date | 1 September 2026 |

### Command

The complete automated suite was run from the repository root:

```bash
.venv/bin/python -m pytest -v
```

### Result

```text
19 passed, 2 warnings in 1.33 seconds
```

All automated tests passed.

The two warnings originated inside Plotly's datetime validation code and concern a future change to Pandas `DatetimeProperties.to_pydatetime`. They did not cause test failures and were not produced directly by custom project logic.

This compatibility warning should be reviewed when Plotly or Pandas is updated.

### Automated test coverage

| Test file | Coverage | Result |
|---|---|---|
| `tests/test_data_loader.py` | Processed-data schemas, dimensions, date coverage, missing values, duplicate keys, hypothesis outputs, model outputs, chronological predictions, validation folds, and coefficients | 8 passed |
| `tests/test_charts.py` | Global, country, hypothesis, prediction, benchmark, residual, validation, and coefficient chart generation | 4 passed |
| `tests/test_streamlit_pages.py` | Application entry point and all six Streamlit page scripts | 7 passed |
| **Total** | **Complete automated suite** | **19 passed** |

## Manual Functional Testing

The manual functional tests were completed locally on 1 September 2026.

### Navigation and Overview

| ID | Test | Expected result | Status |
|---|---|---|---|
| NAV-01 | Start the application | ClimateLens loads without an error message | Pass |
| NAV-02 | Inspect the sidebar | All six pages appear in three clearly labelled navigation groups | Pass |
| NAV-03 | Open every navigation item | The selected page loads and its navigation label remains identifiable | Pass |
| OV-01 | Open Overview | The project title, purpose, and historical-data notice are immediately visible | Pass |
| OV-02 | Inspect the four summary cards | The 2015 anomaly, label count, hypothesis count, and model MAE display without overlap | Pass |
| OV-03 | Hover over the global chart | The tooltip displays a year and anomaly value in °C | Pass |
| OV-04 | Open each key-term expander | Each expander opens independently and displays its explanation | Pass |
| OV-05 | Select the Kaggle and Berkeley Earth links | Each external source opens in a separate browser tab | Pass |

### Global Trends

| ID | Test | Expected result | Status |
|---|---|---|---|
| GT-01 | Select `Temperature anomaly` | The chart and metric values describe temperature anomaly | Pass |
| GT-02 | Select `Absolute temperature` | The chart and metric values change to land-and-ocean temperature | Pass |
| GT-03 | Change the trend smoothing option | The selected rolling-mean line updates appropriately | Pass |
| GT-04 | Reduce the selected year range | Summary cards and the main temperature chart update to the chosen period | Pass |
| GT-05 | Hover over the temperature chart | The tooltip displays the selected measurement, year, and °C unit | Pass |
| GT-06 | Inspect the uncertainty chart | Earlier uncertainty is visibly greater and the comparison periods are labelled | Pass |
| GT-07 | Open both explanatory expanders | The data preview and technical notes display correctly | Pass |
| GT-08 | Download the selected data | A CSV file downloads and contains data for the selected period | Pass |

### Country Explorer

| ID | Test | Expected result | Status |
|---|---|---|---|
| CE-01 | Select one country or area | One labelled anomaly series is displayed | Pass |
| CE-02 | Select several labels | Each selected label appears as a separately identifiable series | Pass |
| CE-03 | Attempt to select more than six labels | The interface prevents more than six selections | Pass |
| CE-04 | Remove every selected label | A warning asks the user to select at least one label | Pass |
| CE-05 | Change the comparison period | Metrics and anomaly chart update to the selected years | Pass |
| CE-06 | Select a period shorter than the smoothing window | An information message explains that annual values are used | Pass |
| CE-07 | Change between largest and smallest increases | The equal-period ranking updates in the requested direction | Pass |
| CE-08 | Change the number of ranking labels | The bar chart displays 10, 15, or 20 labels as selected | Pass |
| CE-09 | Inspect the responsibility warning | The dashboard states that the ranking does not measure climate responsibility | Pass |
| CE-10 | Download selected country data | A CSV file downloads with only the selected labels and period | Pass |

### Hypotheses

| ID | Test | Expected result | Status |
|---|---|---|---|
| HY-01 | Open Hypotheses | Both hypotheses and their supported conclusions are visible | Pass |
| HY-02 | Inspect both box plots | Comparison periods are clearly labelled and use the correct °C axis | Pass |
| HY-03 | Open both technical-detail expanders | Test statistic, p-value, effect size, and limitations are displayed | Pass |
| HY-04 | Switch between interpretation tabs | Plain-language and technical interpretations display independently | Pass |
| HY-05 | Download the statistical summary | The downloaded CSV contains both H1 and H2 | Pass |

### Model Performance

| ID | Test | Expected result | Status |
|---|---|---|---|
| MP-01 | Open Model Performance | Model and benchmark metrics display without errors | Pass |
| MP-02 | Change the historical test period | The prediction chart and displayed-month metrics update | Pass |
| MP-03 | Add and remove chart series | Only the selected observed, model, and benchmark series appear | Pass |
| MP-04 | Remove every series | A warning asks the user to select at least one series | Pass |
| MP-05 | Inspect the benchmark chart | Linear regression has lower MAE and RMSE than the benchmark | Pass |
| MP-06 | Open each diagnostics tab | Residual, cross-validation, and coefficient charts display | Pass |
| MP-07 | Open the model feature expander | All seven chronological model features are explained | Pass |
| MP-08 | Download model results | Metrics and prediction CSV files download successfully | Pass |
| MP-09 | Inspect the model card | Intended use, prohibited use, evaluation, and limitations are clearly stated | Pass |

### Ethics and Governance

| ID | Test | Expected result | Status |
|---|---|---|---|
| EG-01 | Open Ethics & Governance | Four tabs appear: ethics, privacy, governance, and risk register | Pass |
| EG-02 | Inspect the ethics tab | Bias, fair communication, social implications, and AI transparency are documented | Pass |
| EG-03 | Inspect the privacy tab | GDPR relevance, hosting-log risk, licence, and attribution are documented | Pass |
| EG-04 | Select every external reference | Each external reference opens in a separate tab | Pass |
| EG-05 | Inspect the governance tab | Lifecycle, inventory, controls, and maintenance policy display correctly | Pass |
| EG-06 | Inspect the risk-register tab | Risks, impacts, mitigation, and monitoring information are visible | Pass |
| EG-07 | Download the risk register | A readable CSV file downloads successfully | Pass |

### Manual functional result

All 47 manual functional tests passed.

No unresolved functional defects were identified during this test stage.

## Responsive-Layout Testing

Responsive testing must be performed with the browser's responsive-design tools or by resizing the browser window.

The following representative viewport sizes are used:

| Device category | Test viewport |
|---|---|
| Desktop | 1440 × 900 |
| Tablet | 768 × 1024 |
| Mobile | 390 × 844 |

| ID | Test | Expected result | Status |
|---|---|---|---|
| RESP-01 | Open every page at desktop width | Content uses the available width without excessive stretching, clipping, or overlap | Pass |
| RESP-02 | Inspect metric-card rows at tablet width | Cards remain readable and reorganise without covering adjacent content | Pass |
| RESP-03 | Open every page at mobile width | Text, controls, charts, notices, and expanders remain readable | Pass |
| RESP-04 | Inspect charts at all three widths | Charts resize without overlapping preceding or following content | Pass |
| RESP-05 | Inspect chart legends at mobile width | Legends remain readable and do not cover the plotted data or following headings | Pass |
| RESP-06 | Open and close the sidebar at mobile width | Navigation can be opened, used, and closed without hiding page content permanently | Pass |
| RESP-07 | Test Global Trends controls at mobile width | Radio buttons, selector, and year slider remain usable | Pass |
| RESP-08 | Test Country Explorer controls at mobile width | Country selection, sliders, smoothing, and ranking controls remain usable | Pass |
| RESP-09 | Test Model Performance tabs at mobile width | Diagnostic tabs remain accessible and their content stays within the page | Pass |
| RESP-10 | Inspect Ethics & Governance tables at mobile width | Large tables can be viewed without breaking the rest of the page layout | Pass |

## Accessibility Testing

Accessibility was evaluated manually. This review does not claim formal WCAG certification.

| ID | Test | Expected result | Status |
|---|---|---|---|
| A11Y-01 | Navigate through controls using `Tab` and `Shift+Tab` | Interactive elements receive focus in a logical order | Pass |
| A11Y-02 | Activate focused controls using the keyboard | Buttons, selectors, expanders, tabs, and navigation can be operated without a mouse | Pass |
| A11Y-03 | Inspect keyboard focus | The currently focused interactive element is visually identifiable | Pass |
| A11Y-04 | Inspect headings on every page | Pages have descriptive titles, headings, and subheadings in a logical visual hierarchy | Pass |
| A11Y-05 | Inspect form controls | Every selector, slider, radio group, and multiselect has a visible text label | Pass |
| A11Y-06 | Inspect chart titles and axes | Charts include meaningful axis labels and Celsius units where appropriate | Pass |
| A11Y-07 | Inspect chart colours and styles | Information is supported by labels, values, legends, or line styles rather than colour alone | Pass |
| A11Y-08 | Inspect text and background contrast | Text, controls, notices, and chart labels remain clearly readable | Pass |
| A11Y-09 | Increase browser zoom to 200% | Content remains readable and operable without overlapping or disappearing | Pass |
| A11Y-10 | Inspect warning, information, and success messages | Meaning is communicated through text and icons rather than colour alone | Pass |
| A11Y-11 | Inspect technical terminology | Complex terms have nearby explanations, captions, help text, or expanders | Pass |
| A11Y-12 | Perform a VoiceOver spot check where practical | Page purpose, headings, navigation labels, and principal controls are announced meaningfully | Pass |

## Browser Compatibility Testing

Record the browser version from its About screen. Do not mark a browser as passed unless it was personally tested.

| Browser | Version | Application loads | Navigation and controls | Charts | Downloads | Result |
|---|---|---|---|---|---|
| Google Chrome |152.0.7977.65| Pass | Pass | Pass | Pass | Pass |
| Safari |26.5.2| Pass | Pass | Pass | Pass | Pass |
| Firefox |154.0.1| Pass | Pass | Pass | Pass | Pass |


## External-Link Testing

| Link destination | Location | Expected result | Status |
|---|---|---|---|
| Kaggle dataset | Overview and Ethics & Governance | Correct dataset page opens in a separate tab | Pass |
| Berkeley Earth data | Overview and Ethics & Governance | Berkeley Earth data page opens in a separate tab | Pass |
| CC BY-NC-SA 4.0 | Ethics & Governance | Correct Creative Commons licence page opens in a separate tab | Pass |
| European Commission GDPR application | Ethics & Governance | Correct European Commission page opens in a separate tab | Pass |
| European Commission GDPR principles | Ethics & Governance | Correct European Commission page opens in a separate tab | Pass |

## Defects Identified and Resolved

| Defect | Cause | Resolution | Retest result |
|---|---|---|---|
| Plotly figures would not display in a notebook | The Plotly notebook renderer required `nbformat` | Added and pinned `nbformat==5.10.4` | Pass |
| Statistical notebook functionality required a reproducible scientific dependency | SciPy was not explicitly available in the project environment | Added a compatible pinned SciPy dependency | Pass |
| Dashboard charts overlapped headings and later sections | Responsive chart sizing did not reserve a stable rendered height | Added explicit chart heights and shared chart spacing | Pass |
| Source links appeared as raw HTML | Multiline HTML strings were not composed correctly | Corrected link construction and retained safe new-tab attributes | Pass |
| Only the principal page appeared initially | The complete page structure needed to be registered through Streamlit navigation | Registered six pages in three navigation groups | Pass |
| Country data could have produced an incomplete 2013 annual comparison | The source ends in September 2013 | Restricted complete annual country summaries to 2012 | Pass |
| Random model evaluation risked time leakage | Random splitting ignores chronological order | Introduced chronological testing and expanding-window validation | Pass |
| Model metrics lacked an interpretable performance reference | Standalone metrics did not demonstrate improvement over a simple method | Added a seasonal-naive benchmark | Pass |

## Known Limitations and Outstanding Issues

### Third-party compatibility warning

The automated suite produces two non-failing warnings from Plotly's internal datetime-validation code concerning a future Pandas behaviour change.

The warning:

- does not originate from custom project logic;
- does not prevent chart creation;
- does not cause automated test failure;
- should be reviewed when upgrading Plotly or Pandas.

### Historical data

The application uses a historical dataset. Global observations end in December 2015, and complete country-year summaries end in 2012.

This is an intentional project limitation rather than a software defect. It is communicated throughout the dashboard.

## Post-Deployment Testing

The deployed application was tested on 2 September 2026.

**Live application:** [ClimateLens](https://climatelens-global-temperature-54cc5c60cb7b.herokuapp.com/)

| ID | Test | Expected result | Result |
|---|---|---|---|
| PD-01 | Open the root application URL | Overview loads successfully over HTTPS | Pass |
| PD-02 | Inspect deployed navigation | All six pages appear in the correct navigation groups | Pass |
| PD-03 | Open all six public routes | Every route loads without a Streamlit exception | Pass |
| PD-04 | Inspect deployed charts | Overview displays 1 chart, Global Trends 2, Country Explorer 2, Hypotheses 2, and Model Performance 5 | Pass |
| PD-05 | Inspect deployed model metrics | MAE is 0.089 °C, RMSE is 0.114 °C, R² is 0.9916, and MAE improvement is 33.0% | Pass |
| PD-06 | Inspect the browser console | No browser-console errors are reported | Pass |
| PD-07 | Test representative pages at 390 × 844 | Overview, Country Explorer, and Model Performance show no horizontal page overflow | Pass |
| PD-08 | Inspect historical-data notices | Global end date of December 2015 and country-summary end date of 2012 are visible | Pass |

The initial Model Performance route required normal chart-rendering time after page load. Once rendering completed, all five expected Plotly charts were present.

No deployment-specific functional defects were identified.

## Testing Conclusion

Testing produced the following results:

- all 19 automated tests passed;
- all 47 local functional tests passed;
- all 10 responsive-layout tests passed;
- all 12 manual accessibility tests passed;
- Chrome, Safari, and Firefox compatibility tests passed;
- all five external-link tests passed;
- all eight post-deployment checks passed;
- all identified defects were corrected and successfully retested;
- no unresolved local or deployment-specific functional defects were identified.

Two non-failing third-party compatibility warnings remain documented for future dependency review.
