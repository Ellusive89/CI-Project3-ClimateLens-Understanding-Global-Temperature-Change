"""Ethics, privacy, legal, and governance page for ClimateLens."""

import pandas as pd
import streamlit as st

from src.ui import (
    render_footer,
    render_page_header,
)


render_page_header(
    eyebrow="Responsible practice",
    title="Ethics and Data Governance",
    introduction=(
        "Understand how ClimateLens addresses privacy, licensing, "
        "bias, uncertainty, social implications, responsible model "
        "use, and transparent data governance."
    ),
)

st.info(
    "This page provides an educational assessment of responsible "
    "data practice. It is not legal advice.",
    icon="ℹ️",
)


summary_columns = st.columns(4)

with summary_columns[0]:
    st.metric(
        label="Personal data in source files",
        value="None identified",
        help=(
            "The analytical files contain temperature, time, "
            "uncertainty, and geographical labels—not information "
            "about identifiable living people."
        ),
    )

with summary_columns[1]:
    st.metric(
        label="Kaggle snapshot licence",
        value="CC BY-NC-SA 4.0",
        help=(
            "Attribution, non-commercial use, and share-alike "
            "conditions apply to the Kaggle dataset snapshot."
        ),
    )

with summary_columns[2]:
    st.metric(
        label="Dataset status",
        value="Historical",
        help=(
            "The global data ends in 2015 and complete country "
            "summaries end in 2012."
        ),
    )

with summary_columns[3]:
    st.metric(
        label="Model use",
        value="Educational only",
        help=(
            "The model is a historical prototype, not a "
            "professional climate projection."
        ),
    )

st.warning(
    "Low privacy risk does not mean zero governance responsibility. "
    "Licensing, provenance, accuracy, accessibility, security, "
    "misinterpretation, and model misuse still require controls.",
    icon="⚠️",
)

st.divider()

ethics_tab, privacy_tab, governance_tab, risk_tab = st.tabs([
    "Ethics and social impact",
    "Privacy and legal",
    "Data governance",
    "Risk register",
])

# ------------------------------------------------------------------
# Ethics and social impact
# ------------------------------------------------------------------

with ethics_tab:
    st.header("Ethical considerations")

    st.subheader("Historical and geographical bias")

    st.write(
        "Historical measurement coverage is not uniform across "
        "time or location. Earlier periods generally contain "
        "greater reported uncertainty, and some regions may have "
        "fewer or less representative observations."
    )

    st.markdown(
        "- The dashboard displays uncertainty alongside temperature.\n"
        "- Missing measurements are not silently imputed.\n"
        "- Comparisons use complete years where possible.\n"
        "- Country-specific anomalies are preferred over absolute "
        "temperature rankings.\n"
        "- Geographical labels are described as dataset labels rather "
        "than assumed to be current sovereign states."
    )

    st.subheader("Fair communication")

    communication_columns = st.columns(2)

    with communication_columns[0]:
        st.markdown("#### Practices used")

        st.markdown(
            "- Plain-language explanations accompany technical metrics.\n"
            "- Chart axes include units and reference periods.\n"
            "- Colour is supplemented by labels and line styles.\n"
            "- Model performance is compared with a baseline.\n"
            "- Limitations appear near the relevant result.\n"
            "- Users control filters and downloads."
        )

    with communication_columns[1]:
        st.markdown("#### Practices avoided")

        st.markdown(
            "- Presenting historical data as current monitoring\n"
            "- Treating correlation as causation\n"
            "- Ranking countries by climate responsibility\n"
            "- Hiding measurement uncertainty\n"
            "- Reporting model R² without error metrics\n"
            "- Presenting the prototype as a climate projection"
        )

    st.subheader("Social implications")

    st.write(
        "Climate information can influence public understanding, "
        "education, organisational planning, and policy discussion. "
        "Poor communication could encourage either unjustified alarm "
        "or unjustified dismissal of evidence."
    )

    st.markdown(
        "- Country averages can hide local and community-level impacts.\n"
        "- Temperature change does not measure vulnerability or resilience.\n"
        "- Temperature change does not measure historical emissions.\n"
        "- Communities contributing least to emissions may experience "
        "substantial impacts.\n"
        "- Findings should be combined with authoritative scientific and "
        "social evidence before supporting real decisions."
    )

    st.subheader("Generative AI transparency")

    st.write(
        "Generative AI was used to support ideation, structure, code "
        "explanations, and communication. The project author remains "
        "responsible for executing, reviewing, testing, documenting, "
        "and interpreting the work."
    )

    st.markdown(
        "- AI-generated suggestions were checked against actual outputs.\n"
        "- Statistical values were calculated from the project data.\n"
        "- AI did not replace the original data source.\n"
        "- External sources and licences are credited.\n"
        "- AI assistance must also be acknowledged in the README."
    )

