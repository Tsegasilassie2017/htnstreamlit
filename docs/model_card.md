# Model card: multi-country adult hypertension model

## Status
**Pre-model development. No validated model is currently available.** The app therefore does not calculate individual predictions.

## Intended project
Develop and validate a research model for prevalent hypertension among adults aged 18 years or older in nine WHO STEPS country surveys: Kenya (2015), Sudan (2016), Benin (2015), Cabo Verde (2020), Central African Republic (2017), Malawi (2017), Sao Tome and Principe (2019), Zambia (2017), and Ethiopia (2015).

## Outcome
Working target column: `hypertension`. The exact case algorithm using measured repeated blood-pressure readings and/or antihypertensive medication has not yet been verified and frozen. No final model fitting or performance claim should be made until this step is complete.

## Candidate predictors
Provisional core: age, sex, marital status, work status, waist circumference, and BMI using harmonized canonical columns in `config/config.yaml`. Education and diet are sensitivity candidates. Tobacco, alcohol, physical activity, and biochemical variables remain disabled until questionnaire crosswalks are verified.

## Validation
Prior analyses used Cabo Verde and Sudan as held-out countries and examined their outcomes. Those results are exploratory and must not be described as untouched external validation. Freeze a new validation plan, use country-aware validation, report performance by country, and assess calibration as well as discrimination.

## Known data limitations
- Sudan education missingness is largely structural due to the XC1 skip pattern.
- Ethiopia education code 5 remains unresolved.
- CAR household size and fruit/vegetable follow-up items contain values requiring source review.
- Some diet variables have elevated country-specific missingness.
- Cross-sectional prevalence prediction is not future disease-risk prediction.

## Use and safeguards
Research use only. Not a diagnostic device or clinical decision aid. Do not put blood-pressure readings, antihypertensive medication, or self-reported hypertension into the predictors. No participant-level survey data or trained model artifact should be committed to the public repository without authorization and a privacy review.
