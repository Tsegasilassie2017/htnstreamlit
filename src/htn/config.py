"""Central configuration loader and feature-list helpers."""
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]


def load_config(path: str | Path | None = None) -> dict:
    """Load YAML configuration; default to the repository config file."""
    config_path = Path(path) if path else ROOT / "config" / "config.yaml"
    if not config_path.is_absolute():
        config_path = ROOT / config_path
    with config_path.open("r", encoding="utf-8") as stream:
        return yaml.safe_load(stream)


def feature_lists(cfg: dict) -> tuple[list[str], list[str]]:
    """Return active (categorical, numeric) features after exclusions."""
    excluded = set(cfg.get("features", {}).get("exclude") or [])
    categorical = [
        name for name in cfg["features"].get("categorical", [])
        if name not in excluded
    ]
    numeric = [
        name for name in cfg["features"].get("numeric", [])
        if name not in excluded
    ]
    return categorical, numeric


def resolve(cfg_path: str | Path) -> Path:
    """Resolve a configured repository path, preserving absolute paths."""
    path = Path(cfg_path)
    return path if path.is_absolute() else ROOT / path
