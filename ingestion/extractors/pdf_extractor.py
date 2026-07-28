"""
PDF Extractor Module

This module provides functionality to extract text content from PDF
documents using the PyPDF library.
"""

from pathlib import Path
from typing import List

from pypdf import PdfReader


class PDFExtractor:
    """
    Extracts text from PDF documents.
    """

    def __init__(self) -> None:
        """Initialize the PDF extractor."""
        pass

    def extract(self, file_path: str | Path) -> str:
        """
        Extract text from a PDF document.

        Args:
            file_path (str | Path):
                Path to the PDF file.

        Returns:
            str:
                Extracted text from all pages.

        Raises:
            FileNotFoundError:
                If the PDF file does not exist.

            ValueError:
                If the file is not a PDF.

            RuntimeError:
                If text extraction fails.
        """

        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if file_path.suffix.lower() != ".pdf":
            raise ValueError(f"Expected a PDF file, got: {file_path.suffix}")

        try:
            reader = PdfReader(file_path)

            pages: List[str] = []

            for page in reader.pages:
                text = page.extract_text()

                if text:
                    pages.append(text)

            return "\n".join(pages)

        except Exception as exc:
            raise RuntimeError(
                f"Failed to extract text from PDF: {file_path}"
            ) from exc