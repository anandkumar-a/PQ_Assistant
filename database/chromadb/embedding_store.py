"""
Embedding storage operations for the PQ Assistant application.

This module is responsible for storing, updating, retrieving,
and deleting document embeddings and their associated metadata
in ChromaDB.

Embedding generation is handled separately by the embeddings package.
"""

from typing import Any, Dict, List, Optional

from config.logging_config import get_logger
from database.chromadb.collections import CollectionManager


logger = get_logger(__name__)


class EmbeddingStore:
    """
    Manages embedding storage operations in ChromaDB.

    This class handles adding, updating, retrieving, and deleting
    document embeddings along with their documents and metadata.
    """

    def __init__(
        self,
        collection_name: str,
        persist_directory: Optional[str] = None
    ):
        """
        Initialize the EmbeddingStore.

        Args:
            collection_name:
                Name of the ChromaDB collection.

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
            "EmbeddingStore initialized for collection '%s'.",
            collection_name
        )

    def add_embeddings(
        self,
        ids: List[str],
        embeddings: List[List[float]],
        documents: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None
    ) -> None:
        """
        Add embeddings to the ChromaDB collection.

        Args:
            ids:
                Unique IDs for the document chunks.

            embeddings:
                Vector embeddings corresponding to the documents.

            documents:
                Original text chunks associated with the embeddings.

            metadatas:
                Optional metadata for each document chunk.

        Raises:
            ValueError:
                If the input list lengths do not match.
        """

        if not (
            len(ids)
            == len(embeddings)
            == len(documents)
        ):
            raise ValueError(
                "The lengths of ids, embeddings, and documents "
                "must be equal."
            )

        if (
            metadatas is not None
            and len(metadatas) != len(ids)
        ):
            raise ValueError(
                "The length of metadatas must match "
                "the number of ids."
            )

        try:
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas
            )

            logger.info(
                "Successfully stored %d embeddings in collection '%s'.",
                len(ids),
                self.collection_name
            )

        except Exception as error:
            logger.exception(
                "Failed to store embeddings in collection '%s': %s",
                self.collection_name,
                error
            )
            raise

    def upsert_embeddings(
        self,
        ids: List[str],
        embeddings: List[List[float]],
        documents: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None
    ) -> None:
        """
        Add or update embeddings in the ChromaDB collection.

        If an ID already exists, its embedding, document, and metadata
        will be updated. Otherwise, a new record will be created.
        """

        if not (
            len(ids)
            == len(embeddings)
            == len(documents)
        ):
            raise ValueError(
                "The lengths of ids, embeddings, and documents "
                "must be equal."
            )

        if (
            metadatas is not None
            and len(metadatas) != len(ids)
        ):
            raise ValueError(
                "The length of metadatas must match "
                "the number of ids."
            )

        try:
            self.collection.upsert(
                ids=ids,
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas
            )

            logger.info(
                "Successfully upserted %d embeddings in collection '%s'.",
                len(ids),
                self.collection_name
            )

        except Exception as error:
            logger.exception(
                "Failed to upsert embeddings in collection '%s': %s",
                self.collection_name,
                error
            )
            raise

    def get_embeddings(
        self,
        ids: Optional[List[str]] = None,
        where: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Retrieve embeddings and associated data.

        Args:
            ids:
                Optional list of embedding IDs.

            where:
                Optional metadata filter.

        Returns:
            Dictionary containing IDs, embeddings, documents,
            and metadata.
        """

        try:
            result = self.collection.get(
                ids=ids,
                where=where,
                include=[
                    "embeddings",
                    "documents",
                    "metadatas"
                ]
            )

            logger.debug(
                "Retrieved %d records from collection '%s'.",
                len(result.get("ids", [])),
                self.collection_name
            )

            return result

        except Exception as error:
            logger.exception(
                "Failed to retrieve embeddings from collection '%s': %s",
                self.collection_name,
                error
            )
            raise

    def delete_embeddings(
        self,
        ids: Optional[List[str]] = None,
        where: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Delete embeddings from the ChromaDB collection.

        Args:
            ids:
                Optional list of embedding IDs to delete.

            where:
                Optional metadata filter for deletion.

        Raises:
            ValueError:
                If neither ids nor where is provided.
        """

        if ids is None and where is None:
            raise ValueError(
                "Either 'ids' or 'where' must be provided "
                "to delete embeddings."
            )

        try:
            self.collection.delete(
                ids=ids,
                where=where
            )

            logger.info(
                "Embeddings deleted from collection '%s'.",
                self.collection_name
            )

        except Exception as error:
            logger.exception(
                "Failed to delete embeddings from collection '%s': %s",
                self.collection_name,
                error
            )
            raise

    def count(self) -> int:
        """
        Return the total number of embeddings in the collection.
        """

        try:
            total = self.collection.count()

            logger.debug(
                "Collection '%s' contains %d embeddings.",
                self.collection_name,
                total
            )

            return total

        except Exception as error:
            logger.exception(
                "Failed to count embeddings in collection '%s': %s",
                self.collection_name,
                error
            )
            raise