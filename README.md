# Multi-country hypertension model development

A research codebase for questionnaire-guided data management and development of a hypertension model using adult WHO STEPS country CSV datasets. It is currently at the data harmonization and outcome-definition stage; it does not contain a validated model.

> Research workflow only. Not a diagnostic tool or clinical decision aid.

## Study data

Nine country surveys are in scope: Kenya 2015, Sudan 2016, Benin 2015, Cabo Verde 2020, Central African Republic 2017, Malawi 2017, Sao Tome and Principe 2019, Zambia 2017, and Ethiopia 2015. Use adults aged 18 years and older. Store source CSV files locally under `data/raw/`; survey records are excluded from Git.

## Architecture

```
htnstreamlit/
├── config/config.yaml              # countries, candidate variables, QC and validation status
├── data/{raw,interim,processed}/   # local-only survey files and derived data
├── docs/
│   ├── data_dictionary.md          # questionnaire-informed canonical fields and caveats
│   └── model_card.md               # intended use, current status and limitations
├── notebooks/                      # exploration and error analysis
├── src/htn/
│   ├── config.py                   # YAML loader and feature lists
│   ├── data/                       # ingestion, validation, cleaning and splitting
│   ├── features/pipeline.py        # train-fold imputation, scaling and encoding
│   └── models/                     # training, evaluation and prediction utilities
├── app/streamlit_app.py            # status page; predictions disabled until validation
├── scripts/make_synthetic_data.py  # synthetic-only software smoke-test data
├── tests/                          # pipeline unit tests
└── reports/                         # local metrics and figures
```

## Provisional predictor set

Core candidates currently supported by questionnaire review:

- Demographic: `age_years_clean`, `sex_harmonized`, `marital_status_harmonized`, `work_status_harmonized`
- Anthropometry: `waist_clean`, `bmi_clean`

Education and fruit/vegetable items are sensitivity candidates because of structural skips, unresolved codes, item conflicts, or country-specific missingness. Tobacco, alcohol, physical activity, and biochemical variables stay disabled until the exact questionnaire mappings are checked. See [the data dictionary](docs/data_dictionary.md).

## Workflow

1. Preserve raw country CSV files locally and document source item mappings.
2. Restrict to adults aged 18+; harmonize categories and special codes by questionnaire.
3. Review missingness, skips, sentinel values, outliers, and derived measures without arbitrary capping.
4. Verify and freeze the hypertension label algorithm from measured BP and medication items.
5. Freeze a country-aware validation plan. Previously examined Cabo Verde and Sudan results are exploratory, not untouched external validation.
6. Fit imputation, scaling, and encoding within training folds; compare interpretable and nonlinear models.
7. Evaluate discrimination, calibration, sensitivity, specificity, and country-level variation.
8. Update the model card and app only after validation and review.

## Local setup

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
```

Place the final harmonized adult analysis file at the configured `data.raw_path` only after its schema and outcome have been reviewed. The default pipeline split is marked for software development only and must not be reported as final multi-country validation.

Generate synthetic data for software checks:

```bash
python scripts/make_synthetic_data.py
```

Synthetic output is artificial and must never be combined with study records or used to report epidemiologic/model performance.

## Data protection

Never commit original or participant-level CSV/DTA files, intermediate analysis files, model artifacts, or metrics derived from restricted data. Use local ignored directories and follow the study's data-sharing and ethics requirements.
