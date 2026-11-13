"""Research project status page; prediction stays disabled until validation."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import streamlit as st  # noqa: E402
from htn.config import feature_lists, load_config  # noqa: E402

cfg = load_config()
st.set_page_config(page_title="Hypertension Model Development", page_icon="🩺")
st.title("Multi-country hypertension model")
st.caption("WHO STEPS adult survey data | Development and validation workspace")

st.warning(
    "This project is in data harmonization and outcome verification. "
    "No validated model is available, so this app does not generate individual predictions."
)

st.subheader("Current analysis scope")
st.write(
    "Adults aged 18 years and older from nine country surveys. The analysis "
    "uses questionnaire-derived variables after harmonization and quality review."
)
categorical, numeric = feature_lists(cfg)
st.markdown("**Provisional core predictors**")
st.code("\n".join(categorical + numeric), language="text")

st.markdown("**Sensitivity candidates**")
for domain, variables in cfg["features"]["sensitivity_candidates"].items():
    st.write(f"- **{domain.replace('_', ' ').title()}:** " +
             (", ".join(variables) if variables else "not yet mapped"))

st.subheader("Before a model can be enabled")
st.markdown(
    """
1. Verify and document the country-specific hypertension case definition.
2. Freeze the adult harmonized dataset and questionnaire crosswalk.
3. Decide validation by country; previous Cabo Verde and Sudan analyses are exploratory.
4. Fit preprocessing inside cross-validation, evaluate calibration and discrimination,
   and report country-specific performance.
5. Update the model card and enable prediction only after external validation and review.
"""
)
st.caption(
    "Research workflow only. This software is not a diagnostic tool and does not provide "
    "clinical advice. Blood-pressure readings and antihypertensive medication are reserved "
    "for outcome construction and must not enter the predictor set."
)
