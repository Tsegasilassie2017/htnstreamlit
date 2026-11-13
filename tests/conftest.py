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
    categorical, numeric = feature_lists(cfg)
    n = 300
    data = {
        "country_key": rng.choice(
            ["ken2015", "sdn2016", "ben2015", "cpv2020", "eth2015"], n
        ),
        "age_years_clean": rng.integers(18, 70, n),
    }
    for column in categorical:
        if column == "sex_harmonized":
            data[column] = rng.choice(["Female", "Male"], n)
        elif column == "marital_status_harmonized":
            data[column] = rng.choice(
                ["Never married", "Married/cohabiting", "Previously married"], n
            )
        else:
            data[column] = rng.choice(["Paid work", "Homemaker", "Student"], n)
    for column in numeric:
        data[column] = rng.uniform(15, 45, n)
    frame = pd.DataFrame(data)
    frame["hypertension"] = (
        frame["age_years_clean"] + rng.normal(0, 15, n) > 45
    ).astype(int)
    return frame
