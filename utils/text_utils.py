"""
Text processing utilities for the PQ Assistant.

Provides reusable helpers for cleaning, normalizing, truncating,
and preparing text for retrieval and response generation.
"""

import re
import unicodedata
from typing import Optional


def clean_text(text: str) -> str:
    """
    Clean text by removing excessive whitespace and normalizing Unicode.

    Args:
        text: Input text.

    Returns:
        Cleaned text.
    """
    if not isinstance(text, str):
        return ""

    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def normalize_text(text: str) -> str:
    """
    Normalize text for search and comparison.

    Args:
        text: Input text.

    Returns:
        Lowercase normalized text.
    """
    text = clean_text(text)
    return text.lower()


def remove_special_characters(
    text: str,
    keep_chars: Optional[str] = None,
) -> str:
    """
    Remove special characters while optionally preserving selected characters.

    Args:
        text: Input text.
        keep_chars: Characters that should be preserved.

    Returns:
        Text with unwanted special characters removed.
    """
    if not isinstance(text, str):
        return ""

    allowed = keep_chars or ""
    pattern = rf"[^a-zA-Z0-9\s{re.escape(allowed)}]"
    text = re.sub(pattern, "", text)

    return re.sub(r"\s+", " ", text).strip()


def truncate_text(
    text: str,
    max_length: int,
    suffix: str = "...",
) -> str:
    """
    Truncate text to a maximum character length.

    Args:
        text: Input text.
        max_length: Maximum allowed length.
        suffix: Text appended when truncation occurs.

    Returns:
        Truncated text.
    """
    if not isinstance(text, str):
        return ""

    if max_length <= 0:
        return ""

    if len(text) <= max_length:
        return text

    if len(suffix) >= max_length:
        return suffix[:max_length]

    return text[: max_length - len(suffix)].rstrip() + suffix


def normalize_whitespace(text: str) -> str:
    """
    Replace multiple spaces, tabs, and newlines with a single space.

    Args:
        text: Input text.

    Returns:
        Text with normalized whitespace.
    """
    if not isinstance(text, str):
        return ""

    return re.sub(r"\s+", " ", text).strip()


def extract_numbers(text: str) -> list[str]:
    """
    Extract numeric values from text.

    Useful for identifying product numbers, fault codes,
    quantities, and other numeric identifiers.

    Args:
        text: Input text.

    Returns:
        List of numeric strings.
    """
    if not isinstance(text, str):
        return []

    return re.findall(r"\d+(?:\.\d+)?", text)


def extract_alphanumeric_tokens(text: str) -> list[str]:
    """
    Extract alphanumeric tokens from text.

    Useful for product IDs, part numbers, fault codes,
    and other enterprise identifiers.

    Args:
        text: Input text.

    Returns:
        List of alphanumeric tokens.
    """
    if not isinstance(text, str):
        return []

    return re.findall(r"\b[a-zA-Z0-9_-]+\b", text)


def word_count(text: str) -> int:
    """
    Count the number of words in a text.

    Args:
        text: Input text.

    Returns:
        Number of words.
    """
    if not isinstance(text, str):
        return 0

    return len(re.findall(r"\b\w+\b", text))


def is_empty_text(text: Optional[str]) -> bool:
    """
    Check whether text is empty or contains only whitespace.

    Args:
        text: Input text.

    Returns:
        True if text is empty, otherwise False.
    """
    return not isinstance(text, str) or not text.strip()


def prepare_query(text: str) -> str:
    """
    Prepare a user query for retrieval.

    Applies Unicode normalization, whitespace normalization,
    and lowercase conversion.

    Args:
        text: User query.

    Returns:
        Retrieval-ready query.
    """
    return normalize_text(text)