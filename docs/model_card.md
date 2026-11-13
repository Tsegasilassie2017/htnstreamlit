# Model card (update on every retrain)

- **Intended use:** research / screening support in adults. Not a diagnostic device.
- **Outcome definition:** (e.g. SBP >= 140 and/or DBP >= 90 mmHg, or on treatment)
- **Population / data source:** (survey, setting, years, sample size, prevalence)
- **Model:** see `models/model_metadata.json` (type, tuned parameters, CV score, library versions)
- **Test performance:** see `reports/metrics.json` and `reports/figures/`
- **Decision threshold:** `training.decision_threshold` in config (justify: sensitivity vs specificity)
- **Known limitations:** cross-sectional data, possible leakage (`told_high_bp`), self-reported variables,
  single population: external validation needed
- **Ethics:** approval reference, de-identification, data-sharing restrictions
