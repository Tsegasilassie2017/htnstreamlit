# Harmonized variable dictionary

This is the current working dictionary for the nine country CSV files. The canonical names below refer to cleaned/harmonized outputs, not raw questionnaire columns. Preserve raw source columns and retain a crosswalk from every canonical field to each country's questionnaire item and recoding rule.

## Provisional core predictors

| Canonical variable | Domain | Type | Source / handling | Status |
|---|---|---|---|---|
| `age_years_clean` | Demographic | Numeric, years | Age item; Ethiopia source is C3, other surveys use age | Include; adults 18+ |
| `sex_harmonized` | Demographic | Category | Harmonized labels Female/Male; Ethiopia source C1 (1=Male, 2=Female before recoding) | Include |
| `marital_status_harmonized` | Demographic | Category | Country-specific questionnaire crosswalk | Include after crosswalk check |
| `work_status_harmonized` | Demographic/economic | Category | C8 country-specific recodes; missing/refused kept missing | Include after crosswalk check |
| `waist_clean` | Anthropometry | Numeric, cm | Usually M14; CAR M7. Zero/sentinel and implausible values set missing only after review | Include |
| `bmi_clean` | Anthropometry | Numeric, kg/m² | Derived from cleaned weight and height; do not derive from uncleaned sentinel values | Include |

## Sensitivity candidates

| Canonical variable | Domain | Why sensitivity analysis is needed |
|---|---|---|
| `education_years_clean` | Education | Sudan has structural skips for respondents with XC1=2; overall missingness is about 42.7%. |
| `education_level_model_candidate` | Education | Ethiopia C5 code 5 (498 adults) is unverified; exclude that code pending questionnaire review. |
| `fruit_days_week_clean` | Diet | D1; retain days/week after item-level QC. |
| `vegetable_days_week_clean` | Diet | D3; retain days/week after item-level QC. |
| `fruit_servings_on_eating_day_clean` | Diet | D2; CAR has positive follow-ups despite D1=0 and values as high as 60. Review before modeling; do not cap arbitrarily. |
| `vegetable_servings_on_eating_day_clean` | Diet | D4; CAR has follow-up conflicts after D3=0. Review before modeling. |

Diet missingness is elevated for some derived measures, including fruit in Zambia and both fruit and vegetable measures in Cabo Verde. Compare a demographic/anthropometry model with diet added as a sensitivity model; do not let imputation hide questionnaire skip patterns.

## Not yet harmonized for pooled modeling

Tobacco, alcohol, physical activity, biochemical measures, and household size require questionnaire-by-questionnaire code verification before activation. Raw fields may exist, but no pooled predictor should be created by matching names alone. CAR household-size C9 has 269 zero values and one value of 56; household size is not a current core predictor.

## Outcome and leakage controls

`hypertension` is the binary outcome. Its exact algorithm must be approved against the country questionnaire and study protocol before labels are generated. The source measurements include country-specific repeated SBP/DBP readings and antihypertensive medication. These, plus self-reported hypertension/“told high BP,” are outcome-defining or leakage variables and must never be predictors for this outcome.

Keep country key, survey year, PSU, strata, and survey weights as design/validation metadata where available. Do not treat them as ordinary predictors without a prespecified reason.
