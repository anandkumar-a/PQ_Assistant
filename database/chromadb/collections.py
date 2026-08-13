"""
ChromaDB collection management for the PQ Assistant application.

This module is responsible for creating, retrieving, listing,
and deleting ChromaDB collections.

Collections are used to organize different types of vector data,
such as documents, historical product queries, and service records.
"""

from typing import List, Optional

from config.logging_config import get_logger
from database.chromadb.client import get_chroma_client


logger = get_logger(__name__)


class CollectionManager:
    """
    Manages ChromaDB collections.

    This class provides methods to create, retrieve, list,
    check, and delete collections.
    """

    def __init__(self, persist_directory: Optional[str] = None):
        """
        Initialize the CollectionManager.

        Args:
            persist_directory: Optional custom directory for
                ChromaDB persistent storage.
        """

        self.client = get_chroma_client(
            persist_directory=persist_directory
        )

        logger.info("CollectionManager initialized successfully.")

    def get_or_create_collection(
        self,
        collection_name: str,
        metadata: Optional[dict] = None
    ):
        """
        Get an existing collection or create a new one.

        Args:
            collection_name: Name of the ChromaDB collection.
            metadata: Optional metadata for the collection.

        Returns:
            chromadb.Collection:
                The existing or newly created collection.
        """

        try:
            collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata=metadata
            )

            logger.info(
                "Collection '%s' is ready.",
                collection_name
            )

            return collection

        except Exception as error:
            logger.exception(
                "Failed to get or create collection '%s': %s",
                collection_name,
                error
            )
            raise

    def get_collection(
        self,
        collection_name: str
    ):
        """
        Retrieve an existing collection.

        Args:
            collection_name: Name of the collection.

        Returns:
            chromadb.Collection:
                The requested collection.

        Raises:
            Exception:
                If the collection does not exist or cannot be retrieved.
        """

        try:
            collection = self.client.get_collection(
                name=collection_name
            )

            logger.info(
                "Retrieved collection '%s'.",
                collection_name
            )

            return collection

        except Exception as error:
            logger.exception(
                "Failed to retrieve collection '%s': %s",
                collection_name,
                error
            )
            raise

    def collection_exists(
        self,
        collection_name: str
    ) -> bool:
        """
        Check whether a collection exists.

        Args:
            collection_name: Name of the collection.

        Returns:
            bool:
                True if the collection exists,
                otherwise False.
        """

        try:
            self.client.get_collection(
                name=collection_name
            )

            return True

        except Exception:
            return False

    def list_collections(self) -> List[str]:
        """
        Get the names of all available ChromaDB collections.

        Returns:
            List[str]:
                List containing collection names.
        """

        try:
            collections = self.client.list_collections()

            collection_names = [
                collection.name
                for collection in collections
            ]

            logger.info(
                "Found %d ChromaDB collections.",
                len(collection_names)
            )

            return collection_names

        except Exception as error:
            logger.exception(
                "Failed to list ChromaDB collections: %s",
                error
            )
            raise

    def delete_collection(
        self,
        collection_name: str
    ) -> bool:
        """
        Delete a ChromaDB collection.

        Args:
            collection_name: Name of the collection to delete.

        Returns:
            bool:
                True if the collection was deleted successfully,
                otherwise False.
        """

        try:
            if not self.collection_exists(collection_name):
                logger.warning(
                    "Collection '%s' does not exist.",
                    collection_name
                )

                return False

            self.client.delete_collection(
                name=collection_name
            )

            logger.info(
                "Collection '%s' deleted successfully.",
                collection_name
            )

            return True

        except Exception as error:
            logger.exception(
                "Failed to delete collection '%s': %s",
                collection_name,
                error
            )

            return False