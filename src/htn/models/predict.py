"""Step 8: inference. Used by the Streamlit app; guarantees column names and order."""
import joblib
import pandas as pd
from htn.config import load_config, resolve


def load_artifact(cfg: dict | None = None) -> dict:
    cfg = cfg or load_config()
    return joblib.load(resolve(cfg["artifacts"]["model_path"]))


def predict_proba(artifact: dict, inputs: dict) -> float:
    """inputs: {feature_name: value}. Returns probability of hypertension."""
    X = pd.DataFrame([inputs])[artifact["features"]]
    return float(artifact["pipeline"].predict_proba(X)[0, 1])
