"""
Common utilities for the PQ Assistant.

Contains small, reusable helper functions that do not belong
to a specific utility category.
"""

import hashlib
import uuid
from typing import Any, Iterable, Optional


def generate_uuid() -> str:
    """
    Generate a unique UUID string.

    Returns:
        UUID string.
    """
    return str(uuid.uuid4())


def generate_hash(
    value: Any,
    algorithm: str = "sha256",
) -> str:
    """
    Generate a deterministic hash for a value.

    Args:
        value: Value to hash.
        algorithm: Hash algorithm supported by hashlib.

    Returns:
        Hexadecimal hash string.

    Raises:
        ValueError: If the requested algorithm is unavailable.
    """
    try:
        hash_function = hashlib.new(algorithm)
    except ValueError as exc:
        raise ValueError(
            f"Unsupported hash algorithm: {algorithm}"
        ) from exc

    hash_function.update(str(value).encode("utf-8"))

    return hash_function.hexdigest()


def safe_int(
    value: Any,
    default: int = 0,
) -> int:
    """
    Safely convert a value to an integer.

    Args:
        value: Value to convert.
        default: Value returned if conversion fails.

    Returns:
        Integer value or default.
    """
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def safe_float(
    value: Any,
    default: float = 0.0,
) -> float:
    """
    Safely convert a value to a float.

    Args:
        value: Value to convert.
        default: Value returned if conversion fails.

    Returns:
        Float value or default.
    """
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def safe_string(
    value: Any,
    default: str = "",
) -> str:
    """
    Safely convert a value to a string.

    Args:
        value: Value to convert.
        default: Value returned for None.

    Returns:
        String representation of the value.
    """
    if value is None:
        return default

    return str(value)


def first_or_default(
    values: Optional[Iterable[Any]],
    default: Any = None,
) -> Any:
    """
    Return the first item from an iterable.

    Args:
        values: Iterable of values.
        default: Value returned when the iterable is empty.

    Returns:
        First item or default.
    """
    if values is None:
        return default

    return next(iter(values), default)


def chunk_list(
    items: list[Any],
    chunk_size: int,
) -> list[list[Any]]:
    """
    Split a list into smaller chunks.

    Useful for batch processing documents or embeddings.

    Args:
        items: List to split.
        chunk_size: Maximum number of items per chunk.

    Returns:
        List of chunks.

    Raises:
        ValueError: If chunk_size is not positive.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")

    return [
        items[index:index + chunk_size]
        for index in range(0, len(items), chunk_size)
    ]


def flatten_list(
    nested_list: Iterable[Iterable[Any]],
) -> list[Any]:
    """
    Flatten a nested iterable by one level.

    Args:
        nested_list: Nested iterable.

    Returns:
        Flattened list.
    """
    return [
        item
        for group in nested_list
        for item in group
    ]


def remove_none_values(
    data: dict[str, Any],
) -> dict[str, Any]:
    """
    Remove dictionary entries whose values are None.

    Args:
        data: Dictionary to process.

    Returns:
        Dictionary without None values.
    """
    return {
        key: value
        for key, value in data.items()
        if value is not None
    }


def merge_dicts(
    first: dict[str, Any],
    second: dict[str, Any],
) -> dict[str, Any]:
    """
    Merge two dictionaries.

    Values from the second dictionary override matching
    keys from the first dictionary.

    Args:
        first: First dictionary.
        second: Second dictionary.

    Returns:
        Merged dictionary.
    """
    merged = first.copy()
    merged.update(second)

    return merged


def clamp(
    value: float,
    minimum: float,
    maximum: float,
) -> float:
    """
    Restrict a numeric value to a specified range.

    Args:
        value: Input value.
        minimum: Minimum allowed value.
        maximum: Maximum allowed value.

    Returns:
        Clamped value.

    Raises:
        ValueError: If minimum is greater than maximum.
    """
    if minimum > maximum:
        raise ValueError(
            "minimum cannot be greater than maximum"
        )

    return max(minimum, min(value, maximum))