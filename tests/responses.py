"""
Expected response structures and values used in tests.
"""

EXPECTED_SUCCESS_STATUS = "success"

EXPECTED_FAILURE_STATUS = "error"

EXPECTED_RESPONSE_KEYS = [
    "status",
    "answer",
]

EXPECTED_RETRIEVAL_KEYS = [
    "documents",
    "scores",
]

EXPECTED_VALIDATION_KEYS = [
    "is_valid",
    "reason",
]