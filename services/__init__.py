"""
Service Layer Package

This package contains all business logic for the application.

Responsibilities:
- Validate business rules
- Coordinate repository operations
- Process application data
- Provide reusable services for higher layers

The service layer acts as an intermediary between
the application's interface (API/UI) and the
repository layer.

Available Services:
- BaseService
- DocumentService
- QueryService
"""

from .base_service import BaseService
from .document_service import DocumentService
from .query_service import QueryService

__all__ = [
    "BaseService",
    "DocumentService",
    "QueryService",
]