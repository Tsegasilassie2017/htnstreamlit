import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from htn.config import feature_lists, load_config  # noqa: E402


@pytest.fixture(scope="session")
def cfg():
    return load_config()


@pytest.fixture()
def df(cfg):
    rng = np.random.default_rng(1)
    cat, num = feature_lists(cfg)
    n = 300
    d = pd.DataFrame({c: rng.integers(0, 2, n) for c in cat})
    for c in num:
        d[c] = rng.uniform(1, 5, n)
    d["bmi"] = rng.normal(24, 4, n)
    d[cfg["data"]["target"]] = (d["bmi"] + rng.normal(0, 3, n) > 25).astype(int)
    return d
