"""Create synthetic questionnaire-shaped data for software smoke tests only."""
from pathlib import Path

import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
n = 1800
countries = np.array([
    "ken2015", "sdn2016", "ben2015", "cpv2020", "caf2017",
    "mwi2017", "stp2019", "zmb2017", "eth2015",
])
df = pd.DataFrame({
    "country_key": rng.choice(countries, n),
    "age_years_clean": rng.integers(18, 70, n),
    "sex_harmonized": rng.choice(["Female", "Male"], n),
    "marital_status_harmonized": rng.choice(
        ["Never married", "Married/cohabiting", "Previously married"], n
    ),
    "work_status_harmonized": rng.choice(
        ["Paid work", "Homemaker", "Student", "Unemployed, able to work",
         "Unpaid work", "Retired", "Unable to work"], n
    ),
    "waist_clean": rng.normal(84, 14, n).clip(45, 150),
    "bmi_clean": rng.normal(25, 5, n).clip(14, 55),
})
linear = (
    -4.0
    + 0.055 * (df["age_years_clean"] - 40)
    + 0.018 * (df["waist_clean"] - 85)
    + 0.035 * (df["bmi_clean"] - 25)
)
prob = 1 / (1 + np.exp(-linear))
df["hypertension"] = rng.binomial(1, prob, n).astype("int8")
df.loc[rng.choice(n, 70, replace=False), "waist_clean"] = np.nan
df.loc[rng.choice(n, 55, replace=False), "bmi_clean"] = np.nan

output = Path("data/raw/synthetic_adult_model_dataset.csv")
output.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output, index=False)
print(
    f"Wrote synthetic-only data to {output} "
    f"({len(df):,} rows; prevalence={df['hypertension'].mean():.3f})."
)
