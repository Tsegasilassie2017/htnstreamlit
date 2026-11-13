"""Step 1: load raw data (read-only, never modify files in data/raw)."""
import pandas as pd
from htn.config import resolve


def load_raw(cfg: dict) -> pd.DataFrame:
    path = resolve(cfg["data"]["raw_path"])
    if not path.exists():
        raise FileNotFoundError(
            f"Raw dataset not found at {path}. Place your CSV there (it is git-ignored)."
        )
    return pd.read_csv(path)
