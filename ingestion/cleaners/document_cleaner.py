"""
document_cleaner.py

Purpose:
--------
Provides text cleaning utilities for documents extracted from PDFs,
Word files, text files, manuals, service bulletins, and historical
product queries.

The cleaner standardizes the extracted text before metadata extraction,
chunking, and embedding generation.
"""

import re
from typing import Optional


class DocumentCleaner:
    """
    Cleans extracted document text.

    Functions include:
    - Remove excessive whitespace
    - Remove empty lines
    - Normalize Unicode characters
    - Remove unwanted control characters
    - Normalize punctuation spacing
    """

    def __init__(self):
        pass

    @staticmethod
    def remove_extra_whitespace(text: str) -> str:
        """
        Remove multiple spaces and tabs.

        Args:
            text (str): Raw text

        Returns:
            str: Cleaned text
        """
        return re.sub(r"[ \t]+", " ", text)

    @staticmethod
    def remove_blank_lines(text: str) -> str:
        """
        Remove unnecessary blank lines.

        Args:
            text (str)

        Returns:
            str
        """
        return re.sub(r"\n\s*\n+", "\n\n", text)

    @staticmethod
    def normalize_newlines(text: str) -> str:
        """
        Convert Windows/Mac line endings into Unix format.
        """
        return text.replace("\r\n", "\n").replace("\r", "\n")

    @staticmethod
    def remove_control_characters(text: str) -> str:
        """
        Remove non-printable control characters while
        preserving tabs and newlines.
        """
        return re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "", text)

    @staticmethod
    def normalize_unicode(text: str) -> str:
        """
        Normalize common Unicode punctuation.

        Example:
        --------
        “Example” → "Example"
        """
        replacements = {
            "“": '"',
            "”": '"',
            "‘": "'",
            "’": "'",
            "–": "-",
            "—": "-",
            "…": "...",
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        return text

    @staticmethod
    def clean(text: Optional[str]) -> str:
        """
        Complete cleaning pipeline.

        Args:
            text (str)

        Returns:
            str
        """
        if not text:
            return ""

        text = DocumentCleaner.normalize_newlines(text)
        text = DocumentCleaner.normalize_unicode(text)
        text = DocumentCleaner.remove_control_characters(text)
        text = DocumentCleaner.remove_extra_whitespace(text)
        text = DocumentCleaner.remove_blank_lines(text)

        return text.strip()