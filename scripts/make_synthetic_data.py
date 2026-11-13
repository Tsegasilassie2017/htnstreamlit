"""Generate a SYNTHETIC dataset to smoke-test the pipeline (not real data!)."""
import numpy as np
import pandas as pd

rng = np.random.default_rng(0)
n = 1500
df = pd.DataFrame({
    "sex": rng.integers(0, 2, n), "education": rng.integers(0, 5, n),
    "marital_status": rng.integers(0, 3, n), "occupation": rng.integers(0, 5, n),
    "adult_18": 1, "current_smoking": rng.integers(0, 2, n), "past_smoking": rng.integers(0, 2, n),
    "days_fruit": rng.integers(0, 8, n), "servings_fruit": rng.uniform(0, 5, n),
    "days_veg": rng.integers(0, 8, n), "servings_veg": rng.uniform(0, 5, n),
    "add_salt": rng.integers(0, 2, n), "processed_food": rng.integers(0, 2, n),
    "salt_amount": rng.uniform(1, 15, n), "vigorous_work": rng.integers(0, 2, n),
    "moderate_work": rng.integers(0, 2, n), "sedentary_hours": rng.uniform(1, 14, n),
    "told_high_bp": rng.integers(0, 2, n), "avg_pr": rng.normal(75, 10, n).round(),
    "bmi": rng.normal(24, 4, n), "fbg": rng.normal(95, 20, n),
    "whr": rng.normal(0.9, 0.07, n), "chol": rng.normal(180, 35, n),
})
logit = (0.08 * (df.bmi - 24) + 0.03 * (df.fbg - 95) + 0.1 * df.salt_amount
         + 0.5 * df.told_high_bp + 0.4 * df.current_smoking - 2.5)
df["hypertension"] = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)
df.loc[rng.choice(n, 40, replace=False), "bmi"] = np.nan  # some missingness
df.to_csv("data/raw/htn_dataset.csv", index=False)
print("Wrote data/raw/htn_dataset.csv", df.shape, "prevalence:", df.hypertension.mean().round(3))
