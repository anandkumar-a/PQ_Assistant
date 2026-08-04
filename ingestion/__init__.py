"""
Ingestion Package

This package is responsible for converting raw documents into
structured, cleaned, and chunked text suitable for embedding
generation and retrieval.

Modules
-------
extractors : Document extraction utilities
cleaners   : Text preprocessing and cleaning
chunkers   : Text chunking strategies
metadata   : Metadata extraction utilities
pipeline   : End-to-end ingestion workflow
"""

__version__ = "1.0.0"

__all__ = [
    "extractors",
    "cleaners",
    "chunkers",
    "metadata",
    "pipeline",
]