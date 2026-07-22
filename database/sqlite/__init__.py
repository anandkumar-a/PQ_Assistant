"""
SQLite database package.

This package contains all SQLite-specific components such as
database connection management, initialization, repositories,
and helper utilities.
"""

from .connection import SQLiteConnection

__all__ = ["SQLiteConnection"]