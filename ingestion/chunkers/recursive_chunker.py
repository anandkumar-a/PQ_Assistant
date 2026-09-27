"""
Recursive text chunker implementation.
"""

from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import constants

from .base_chunker import BaseChunker


class RecursiveChunker(BaseChunker):
    """
    Recursive chunking using LangChain's RecursiveCharacterTextSplitter,
    counting chunk_size/chunk_overlap in TOKENS (via tiktoken) rather
    than characters, per the project spec ("512-token sliding window
    chunker with 50-token overlap").
    """

    def __init__(
        self,
        chunk_size: int = constants.CHUNK_SIZE,
        chunk_overlap: int = constants.CHUNK_OVERLAP,
        encoding_name: str = constants.CHUNK_ENCODING,
    ):
        super().__init__(chunk_size, chunk_overlap)

        # from_tiktoken_encoder makes the splitter count chunk_size
        # and chunk_overlap in tokens (per the given encoding)
        # instead of raw characters -- this is the actual token-vs-
        # character fix, not just a renamed variable. The encoding
        # doesn't need to exactly match Gemini's tokenizer; it only
        # needs to be consistent, so "512 tokens" means the same
        # thing every time a document is (re-)ingested.
        self.splitter = (
            RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                encoding_name=encoding_name,
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