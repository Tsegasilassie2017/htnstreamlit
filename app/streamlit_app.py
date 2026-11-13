"""Streamlit front-end. Loads the trained pipeline and predicts hypertension risk."""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import streamlit as st  # noqa: E402

from htn.config import load_config, resolve  # noqa: E402
from htn.labels import CODE_MAPS  # noqa: E402
from htn.models.predict import load_artifact, predict_proba  # noqa: E402

cfg = load_config()
st.set_page_config(page_title="Hypertension Risk", page_icon="🩺")


@st.cache_resource
def get_artifact():
    path = resolve(cfg["artifacts"]["model_path"])
    if not path.exists():
        # Optional: download a released artifact. Set HTN_MODEL_URL (e.g. GitHub Release asset).
        url = os.environ.get("HTN_MODEL_URL")
        if not url:
            raise FileNotFoundError(
                "Model not found. Run `make train` or set HTN_MODEL_URL to a hosted model file.")
        import gdown
        path.parent.mkdir(parents=True, exist_ok=True)
        gdown.download(url, str(path), quiet=False)
    return load_artifact(cfg)


try:
    artifact = get_artifact()
except Exception as e:  # noqa: BLE001
    st.error(f"Error loading model: {e}")
    st.stop()

st.title("Hypertension Prediction App")
st.markdown(
    "Research prototype from a master's thesis in Epidemiology by Tsegasilassie Gebremariam, "
    "Debre Berhan University. **Not a diagnostic tool**: it does not replace a blood pressure "
    "measurement or clinical advice."
)


def choice(label, key):
    options = CODE_MAPS[key]
    return options[st.selectbox(label, list(options))]


with st.form("inputs"):
    st.subheader("Demographics")
    c1, c2 = st.columns(2)
    with c1:
        sex = choice("Sex", "sex")
        marital = choice("Marital status", "marital_status")
        adult = choice("Aged 18 or older", "adult_18")
    with c2:
        edu = choice("Education level", "education")
        occ = choice("Occupation", "occupation")

    st.subheader("Behaviour")
    c1, c2 = st.columns(2)
    with c1:
        cur_smoke = choice("Current smoker", "current_smoking")
        past_smoke = choice("Past smoker", "past_smoking")
        add_salt = choice("Adds salt while eating", "add_salt")
        processed = choice("Eats processed food", "processed_food")
        vig = choice("Vigorous activity at work", "vigorous_work")
        mod = choice("Moderate activity at work", "moderate_work")
    with c2:
        days_fruit = st.number_input("Days fruit eaten per week", 0, 7, 3)
        serv_fruit = st.number_input("Servings of fruit per day", 0.0, 20.0, 1.0, 0.5)
        days_veg = st.number_input("Days vegetables eaten per week", 0, 7, 3)
        serv_veg = st.number_input("Servings of vegetables per day", 0.0, 20.0, 1.0, 0.5)
        salt = st.number_input("Salt intake (grams/day)", 0.0, 50.0, 5.0, 0.5)
        sedentary = st.number_input("Sedentary hours per day", 0.0, 24.0, 6.0, 0.5)

    st.subheader("Clinical measurements")
    c1, c2 = st.columns(2)
    with c1:
        told_bp = choice("Ever told you have high BP", "told_high_bp")
        pulse = st.number_input("Average pulse rate (bpm)", 30, 200, 75)
        bmi = st.number_input("BMI (kg/m²)", 10.0, 70.0, 24.0, 0.1)
    with c2:
        fbg = st.number_input("Fasting blood glucose (mg/dL)", 30.0, 600.0, 90.0, 1.0)
        whr = st.number_input("Waist-to-hip ratio", 0.4, 1.5, 0.9, 0.01)
        chol = st.number_input("Total cholesterol (mg/dL)", 50.0, 500.0, 180.0, 1.0)

    submitted = st.form_submit_button("Predict")

if submitted:
    inputs = dict(
        sex=sex, education=edu, marital_status=marital, occupation=occ, adult_18=adult,
        current_smoking=cur_smoke, past_smoking=past_smoke, days_fruit=days_fruit,
        servings_fruit=serv_fruit, days_veg=days_veg, servings_veg=serv_veg,
        add_salt=add_salt, processed_food=processed, salt_amount=salt,
        vigorous_work=vig, moderate_work=mod, sedentary_hours=sedentary,
        told_high_bp=told_bp, avg_pr=pulse, bmi=bmi, fbg=fbg, whr=whr, chol=chol,
    )
    prob = predict_proba(artifact, inputs)
    threshold = cfg["training"]["decision_threshold"]
    st.metric("Estimated probability of hypertension", f"{prob:.1%}")
    st.progress(min(max(prob, 0.0), 1.0))
    if prob >= threshold:
        st.warning("Higher risk: confirm with a blood pressure measurement at a health facility.")
    else:
        st.success("Lower estimated risk. Regular blood pressure checks are still recommended.")
