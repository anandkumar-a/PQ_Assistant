"""
ChromaDB client management for the PQ Assistant application.

This module is responsible for creating and managing a persistent
ChromaDB client used to store and retrieve vector embeddings.

The client is implemented as a singleton so that the application
reuses a single ChromaDB client instance.
"""

from pathlib import Path
from typing import Optional

import chromadb

from config.logging_config import get_logger


logger = get_logger(__name__)


class ChromaDBClient:
    """
    Manages the persistent ChromaDB client.

    This class creates and provides access to a single persistent
    ChromaDB client instance for the application.
    """

    _instance: Optional["ChromaDBClient"] = None

    def __new__(cls, *args, **kwargs):
        """
        Create or return the existing ChromaDBClient instance.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self, persist_directory: Optional[str] = None):
        """
        Initialize the ChromaDB client.

        Args:
            persist_directory: Directory where ChromaDB data
                will be stored persistently.
        """

        if hasattr(self, "_initialized") and self._initialized:
            return

        if persist_directory is None:
            project_root = Path(__file__).resolve().parents[2]

            persist_directory = (
                project_root / "data" / "chromadb"
            )

        self.persist_directory = Path(persist_directory)

        self.persist_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        try:
            self.client = chromadb.PersistentClient(
                path=str(self.persist_directory)
            )

            logger.info(
                "ChromaDB client initialized successfully at: %s",
                self.persist_directory
            )

            self._initialized = True

        except Exception as error:
            logger.exception(
                "Failed to initialize ChromaDB client: %s",
                error
            )
            raise

    def get_client(self):
        """
        Return the active ChromaDB client.

        Returns:
            chromadb.PersistentClient:
                The initialized ChromaDB client.
        """

        return self.client

    def heartbeat(self) -> bool:
        """
        Check whether the ChromaDB client is active.

        Returns:
            bool: True if the client is active, otherwise False.
        """

        try:
            self.client.heartbeat()

            logger.debug(
                "ChromaDB heartbeat successful."
            )

            return True

        except Exception as error:
            logger.warning(
                "ChromaDB heartbeat failed: %s",
                error
            )

            return False


def get_chroma_client(
    persist_directory: Optional[str] = None
):
    """
    Get the shared ChromaDB client instance.

    Args:
        persist_directory: Optional custom persistence directory.

    Returns:
        chromadb.PersistentClient:
            The active ChromaDB client.
    """

    chroma_client = ChromaDBClient(
        persist_directory=persist_directory
    )

    return chroma_client.get_client()