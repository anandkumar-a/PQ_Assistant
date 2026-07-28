"""
Text Extractor Module

This module provides functionality to extract text content
from plain text (.txt) documents.
"""

from pathlib import Path


class TextExtractor:
    """
    Extracts text from plain text (.txt) documents.
    """

    def __init__(self) -> None:
        """Initialize the text extractor."""
        pass

    def extract(self, file_path: str | Path) -> str:
        """
        Extract text from a text document.

        Args:
            file_path (str | Path):
                Path to the text file.

        Returns:
            str:
                Extracted text.

        Raises:
            FileNotFoundError:
                If the file does not exist.

            ValueError:
                If the file is not a text file.

            RuntimeError:
                If the file cannot be read.
        """

        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if file_path.suffix.lower() != ".txt":
            raise ValueError(
                f"Expected a text (.txt) file, got: {file_path.suffix}"
            )

        try:
            return file_path.read_text(
                encoding="utf-8",
                errors="ignore"
            )

        except Exception as exc:
            raise RuntimeError(
                f"Failed to extract text from: {file_path}"
            ) from exc