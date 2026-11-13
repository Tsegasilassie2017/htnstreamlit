"""Step 2: data validation, quality report and cleaning."""
import numpy as np
import pandas as pd
from htn.config import feature_lists


def validate(df: pd.DataFrame, cfg: dict) -> dict:
    """Check schema and return a data-quality report. Raises on fatal problems."""
    cat, num = feature_lists(cfg)
    target = cfg["data"]["target"]
    missing_cols = [c for c in cat + num + [target] if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    report = {
        "n_rows": int(len(df)),
        "n_duplicates": int(df.duplicated().sum()),
        "target_missing": int(df[target].isna().sum()),
        "class_balance": df[target].value_counts(normalize=True).round(4).to_dict(),
        "missing_pct": (df[cat + num].isna().mean() * 100).round(2).to_dict(),
        "out_of_range": {},
    }
    for col, (lo, hi) in (cfg.get("ranges") or {}).items():
        if col in df.columns:
            bad = ((df[col] < lo) | (df[col] > hi)).sum()
            if bad:
                report["out_of_range"][col] = int(bad)
    return report


def clean(df: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    """Drop duplicates / missing target; set implausible values to NaN (imputed later)."""
    target = cfg["data"]["target"]
    df = df.drop_duplicates().dropna(subset=[target]).copy()
    df[target] = df[target].astype(int)
    for col, (lo, hi) in (cfg.get("ranges") or {}).items():
        if col in df.columns:
            df.loc[(df[col] < lo) | (df[col] > hi), col] = np.nan
    return df.reset_index(drop=True)
