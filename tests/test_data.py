import numpy as np
import pytest
from htn.data.validate import clean, validate


def test_validate_report(df, cfg):
    r = validate(df, cfg)
    assert r["n_rows"] == len(df)
    assert "class_balance" in r


def test_validate_missing_column(df, cfg):
    with pytest.raises(ValueError):
        validate(df.drop(columns=["bmi"]), cfg)


def test_clean_flags_out_of_range(df, cfg):
    df.loc[0, "bmi"] = 999
    out = clean(df, cfg)
    assert out["bmi"].isna().sum() >= 1 and out["bmi"].max() < 999
