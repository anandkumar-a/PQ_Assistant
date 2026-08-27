"""
JSON utilities for the PQ Assistant.

Provides safe and reusable helpers for loading, saving,
parsing, and serializing JSON data.
"""

import json
from pathlib import Path
from typing import Any, Optional


def load_json(
    file_path: str | Path,
    default: Optional[Any] = None,
) -> Any:
    """
    Load JSON data from a file.

    Args:
        file_path: Path to the JSON file.
        default: Value returned if the file cannot be loaded.

    Returns:
        Parsed JSON data or the default value.
    """
    path = Path(file_path)

    if not path.exists():
        return default

    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return default


def save_json(
    data: Any,
    file_path: str | Path,
    indent: int = 4,
) -> bool:
    """
    Save data to a JSON file.

    Args:
        data: Data to serialize.
        file_path: Destination file path.
        indent: JSON indentation level.

    Returns:
        True if saved successfully, otherwise False.
    """
    path = Path(file_path)

    try:
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                indent=indent,
                ensure_ascii=False,
                default=str,
            )

        return True

    except (TypeError, OSError):
        return False


def parse_json(
    json_string: str,
    default: Optional[Any] = None,
) -> Any:
    """
    Parse a JSON string.

    Args:
        json_string: JSON formatted string.
        default: Value returned if parsing fails.

    Returns:
        Parsed JSON data or the default value.
    """
    if not isinstance(json_string, str):
        return default

    try:
        return json.loads(json_string)
    except json.JSONDecodeError:
        return default


def serialize_json(
    data: Any,
    indent: Optional[int] = None,
) -> Optional[str]:
    """
    Serialize Python data into a JSON string.

    Args:
        data: Python object to serialize.
        indent: Optional indentation level.

    Returns:
        JSON string or None if serialization fails.
    """
    try:
        return json.dumps(
            data,
            indent=indent,
            ensure_ascii=False,
            default=str,
        )
    except (TypeError, ValueError):
        return None


def is_valid_json(json_string: str) -> bool:
    """
    Check whether a string contains valid JSON.

    Args:
        json_string: String to validate.

    Returns:
        True if valid JSON, otherwise False.
    """
    if not isinstance(json_string, str):
        return False

    try:
        json.loads(json_string)
        return True
    except json.JSONDecodeError:
        return False


def get_json_value(
    data: dict,
    key: str,
    default: Optional[Any] = None,
) -> Any:
    """
    Safely retrieve a value from a JSON-like dictionary.

    Args:
        data: Dictionary containing the value.
        key: Key to retrieve.
        default: Value returned if the key is unavailable.

    Returns:
        Retrieved value or default.
    """
    if not isinstance(data, dict):
        return default

    return data.get(key, default)