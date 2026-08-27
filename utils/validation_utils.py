"""
Validation utilities for the PQ Assistant.

Provides reusable validation helpers for queries, documents,
identifiers, configuration values, and common data types.
"""

import re
from typing import Any, Iterable, Optional


def is_valid_string(
    value: Any,
    min_length: int = 1,
    max_length: Optional[int] = None,
) -> bool:
    """
    Validate that a value is a non-empty string within a length range.

    Args:
        value: Value to validate.
        min_length: Minimum allowed length.
        max_length: Maximum allowed length.

    Returns:
        True if valid, otherwise False.
    """
    if not isinstance(value, str):
        return False

    value = value.strip()

    if len(value) < min_length:
        return False

    if max_length is not None and len(value) > max_length:
        return False

    return True


def is_valid_query(
    query: Any,
    min_length: int = 2,
    max_length: int = 2000,
) -> bool:
    """
    Validate a user query before sending it through the retrieval pipeline.

    Args:
        query: User query.
        min_length: Minimum query length.
        max_length: Maximum query length.

    Returns:
        True if the query is valid, otherwise False.
    """
    return is_valid_string(
        query,
        min_length=min_length,
        max_length=max_length,
    )


def is_valid_document_text(
    text: Any,
    min_length: int = 10,
) -> bool:
    """
    Validate extracted document text.

    Args:
        text: Document text.
        min_length: Minimum required length.

    Returns:
        True if valid document text, otherwise False.
    """
    return is_valid_string(text, min_length=min_length)


def is_valid_identifier(
    identifier: Any,
    pattern: str = r"^[A-Za-z0-9][A-Za-z0-9_-]*$",
) -> bool:
    """
    Validate an identifier such as a document ID, part number, or fault code.

    Args:
        identifier: Identifier to validate.
        pattern: Regular expression pattern.

    Returns:
        True if valid, otherwise False.
    """
    if not isinstance(identifier, str):
        return False

    identifier = identifier.strip()

    return bool(re.fullmatch(pattern, identifier))


def is_valid_positive_integer(value: Any) -> bool:
    """
    Validate a positive integer.

    Args:
        value: Value to validate.

    Returns:
        True if value is a positive integer.
    """
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def is_valid_non_negative_integer(value: Any) -> bool:
    """
    Validate a non-negative integer.

    Args:
        value: Value to validate.

    Returns:
        True if value is a non-negative integer.
    """
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def is_valid_number(
    value: Any,
    minimum: Optional[float] = None,
    maximum: Optional[float] = None,
) -> bool:
    """
    Validate a numeric value within optional bounds.

    Args:
        value: Value to validate.
        minimum: Optional minimum value.
        maximum: Optional maximum value.

    Returns:
        True if valid, otherwise False.
    """
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False

    if minimum is not None and value < minimum:
        return False

    if maximum is not None and value > maximum:
        return False

    return True


def is_valid_choice(
    value: Any,
    choices: Iterable[Any],
) -> bool:
    """
    Check whether a value belongs to an allowed set of choices.

    Args:
        value: Value to validate.
        choices: Allowed values.

    Returns:
        True if value is allowed, otherwise False.
    """
    return value in choices


def validate_required_fields(
    data: Any,
    required_fields: Iterable[str],
) -> tuple[bool, list[str]]:
    """
    Validate that required fields are present in a dictionary.

    Args:
        data: Dictionary to validate.
        required_fields: Required field names.

    Returns:
        Tuple containing validation status and missing fields.
    """
    if not isinstance(data, dict):
        return False, list(required_fields)

    missing_fields = [
        field
        for field in required_fields
        if field not in data or data[field] is None
    ]

    return len(missing_fields) == 0, missing_fields


def validate_top_k(top_k: Any) -> bool:
    """
    Validate a retrieval Top-K value.

    Args:
        top_k: Number of documents to retrieve.

    Returns:
        True if valid, otherwise False.
    """
    return is_valid_positive_integer(top_k) and top_k <= 100


def validate_similarity_score(score: Any) -> bool:
    """
    Validate a similarity score expected to be between 0 and 1.

    Args:
        score: Similarity score.

    Returns:
        True if valid, otherwise False.
    """
    return is_valid_number(score, minimum=0.0, maximum=1.0)


def validate_probability(probability: Any) -> bool:
    """
    Validate a probability value between 0 and 1.

    Args:
        probability: Probability value.

    Returns:
        True if valid, otherwise False.
    """
    return is_valid_number(probability, minimum=0.0, maximum=1.0)