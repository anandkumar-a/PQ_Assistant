"""
Base class for all chunking strategies.
"""

from abc import ABC, abstractmethod
from typing import List

from config import constants


class BaseChunker(ABC):
    """
    Abstract base class for document chunkers.
    """

    def __init__(
        self,
        chunk_size: int = constants.CHUNK_SIZE,
        chunk_overlap: int = constants.CHUNK_OVERLAP,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    @abstractmethod
    def chunk(self, text: str) -> List[str]:
        """
        Split text into chunks.

        Args:
            text: Input document text.

        Returns:
            List of text chunks.
        """
        pass