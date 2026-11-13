# Hypertension Prediction (htnstreamlit)

Machine-learning model and Streamlit app predicting hypertension from socio-demographic,
behavioural and clinical variables. Built for a master's thesis in Epidemiology
(Tsegasilassie Gebremariam, Debre Berhan University).

> Research prototype. **Not a diagnostic tool.**

## Architecture

```
htnstreamlit/
├── config/config.yaml        # single source of truth: paths, features, ranges, CV, threshold
├── data/
│   ├── raw/                  # original data, read-only, git-ignored
│   ├── interim/              # intermediate files, git-ignored
│   ├── processed/            # train.csv / test.csv, git-ignored
│   └── external/             # reference data, git-ignored
├── notebooks/                # EDA and error analysis only
├── src/htn/
│   ├── config.py             # config loader, feature lists
│   ├── labels.py             # code -> label maps used by the app
│   ├── data/                 # ingest.py, validate.py (quality report + cleaning), split.py
│   ├── features/pipeline.py  # imputation, scaling, encoding (inside the sklearn Pipeline)
│   ├── models/               # train.py (CV compare + tuning), evaluate.py, predict.py
│   └── pipeline.py           # CLI orchestration: data -> train -> evaluate
├── app/streamlit_app.py      # UI (loads the saved pipeline)
├── htnstreamlit.py           # thin entry point kept for existing deployment
├── models/                   # saved pipeline + model_metadata.json
├── reports/                  # metrics.json and figures (ROC, calibration, confusion matrix)
├── tests/                    # pytest: validation, split, training, prediction
├── docs/                     # data dictionary, model card
└── Makefile
```

## Data science workflow

| # | Step | Where | Notes |
|---|------|-------|-------|
| 1 | Define problem and outcome | `docs/model_card.md` | Outcome definition (e.g. SBP ≥ 140 or DBP ≥ 90) |
| 2 | Ingest | `data/ingest.py` | Raw data never modified |
| 3 | Validate and clean | `data/validate.py` | Schema check, duplicates, missingness, implausible values -> NaN |
| 4 | Split | `data/split.py` | Stratified train/test; **test set untouched until step 8** |
| 5 | Preprocess | `features/pipeline.py` | Fitted inside CV folds, so no leakage |
| 6 | Compare baselines | `models/train.py` | Logistic regression, random forest, gradient boosting (stratified CV) |
| 7 | Tune best model | `models/train.py` | RandomizedSearchCV on the primary metric |
| 8 | Final evaluation | `models/evaluate.py` | AUC, PR-AUC, sensitivity, specificity, F1, Brier, calibration |
| 9 | Persist | `models/train.py` | Pipeline + feature order + library versions |
| 10 | Serve | `app/streamlit_app.py` | Named columns, probability output, disclaimer |
| 11 | Monitor / document | `docs/` | Update model card on every retrain |

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
make install
# put your dataset at data/raw/htn_dataset.csv and set the `target` column in config/config.yaml
make data       # validate, clean, split
make train      # compare models, tune, save models/htn_pipeline.joblib
make evaluate   # test-set metrics and figures in reports/
make app        # streamlit run htnstreamlit.py
make test
```

No data yet? `make synthetic` creates fake data to smoke-test the pipeline.

## Before you trust the results

- [ ] Edit `config/config.yaml` column names to match your dataset exactly.
- [ ] Fill `docs/data_dictionary.md` and verify `src/htn/labels.py` codes match your encoding.
- [ ] Check `told_high_bp` for outcome leakage (add it to `features.exclude` and compare).
- [ ] Confirm units for `fbg` and `chol`, and that `whr` is waist-to-hip ratio.
- [ ] Pin `scikit-learn` / `joblib` in `requirements.txt` to the versions in `models/model_metadata.json`.
- [ ] Host the trained model (GitHub Release / Git LFS) and set `HTN_MODEL_URL` for deployment.
- [ ] Never commit participant-level data (`.gitignore` already blocks `data/*`).
