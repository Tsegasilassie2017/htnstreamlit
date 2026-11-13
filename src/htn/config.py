"""Central configuration loader."""
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]


def load_config(path: str | Path = ROOT / "config" / "config.yaml") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def feature_lists(cfg: dict) -> tuple[list[str], list[str]]:
    """Return (categorical, numeric) after applying the exclude list."""
    excl = set(cfg["features"].get("exclude") or [])
    cat = [c for c in cfg["features"]["categorical"] if c not in excl]
    num = [c for c in cfg["features"]["numeric"] if c not in excl]
    return cat, num


def resolve(cfg_path: str) -> Path:
    return ROOT / cfg_path
