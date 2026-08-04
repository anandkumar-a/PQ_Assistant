"""
Metadata Package

This package provides utilities for extracting and managing
metadata from documents during the ingestion process.

Responsibilities
----------------
- Extract file metadata
- Extract document-specific metadata
- Standardize metadata structure
- Support downstream indexing and retrieval
"""

from .metadata_extractor import MetadataExtractor

__version__ = "1.0.0"

__all__ = [
    "MetadataExtractor",
]