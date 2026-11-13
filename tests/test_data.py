import pytest
from htn.data.validate import clean, validate


def test_validate_report(df, cfg):
    report = validate(df, cfg)
    assert report["n_rows"] == len(df)
    assert report["adult_rows"] == len(df)
    assert report["outcome_leakage_features"] == []


def test_validate_missing_column(df, cfg):
    with pytest.raises(ValueError):
        validate(df.drop(columns=["bmi_clean"]), cfg)


def test_clean_keeps_only_adults_and_binary_outcome(df, cfg):
    df.loc[0, "age_years_clean"] = 17
    df.loc[1, "hypertension"] = None
    cleaned = clean(df, cfg)
    assert cleaned["age_years_clean"].min() >= 18
    assert cleaned["hypertension"].isin([0, 1]).all()
