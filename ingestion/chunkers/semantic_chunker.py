"""
Semantic chunker.

Currently acts as a placeholder.

Future versions can use:
- Sentence Transformers
- LangChain SemanticChunker
- LlamaIndex Semantic Splitter
"""

from typing import List

from .base_chunker import BaseChunker


class SemanticChunker(BaseChunker):
    """
    Placeholder semantic chunker.

    Currently falls back to paragraph-based chunking.
    """

    def chunk(self, text: str) -> List[str]:
        """
        Split text semantically (placeholder).

        Args:
            text: Input document.

        Returns:
            List of chunks.
        """
        if not text:
            return []

        paragraphs = [
            p.strip()
            for p in text.split("\n\n")
            if p.strip()
        ]

        return paragraphs