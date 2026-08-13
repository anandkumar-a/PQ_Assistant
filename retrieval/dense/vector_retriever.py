"""
Vector Retriever Module
-----------------------
Provides dense/semantic document retrieval using embeddings
and ChromaDB.

The retriever converts a user query into an embedding vector
and searches the vector database for the most semantically
similar documents.
"""

from typing import Any, Dict, List, Optional

import chromadb

from config.logging_config import get_logger


logger = get_logger(__name__)


class VectorRetriever:
    """
    Dense vector retriever for semantic document search.

    This class connects to a ChromaDB collection and retrieves
    documents based on semantic similarity between the user query
    and stored document embeddings.
    """

    def __init__(
        self,
        collection_name: str,
        persist_directory: str,
    ) -> None:
        """
        Initialize the VectorRetriever.

        Args:
            collection_name: Name of the ChromaDB collection.
            persist_directory: Directory where ChromaDB data is stored.
        """

        self.collection_name = collection_name
        self.persist_directory = persist_directory

        try:
            self.client = chromadb.PersistentClient(
                path=self.persist_directory
            )

            self.collection = self.client.get_or_create_collection(
                name=self.collection_name
            )

            logger.info(
                "VectorRetriever initialized successfully "
                "for collection: %s",
                self.collection_name,
            )

        except Exception as error:
            logger.exception(
                "Failed to initialize VectorRetriever: %s",
                error,
            )
            raise

    def retrieve(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        where: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve the most semantically similar documents.

        Args:
            query_embedding: Embedding vector of the user query.
            top_k: Number of top results to retrieve.
            where: Optional metadata filter.

        Returns:
            A list of retrieved documents containing their
            content, metadata, distance, and ID.
        """

        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where=where,
                include=[
                    "documents",
                    "metadatas",
                    "distances",
                ],
            )

            retrieved_documents = []

            if not results.get("ids"):
                logger.info("No documents found for the query.")
                return retrieved_documents

            for index, document_id in enumerate(results["ids"][0]):

                document = (
                    results["documents"][0][index]
                    if results.get("documents")
                    else None
                )

                metadata = (
                    results["metadatas"][0][index]
                    if results.get("metadatas")
                    else {}
                )

                distance = (
                    results["distances"][0][index]
                    if results.get("distances")
                    else None
                )

                retrieved_documents.append(
                    {
                        "id": document_id,
                        "content": document,
                        "metadata": metadata,
                        "distance": distance,
                    }
                )

            logger.info(
                "Retrieved %s documents from collection: %s",
                len(retrieved_documents),
                self.collection_name,
            )

            return retrieved_documents

        except Exception as error:
            logger.exception(
                "Vector retrieval failed: %s",
                error,
            )
            return []

    def get_collection_count(self) -> int:
        """
        Get the total number of documents in the collection.

        Returns:
            Number of documents stored in the collection.
        """

        try:
            return self.collection.count()

        except Exception as error:
            logger.exception(
                "Failed to get collection count: %s",
                error,
            )
            return 0

    def reset_collection(self) -> None:
        """
        Delete and recreate the current collection.

        Warning:
            This permanently removes all stored documents.
        """

        try:
            self.client.delete_collection(
                name=self.collection_name
            )

            self.collection = self.client.get_or_create_collection(
                name=self.collection_name
            )

            logger.warning(
                "Collection reset successfully: %s",
                self.collection_name,
            )

        except Exception as error:
            logger.exception(
                "Failed to reset collection: %s",
                error,
            )
            raise