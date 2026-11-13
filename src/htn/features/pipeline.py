"""Step 4: preprocessing. Fitted INSIDE the model pipeline, so no data leakage in CV."""
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from htn.config import feature_lists


def build_preprocessor(cfg: dict) -> ColumnTransformer:
    cat, num = feature_lists(cfg)
    numeric = Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("scale", StandardScaler()),
    ])
    categorical = Pipeline([
        ("impute", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ])
    return ColumnTransformer([("num", numeric, num), ("cat", categorical, cat)])
