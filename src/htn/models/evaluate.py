"""Step 7: final, one-time evaluation on the held-out test set."""
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.calibration import CalibrationDisplay
from sklearn.metrics import (ConfusionMatrixDisplay, RocCurveDisplay,
                             accuracy_score, average_precision_score, brier_score_loss,
                             f1_score, precision_score, recall_score, roc_auc_score)

from htn.config import resolve


def evaluate(pipeline, features, test: pd.DataFrame, cfg: dict) -> dict:
    X, y = test[features], test[cfg["data"]["target"]]
    proba = pipeline.predict_proba(X)[:, 1]
    pred = (proba >= cfg["training"]["decision_threshold"]).astype(int)

    metrics = {
        "n_test": int(len(y)),
        "roc_auc": roc_auc_score(y, proba),
        "pr_auc": average_precision_score(y, proba),
        "accuracy": accuracy_score(y, pred),
        "precision": precision_score(y, pred, zero_division=0),
        "recall_sensitivity": recall_score(y, pred),
        "specificity": recall_score(y, pred, pos_label=0),
        "f1": f1_score(y, pred),
        "brier": brier_score_loss(y, proba),
    }
    metrics = {k: round(float(v), 4) if k != "n_test" else v for k, v in metrics.items()}

    figs = resolve(cfg["artifacts"]["figures_dir"])
    figs.mkdir(parents=True, exist_ok=True)
    for name, fn in {
        "roc_curve.png": lambda ax: RocCurveDisplay.from_predictions(y, proba, ax=ax),
        "confusion_matrix.png": lambda ax: ConfusionMatrixDisplay.from_predictions(y, pred, ax=ax),
        "calibration.png": lambda ax: CalibrationDisplay.from_predictions(y, proba, n_bins=10, ax=ax),
    }.items():
        fig, ax = plt.subplots(figsize=(5, 4))
        fn(ax)
        fig.tight_layout()
        fig.savefig(figs / name, dpi=150)
        plt.close(fig)

    out = resolve(cfg["artifacts"]["metrics_path"])
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    return metrics
