"""
Embedding Manager

Coordinates embedding generation and storage.
"""

import uuid
from typing import Dict, List

from .embedding_generator import EmbeddingGenerator
from .chroma_store import ChromaStore


class EmbeddingManager:
    """
    High-level embedding workflow manager.
    """

    def __init__(
        self,
        embedding_generator: EmbeddingGenerator = None,
        chroma_store: ChromaStore = None,
    ):
        self.generator = embedding_generator or EmbeddingGenerator()
        self.store = chroma_store or ChromaStore()

    def process_chunks(
        self,
        chunks: List[str],
        metadata: List[Dict],
    ):
        """
        Generate embeddings and save them.
        """

        embeddings = self.generator.generate_embeddings(chunks)

        ids = [str(uuid.uuid4()) for _ in chunks]

        self.store.add_documents(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadata,
        )

        return ids

    def embed_query(self, query: str):
        """
        Generate query embedding.
        """

        return self.generator.generate_embedding(query)

    def similarity_search(
        self,
        query: str,
        top_k: int = 5,
    ):
        """
        Search similar chunks.
        """

        embedding = self.embed_query(query)

        return self.store.query(
            embedding=embedding,
            top_k=top_k,
        )

    def delete_document(self, ids: List[str]):
        """
        Remove embeddings.
        """

        self.store.delete_documents(ids)

    def total_vectors(self):
        """
        Returns total stored vectors.
        """

        return self.store.count()