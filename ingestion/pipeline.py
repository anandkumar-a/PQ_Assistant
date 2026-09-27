from pathlib import Path
from typing import Dict, Any, List

from config import constants

from ingestion.extractors.document_loader import DocumentLoader
from ingestion.cleaners.document_cleaner import DocumentCleaner
from ingestion.metadata.metadata_extractor import MetadataExtractor
from ingestion.chunkers.recursive_chunker import RecursiveChunker


class IngestionPipeline:
    """
    End-to-end ingestion pipeline.
    """

    def __init__(
        self,
        chunk_size: int = constants.CHUNK_SIZE,
        chunk_overlap: int = constants.CHUNK_OVERLAP,
    ):
        """
        Initialize the ingestion pipeline.

        Args:
            chunk_size: Maximum tokens per chunk (see
                config/constants.py -- fixed at 512 per spec).
            chunk_overlap: Token overlap between chunks (fixed at
                50 per spec).
        """

        self.loader = DocumentLoader()
        self.cleaner = DocumentCleaner()
        self.metadata_extractor = MetadataExtractor()
        self.chunker = RecursiveChunker(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )