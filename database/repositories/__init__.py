"""
Repository package.

This package provides the data access layer for the application.
Each repository encapsulates database operations for a specific model,
following the Repository Pattern to separate persistence logic from
business logic.
"""

from .base_repository import BaseRepository
from .document_repository import DocumentRepository
from .query_repository import QueryRepository

__all__ = [
    "BaseRepository",
    "DocumentRepository",
    "QueryRepository",
]