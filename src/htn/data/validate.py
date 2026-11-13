"""Data schema, adult-population and outcome validation."""
import numpy as np
import pandas as pd
from htn.config import feature_lists


def validate(df: pd.DataFrame, cfg: dict) -> dict:
    """Check required columns, adult eligibility and binary outcome coding."""
    categorical, numeric = feature_lists(cfg)
    target = cfg["data"]["target"]
    country_col = cfg["data"].get("country_column")
    required = categorical + numeric + [target, cfg["data"]["adult_age_column"]]
    if country_col:
        required.append(country_col)
    missing_cols = [column for column in required if column not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    outcome_status = cfg.get("outcome", {}).get("status", "")
    age = pd.to_numeric(df[cfg["data"]["adult_age_column"]], errors="coerce")
    target_values = set(pd.to_numeric(df[target], errors="coerce").dropna().unique())
    if not target_values.issubset({0, 1}):
        raise ValueError(f"{target} must contain only 0/1 after outcome derivation.")

    leakage = set(cfg.get("outcome", {}).get("predictors_must_exclude", []))
    active_features = set(categorical + numeric)
    leakage_in_features = sorted(active_features & leakage)
    if leakage_in_features:
        raise ValueError(
            "Outcome-defining variables cannot be predictors: "
            f"{leakage_in_features}"
        )

    return {
        "n_rows": int(len(df)),
        "n_duplicates": int(df.duplicated().sum()),
        "adult_rows": int((age >= cfg["data"]["minimum_age_years"]).sum()),
        "underage_or_age_missing": int(
            (age < cfg["data"]["minimum_age_years"]).sum() + age.isna().sum()
        ),
        "target_missing": int(df[target].isna().sum()),
        "target_values": sorted(target_values),
        "target_prevalence": float(pd.to_numeric(df[target], errors="coerce").mean()),
        "outcome_definition_status": outcome_status,
        "country_counts": (
            df[country_col].value_counts(dropna=False).to_dict()
            if country_col else {}
        ),
        "missing_pct": (
            df[categorical + numeric].isna().mean().mul(100).round(2).to_dict()
        ),
        "outcome_leakage_features": leakage_in_features,
    }


def clean(df: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    """Apply adult eligibility and remove duplicate/missing-outcome rows.

    Raw predictor values are not capped or overwritten here. Sentinel-code
    handling and implausible-value review belong in country-specific
    preprocessing, with an audit trail.
    """
    target = cfg["data"]["target"]
    age_col = cfg["data"]["adult_age_column"]
    age = pd.to_numeric(df[age_col], errors="coerce")
    outcome = pd.to_numeric(df[target], errors="coerce")
    df = df.loc[
        age.ge(cfg["data"]["minimum_age_years"]) & outcome.isin([0, 1])
    ].copy()
    df[target] = outcome.loc[df.index].astype("int8")
    return df.drop_duplicates().reset_index(drop=True)