# ------------------------------------------------------------------
# Privacy and legal
# ------------------------------------------------------------------

with privacy_tab:
    st.header("Privacy and legal considerations")

    st.subheader("GDPR relevance")

    st.write(
        "GDPR applies to information relating to an identified or "
        "identifiable living individual. The project temperature "
        "datasets contain dates, measurements, uncertainties, and "
        "geographical labels, but no person-level records."
    )

    st.success(
        "The analytical dataset itself presents low GDPR risk because "
        "no personal data has been identified in its fields.",
        icon="✅",
    )

    st.write(
        "However, a deployed application may generate technical "
        "server logs. Depending on the hosting configuration, those "
        "logs could include IP addresses or other online identifiers. "
        "The hosting provider's privacy and retention documentation "
        "must therefore be reviewed before production use."
    )

    st.markdown(
        "- The application does not request names or email addresses.\n"
        "- It does not provide user-upload functionality.\n"
        "- It does not intentionally collect precise user location.\n"
        "- It does not create user profiles or automated decisions.\n"
        "- No advertising or third-party analytics are intentionally added.\n"
        "- Privacy impact must be reassessed if the scope changes."
    )

    with st.expander("GDPR principles relevant to future changes"):
        st.markdown(
            "- **Lawfulness, fairness and transparency:** explain what "
            "personal data is collected and why.\n"
            "- **Purpose limitation:** use personal data only for a "
            "clearly stated purpose.\n"
            "- **Data minimisation:** collect only what is necessary.\n"
            "- **Accuracy:** correct inaccurate personal data.\n"
            "- **Storage limitation:** define review and deletion periods.\n"
            "- **Integrity and confidentiality:** protect data from "
            "unauthorised access or loss.\n"
            "- **Accountability:** document and demonstrate compliance."
        )

    gdpr_reference_html = (
        '<p>Authoritative references: '
        '<a '
        'href="https://commission.europa.eu/law/law-topic/'
        'data-protection/information-business-and-organisations/'
        'application-gdpr_en" '
        'target="_blank" '
        'rel="noopener noreferrer">'
        'European Commission: application of the GDPR'
        '</a> and '
        '<a '
        'href="https://commission.europa.eu/law/law-topic/'
        'data-protection/information-business-and-organisations/'
        'principles-gdpr_en" '
        'target="_blank" '
        'rel="noopener noreferrer">'
        'principles of GDPR processing'
        '</a>. External links open in a separate tab.</p>'
    )

    st.markdown(
        gdpr_reference_html,
        unsafe_allow_html=True,
    )

    st.divider()

    st.subheader("Dataset licence and attribution")

    st.write(
        "The Kaggle dataset page identifies the downloaded snapshot "
        "as CC BY-NC-SA 4.0. Berkeley Earth describes its data more "
        "generally as CC BY-NC 4.0 for non-commercial use. The project "
        "therefore follows the more specific conditions shown with "
        "the downloaded Kaggle snapshot."
    )

    st.markdown(
        "- **BY — Attribution:** credit Kaggle and Berkeley Earth.\n"
        "- **NC — Non-commercial:** use the dataset for this educational, "
        "non-commercial project.\n"
        "- **SA — Share alike:** distribute adapted material under the "
        "required compatible terms.\n"
        "- Preserve source and licence information in the README.\n"
        "- Recheck licensing before commercial reuse or redistribution."
    )

    licence_reference_html = (
        '<p>Licence references: '
        '<a '
        'href="https://www.kaggle.com/datasets/berkeleyearth/'
        'climate-change-earth-surface-temperature-data" '
        'target="_blank" '
        'rel="noopener noreferrer">'
        'Kaggle dataset page'
        '</a>, '
        '<a '
        'href="https://berkeleyearth.org/data/" '
        'target="_blank" '
        'rel="noopener noreferrer">'
        'Berkeley Earth data page'
        '</a>, and '
        '<a '
        'href="https://creativecommons.org/licenses/by-nc-sa/4.0/" '
        'target="_blank" '
        'rel="noopener noreferrer">'
        'CC BY-NC-SA 4.0 summary'
        '</a>. External links open in a separate tab.</p>'
    )

    st.markdown(
        licence_reference_html,
        unsafe_allow_html=True,
    )

