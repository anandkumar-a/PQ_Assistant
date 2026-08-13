"""
ChromaDB Storage

Handles all interactions with ChromaDB.
"""

from typing import List, Dict, Optional

import chromadb
from chromadb.config import Settings


class ChromaStore:
    """
    Wrapper around ChromaDB.
    """

    def __init__(
        self,
        persist_directory: str = "./storage/chroma",
        collection_name: str = "pq_documents",
    ):
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False),
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def add_documents(
        self,
        ids: List[str],
        documents: List[str],
        embeddings: List[List[float]],
        metadatas: Optional[List[Dict]] = None,
    ):
        """
        Store documents and embeddings.
        """

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def delete_documents(self, ids: List[str]):
        """
        Delete documents from collection.
        """

        self.collection.delete(ids=ids)

    def query(
        self,
        embedding: List[float],
        top_k: int = 5,
    ):
        """
        Perform similarity search.
        """

        return self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
        )

    def count(self) -> int:
        """
        Number of stored vectors.
        """

        return self.collection.count()

    def reset_collection(self):
        """
        Deletes and recreates collection.
        """

        name = self.collection.name

        self.client.delete_collection(name)

        self.collection = self.client.get_or_create_collection(name=name)