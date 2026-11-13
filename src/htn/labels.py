"""Questionnaire harmonization labels.

Keep source codes and country-specific mappings in the data-management
crosswalk. This module only documents the canonical labels emitted by that
harmonization; it must not guess raw questionnaire codes.
"""

CANONICAL_LABELS = {
    "sex_harmonized": ["Female", "Male"],
    "education_level_model_candidate": [
        "No formal schooling",
        "Below primary",
        "Primary completed",
        "Secondary",
        "Tertiary or higher",
    ],
}

# The outcome is not constructed here. Confirm country-specific BP and
# medication coding against each STEPS questionnaire and the analysis protocol.
OUTCOME_COLUMN = "hypertension"
OUTCOME_STATUS = "pending_questionnaire_and_protocol_verification"
