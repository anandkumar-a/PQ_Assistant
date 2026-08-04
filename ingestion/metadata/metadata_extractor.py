"""
Metadata Extractor Module

This module extracts metadata from documents during the ingestion
pipeline. The extracted metadata is used for indexing, retrieval,
and document management.
"""

from __future__ import annotations

import mimetypes
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from pypdf import PdfReader


class MetadataExtractor:
    """
    Extract metadata from supported document types.
    """

    def __init__(self) -> None:
        """Initialize the metadata extractor."""
        pass

    def extract(self, file_path: str | Path) -> dict[str, Any]:
        """
        Extract metadata from a document.

        Args:
            file_path:
                Path to the document.

        Returns:
            Dictionary containing document metadata.

        Raises:
            FileNotFoundError:
                If the file does not exist.
        """

        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        stat = file_path.stat()

        metadata = {
            "document_id": str(uuid.uuid4()),
            "file_name": file_path.name,
            "file_path": str(file_path.resolve()),
            "file_extension": file_path.suffix.lower(),
            "mime_type": mimetypes.guess_type(file_path)[0],
            "file_size_bytes": stat.st_size,
            "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "page_count": self._get_page_count(file_path),
        }

        return metadata

    def _get_page_count(self, file_path: Path) -> int | None:
        """
        Get page count for supported document types.

        Args:
            file_path:
                Path to the document.

        Returns:
            Number of pages for PDFs, otherwise None.
        """

        if file_path.suffix.lower() != ".pdf":
            return None

        try:
            reader = PdfReader(file_path)
            return len(reader.pages)
        except Exception:
            return None