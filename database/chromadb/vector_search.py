"""
Vector search operations for the PQ Assistant application.

This module performs similarity search on embeddings stored in
ChromaDB collections.

Embedding generation is handled separately by the embeddings package.
This module receives query embeddings and retrieves the most relevant
documents from ChromaDB.
"""

from typing import Any, Dict, List, Optional

from config.logging_config import get_logger
from database.chromadb.collections import CollectionManager


logger = get_logger(__name__)


class VectorSearch:
    """
    Performs vector similarity search using ChromaDB.

    This class retrieves the most relevant documents based on
    query embeddings stored in a specified ChromaDB collection.
    """

    def __init__(
        self,
        collection_name: str,
        persist_directory: Optional[str] = None
    ):
        """
        Initialize the VectorSearch.

        Args:
            collection_name:
                Name of the ChromaDB collection to search.

            persist_directory:
                Optional directory for ChromaDB persistent storage.
        """

        self.collection_name = collection_name

        self.collection_manager = CollectionManager(
            persist_directory=persist_directory
        )

        self.collection = (
            self.collection_manager.get_or_create_collection(
                collection_name=collection_name
            )
        )

        logger.info(
            "VectorSearch initialized for collection '%s'.",
            collection_name
        )

    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        where: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Perform similarity search using a query embedding.

        Args:
            query_embedding:
                Vector representation of the user's query.

            top_k:
                Number of most relevant results to retrieve.

            where:
                Optional metadata filter.

        Returns:
            Dictionary containing matching IDs, documents,
            metadata, and similarity distances.
        """

        if not query_embedding:
            raise ValueError(
                "query_embedding cannot be empty."
            )

        if top_k <= 0:
            raise ValueError(
                "top_k must be greater than 0."
            )

        try:
            result = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where=where,
                include=[
                    "documents",
                    "metadatas",
                    "distances"
                ]
            )

            logger.info(
                "Vector search completed successfully in "
                "collection '%s'. Retrieved up to %d results.",
                self.collection_name,
                top_k
            )

            return result

        except Exception as error:
            logger.exception(
                "Vector search failed in collection '%s': %s",
                self.collection_name,
                error
            )
            raise

    def search_with_metadata(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        where: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Perform vector search and return results in a structured format.

        Args:
            query_embedding:
                Vector representation of the user's query.

            top_k:
                Number of most relevant results.

            where:
                Optional metadata filter.

        Returns:
            List of dictionaries containing ID, document,
            metadata, and distance for each result.
        """

        result = self.search(
            query_embedding=query_embedding,
            top_k=top_k,
            where=where
        )

        ids = result.get("ids", [[]])[0]
        documents = result.get("documents", [[]])[0]
        metadatas = result.get("metadatas", [[]])[0]
        distances = result.get("distances", [[]])[0]

        search_results = []

        for index, document_id in enumerate(ids):
            search_results.append(
                {
                    "id": document_id,
                    "document": documents[index],
                    "metadata": metadatas[index],
                    "distance": distances[index]
                }
            )

        logger.debug(
            "Formatted %d vector search results.",
            len(search_results)
        )

        return search_results

    def count(self) -> int:
        """
        Return the total number of vectors in the collection.

        Returns:
            int: Number of stored embeddings.
        """

        try:
            return self.collection.count()

        except Exception as error:
            logger.exception(
                "Failed to count vectors in collection '%s': %s",
                self.collection_name,
                error
            )
            raise