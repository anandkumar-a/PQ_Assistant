"""
Time and timestamp utilities for the PQ Assistant.

Provides reusable helpers for timestamps, duration measurement,
date/time formatting, and execution-time tracking.
"""

import time
from datetime import datetime, timezone
from typing import Optional


def get_current_timestamp() -> datetime:
    """
    Get the current UTC timestamp.

    Returns:
        Current timezone-aware UTC datetime.
    """
    return datetime.now(timezone.utc)


def get_current_timestamp_string(
    include_microseconds: bool = False,
) -> str:
    """
    Get the current UTC timestamp as an ISO 8601 string.

    Args:
        include_microseconds: Whether to include microseconds.

    Returns:
        ISO 8601 formatted UTC timestamp.
    """
    timestamp = get_current_timestamp()

    if not include_microseconds:
        timestamp = timestamp.replace(microsecond=0)

    return timestamp.isoformat()


def format_timestamp(
    timestamp: datetime,
    format_string: str = "%Y-%m-%d %H:%M:%S",
) -> str:
    """
    Format a datetime object as a string.

    Args:
        timestamp: Datetime object.
        format_string: Desired datetime format.

    Returns:
        Formatted timestamp.
    """
    return timestamp.strftime(format_string)


def parse_timestamp(
    timestamp_string: str,
) -> Optional[datetime]:
    """
    Parse an ISO 8601 timestamp string.

    Args:
        timestamp_string: ISO formatted timestamp.

    Returns:
        Parsed datetime or None if parsing fails.
    """
    if not isinstance(timestamp_string, str):
        return None

    try:
        return datetime.fromisoformat(timestamp_string)
    except ValueError:
        return None


def get_unix_timestamp() -> float:
    """
    Get the current Unix timestamp.

    Returns:
        Current Unix timestamp in seconds.
    """
    return time.time()


def get_elapsed_time(start_time: float) -> float:
    """
    Calculate elapsed time using a monotonic clock.

    Args:
        start_time: Starting value returned by time.perf_counter().

    Returns:
        Elapsed time in seconds.
    """
    return time.perf_counter() - start_time


def start_timer() -> float:
    """
    Start a high-resolution execution timer.

    Returns:
        Timer start value.
    """
    return time.perf_counter()


def format_duration(seconds: float) -> str:
    """
    Format a duration into a human-readable representation.

    Args:
        seconds: Duration in seconds.

    Returns:
        Formatted duration string.
    """
    if seconds < 0:
        seconds = 0

    if seconds < 1:
        return f"{seconds * 1000:.2f} ms"

    if seconds < 60:
        return f"{seconds:.2f} sec"

    minutes, remaining_seconds = divmod(seconds, 60)

    if minutes < 60:
        return f"{int(minutes)} min {remaining_seconds:.1f} sec"

    hours, remaining_minutes = divmod(minutes, 60)

    return (
        f"{int(hours)} hr "
        f"{int(remaining_minutes)} min "
        f"{remaining_seconds:.1f} sec"
    )


def timestamp_difference(
    start: datetime,
    end: datetime,
) -> float:
    """
    Calculate the difference between two timestamps.

    Args:
        start: Starting datetime.
        end: Ending datetime.

    Returns:
        Difference in seconds.
    """
    return (end - start).total_seconds()


def is_timestamp_valid(timestamp_string: str) -> bool:
    """
    Check whether a string is a valid ISO 8601 timestamp.

    Args:
        timestamp_string: Timestamp string.

    Returns:
        True if valid, otherwise False.
    """
    return parse_timestamp(timestamp_string) is not None