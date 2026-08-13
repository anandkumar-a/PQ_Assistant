"""
Embedding Generator

Generates vector embeddings using Sentence Transformers.
"""

from typing import List

from sentence_transformers import SentenceTransformer


class EmbeddingGenerator:
    """
    Generates embeddings for text using a SentenceTransformer model.
    """

    DEFAULT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

    def __init__(self, model_name: str = DEFAULT_MODEL):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        """
        return self.model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True,
        ).tolist()

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.
        """
        return self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
        ).tolist()

    @property
    def embedding_dimension(self) -> int:
        """
        Returns embedding vector dimension.
        """
        return self.model.get_sentence_embedding_dimension()