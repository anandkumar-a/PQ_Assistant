"""
Recursive text chunker implementation.
"""

from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter

from .base_chunker import BaseChunker


class RecursiveChunker(BaseChunker):
    """
    Recursive chunking using LangChain's RecursiveCharacterTextSplitter.
    """

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 100,
    ):
        super().__init__(chunk_size, chunk_overlap)

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                "? ",
                "! ",
                ", ",
                " ",
                "",
            ],
        )

    def chunk(self, text: str) -> List[str]:
        """
        Split document recursively.

        Args:
            text: Input document.

        Returns:
            List of chunks.
        """
        if not text:
            return []

        return self.splitter.split_text(text)