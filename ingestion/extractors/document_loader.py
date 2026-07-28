"""
Document Loader Module

This module acts as a unified interface for loading documents
of different file types. It automatically selects the appropriate
extractor based on the file extension.
"""

from pathlib import Path

from ingestion.extractors.pdf_extractor import PDFExtractor
from ingestion.extractors.text_extractor import TextExtractor


class DocumentLoader:
    """
    Loads documents using the appropriate extractor.
    """

    SUPPORTED_EXTENSIONS = {
        ".pdf": PDFExtractor,
        ".txt": TextExtractor,
    }

    def __init__(self) -> None:
        """
        Initialize the document loader.
        """
        self._extractors = {
            extension: extractor_class()
            for extension, extractor_class in self.SUPPORTED_EXTENSIONS.items()
        }

    def load(self, file_path: str | Path) -> str:
        """
        Load and extract text from a document.

        Args:
            file_path (str | Path):
                Path to the document.

        Returns:
            str:
                Extracted document text.

        Raises:
            FileNotFoundError:
                If the file does not exist.

            ValueError:
                If the file type is unsupported.
        """

        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        extension = file_path.suffix.lower()

        extractor = self._extractors.get(extension)

        if extractor is None:
            supported = ", ".join(self.SUPPORTED_EXTENSIONS.keys())
            raise ValueError(
                f"Unsupported file type '{extension}'. "
                f"Supported types: {supported}"
            )

        return extractor.extract(file_path)

    @classmethod
    def supported_extensions(cls) -> list[str]:
        """
        Return the list of supported file extensions.
        """

        return list(cls.SUPPORTED_EXTENSIONS.keys())