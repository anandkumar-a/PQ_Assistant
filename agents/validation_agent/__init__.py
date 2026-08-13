"""
Validation Agent
----------------

This package validates generated responses before they are
returned to the user.

Responsibilities:
    - Validate response quality
    - Check for empty responses
    - Check whether relevant documents were retrieved
    - Identify possible unsupported responses
    - Assign a validation status
"""

from .validation_agent import ValidationAgent

__all__ = [
    "ValidationAgent",
]