# ------------------------------------------------------------------
# Data governance
# ------------------------------------------------------------------

with governance_tab:
    st.header("Data-governance approach")

    st.subheader("Data lifecycle")

    st.markdown(
        "1. **Acquire:** download the documented Kaggle snapshot.\n"
        "2. **Preserve:** retain unchanged raw files under `data/raw/v1/`.\n"
        "3. **Inspect:** validate structure, dates, missingness, and duplicates.\n"
        "4. **Clean:** document each transformation in a Jupyter notebook.\n"
        "5. **Version:** save cleaned outputs under `data/processed/v1/`.\n"
        "6. **Analyse:** create complete-year analytical summaries.\n"
        "7. **Model:** use chronological validation and a baseline comparison.\n"
        "8. **Publish:** display limitations, provenance, and intended use.\n"
        "9. **Maintain:** recheck links, dependencies, data currency, and tests.\n"
        "10. **Retire or update:** archive superseded versions without silently "
        "overwriting their historical provenance."
    )

    st.subheader("Data inventory")

    data_inventory = pd.DataFrame([
        {
            "Asset": "GlobalTemperatures.csv",
            "Classification": "Public historical environmental data",
            "Location": "data/raw/v1",
            "Treatment": "Immutable raw source",
        },
        {
            "Asset": "GlobalLandTemperaturesByCountry.csv",
            "Classification": "Public historical environmental data",
            "Location": "data/raw/v1",
            "Treatment": "Immutable raw source",
        },
        {
            "Asset": "Cleaned monthly files",
            "Classification": "Derived environmental data",
            "Location": "data/processed/v1",
            "Treatment": "Reproducible notebook output",
        },
        {
            "Asset": "Annual analytical summaries",
            "Classification": "Derived analytical data",
            "Location": "data/processed/v1",
            "Treatment": "Dashboard input",
        },
        {
            "Asset": "Model metrics and predictions",
            "Classification": "Derived model output",
            "Location": "data/processed/v1",
            "Treatment": "Educational evaluation only",
        },
    ])

    st.dataframe(
        data_inventory,
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Governance controls")

    governance_columns = st.columns(2)

    with governance_columns[0]:
        st.markdown("#### Technical controls")

        st.markdown(
            "- Raw and processed data are separated.\n"
            "- Data outputs use explicit version folders.\n"
            "- Validation assertions are included in notebooks.\n"
            "- Random model splitting is avoided.\n"
            "- Secrets and Kaggle credentials are ignored by Git.\n"
            "- Commit history documents individual changes."
        )

    with governance_columns[1]:
        st.markdown("#### Organisational controls")

        st.markdown(
            "- The project purpose and audience are documented.\n"
            "- Data and model limitations are visible to users.\n"
            "- Licences and sources are credited.\n"
            "- New data versions require renewed validation.\n"
            "- Domain-expert review is required before operational use.\n"
            "- User feedback should be recorded and prioritised."
        )

    st.subheader("Maintenance and update policy")

    st.markdown(
        "- Review external links before each assessed release.\n"
        "- Review dependency versions and security notices regularly.\n"
        "- Do not silently replace Version 1 data.\n"
        "- Add future datasets under a new version folder.\n"
        "- Rerun all notebooks after a data or dependency update.\n"
        "- Compare new metrics against the documented Version 1 results.\n"
        "- Retest responsive layout and accessibility after UI changes.\n"
        "- Record known defects and corrective actions."
    )

# ------------------------------------------------------------------
# Risk register
# ------------------------------------------------------------------

with risk_tab:
    st.header("Project risk register")

    st.write(
        "The risk register records foreseeable harms, their potential "
        "impact, and the controls used to reduce them."
    )

    risk_register = pd.DataFrame([
        {
            "Risk": "Historical data presented as current",
            "Likelihood": "Medium",
            "Impact": "High",
            "Mitigation": (
                "Display end dates and historical-data notices "
                "throughout the dashboard."
            ),
            "Monitoring": "Review wording on every release",
        },
        {
            "Risk": "Temperature difference treated as causation",
            "Likelihood": "Medium",
            "Impact": "High",
            "Mitigation": (
                "Use association language and provide causal caveats."
            ),
            "Monitoring": "Review narratives and chart captions",
        },
        {
            "Risk": "Geographical coverage bias is overlooked",
            "Likelihood": "Medium",
            "Impact": "Medium",
            "Mitigation": (
                "Show uncertainty and document historical coverage limits."
            ),
            "Monitoring": "Reassess when data is updated",
        },
        {
            "Risk": "Country ranking implies responsibility",
            "Likelihood": "Medium",
            "Impact": "High",
            "Mitigation": (
                "Label rankings as descriptive temperature comparisons "
                "and display responsibility warnings."
            ),
            "Monitoring": "User testing and content review",
        },
        {
            "Risk": "Predictive prototype is used as a projection",
            "Likelihood": "Medium",
            "Impact": "High",
            "Mitigation": (
                "Publish a model card and prohibit professional use."
            ),
            "Monitoring": "Review all model-page language",
        },
        {
            "Risk": "Licence conditions are breached",
            "Likelihood": "Low",
            "Impact": "High",
            "Mitigation": (
                "Maintain attribution, non-commercial use, licence links, "
                "and share-alike documentation."
            ),
            "Monitoring": "Licence review before redistribution",
        },
        {
            "Risk": "Deployment logs create privacy obligations",
            "Likelihood": "Medium",
            "Impact": "Medium",
            "Mitigation": (
                "Review host logging and retention; avoid unnecessary "
                "analytics and user identifiers."
            ),
            "Monitoring": "Review hosting privacy documentation",
        },
        {
            "Risk": "Dashboard becomes inaccessible",
            "Likelihood": "Low",
            "Impact": "Medium",
            "Mitigation": (
                "Use contrast, units, text alternatives, keyboard-friendly "
                "controls, and colour-independent chart distinctions."
            ),
            "Monitoring": "Responsive and accessibility testing",
        },
    ])

    st.dataframe(
        risk_register,
        use_container_width=True,
        hide_index=True,
    )

    risk_csv = risk_register.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download risk register as CSV",
        data=risk_csv,
        file_name="climatelens_risk_register.csv",
        mime="text/csv",
    )

    st.subheader("Residual risk")

    st.write(
        "The controls reduce foreseeable harm but cannot remove every "
        "risk. The most important remaining risks are misinterpretation, "
        "outdated data, uneven historical coverage, and use outside the "
        "dashboard's educational purpose."
    )

render_footer()
