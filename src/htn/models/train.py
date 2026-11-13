"""Steps 5-6: model comparison and hyper-parameter tuning."""
import json
from datetime import datetime, timezone

import joblib
import pandas as pd
import sklearn
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import (RandomizedSearchCV, StratifiedKFold,
                                     cross_validate)
from sklearn.pipeline import Pipeline

from htn.config import assert_modeling_ready, feature_lists, resolve
from htn.features.pipeline import build_preprocessor


def candidates(seed: int) -> dict:
    return {
        "logistic_regression": LogisticRegression(max_iter=1000, class_weight="balanced"),
        "random_forest": RandomForestClassifier(
            n_estimators=300, class_weight="balanced", random_state=seed, n_jobs=-1),
        "gradient_boosting": GradientBoostingClassifier(random_state=seed),
    }


SEARCH_SPACES = {
    "logistic_regression": {"model__C": [0.01, 0.1, 1, 10, 100]},
    "random_forest": {
        "model__n_estimators": [200, 400, 600],
        "model__max_depth": [None, 5, 10, 20],
        "model__min_samples_leaf": [1, 2, 5, 10],
        "model__max_features": ["sqrt", "log2"],
    },
    "gradient_boosting": {
        "model__n_estimators": [100, 200, 400],
        "model__learning_rate": [0.01, 0.05, 0.1],
        "model__max_depth": [2, 3, 4],
        "model__subsample": [0.7, 0.85, 1.0],
    },
}


def _pipe(cfg, model) -> Pipeline:
    return Pipeline([("prep", build_preprocessor(cfg)), ("model", model)])


def compare_models(train: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    """Cross-validated comparison on training data only."""
    assert_modeling_ready(cfg)
    categorical, numeric = feature_lists(cfg)
    X, y = train[categorical + numeric], train[cfg["data"]["target"]]
    cv = StratifiedKFold(cfg["training"]["cv_folds"], shuffle=True,
                         random_state=cfg["random_state"])
    rows = []
    for name, model in candidates(cfg["random_state"]).items():
        result = cross_validate(
            _pipe(cfg, model), X, y, cv=cv,
            scoring=["roc_auc", "average_precision", "recall", "f1"],
        )
        rows.append({
            "model": name,
            **{
                key.replace("test_", ""): values.mean().round(4)
                for key, values in result.items() if key.startswith("test_")
            },
        })
    return pd.DataFrame(rows).sort_values(
        cfg["training"]["primary_metric"], ascending=False
    )


def tune_and_fit(train: pd.DataFrame, cfg: dict, model_name: str):
    assert_modeling_ready(cfg)
    categorical, numeric = feature_lists(cfg)
    X, y = train[categorical + numeric], train[cfg["data"]["target"]]
    cv = StratifiedKFold(cfg["training"]["cv_folds"], shuffle=True,
                         random_state=cfg["random_state"])
    search = RandomizedSearchCV(
        _pipe(cfg, candidates(cfg["random_state"])[model_name]),
        SEARCH_SPACES[model_name],
        n_iter=cfg["training"]["tuning_iterations"],
        scoring=cfg["training"]["primary_metric"],
        cv=cv, random_state=cfg["random_state"], n_jobs=-1, refit=True,
    )
    search.fit(X, y)
    return search.best_estimator_, search.best_params_, float(search.best_score_)


def save_artifact(pipeline, cfg, model_name, best_params, cv_score):
    assert_modeling_ready(cfg)
    categorical, numeric = feature_lists(cfg)
    features = categorical + numeric
    model_path = resolve(cfg["artifacts"]["model_path"])
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"pipeline": pipeline, "features": features}, model_path)
    meta = {
        "model": model_name,
        "best_params": {
            key: (value if isinstance(value, (int, float, str, type(None))) else str(value))
            for key, value in best_params.items()
        },
        "cv_score": round(cv_score, 4),
        "metric": cfg["training"]["primary_metric"],
        "features": features,
        "trained_at": datetime.now(timezone.utc).isoformat(),
        "sklearn_version": sklearn.__version__,
        "joblib_version": joblib.__version__,
    }
    metadata_path = resolve(cfg["artifacts"]["metadata_path"])
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    with metadata_path.open("w", encoding="utf-8") as stream:
        json.dump(meta, stream, indent=2)
    return meta
