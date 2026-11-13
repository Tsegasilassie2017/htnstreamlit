"""Human-readable labels for coded variables.
!! VERIFY every mapping against your training data dictionary (docs/data_dictionary.md).
   The numeric codes must be IDENTICAL to what the model was trained on."""

YES_NO = {"No": 0, "Yes": 1}

CODE_MAPS = {
    "sex": {"Female": 0, "Male": 1},                                   # TODO verify
    "education": {"No formal education": 0, "Primary": 1, "Secondary": 2,
                  "Diploma": 3, "Degree or higher": 4},                # TODO verify
    "marital_status": {"Single": 0, "Married": 1, "Divorced/Widowed": 2},  # TODO verify
    "occupation": {"Unemployed": 0, "Farmer": 1, "Employee": 2,
                   "Merchant": 3, "Other": 4},                         # TODO verify
    "adult_18": YES_NO, "current_smoking": YES_NO, "past_smoking": YES_NO,
    "add_salt": YES_NO, "processed_food": YES_NO, "vigorous_work": YES_NO,
    "moderate_work": YES_NO, "told_high_bp": YES_NO,
}
