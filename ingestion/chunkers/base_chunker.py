"""
Base class for all chunking strategies.
"""

from abc import ABC, abstractmethod
from typing import List


class BaseChunker(ABC):
    """
    Abstract base class for document chunkers.
    """

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 100,
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