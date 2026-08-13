"""
ChromaDB integration package for the PQ Assistant application.

This package provides database-level functionality for managing
ChromaDB operations used in the Retrieval-Augmented Generation (RAG)
pipeline.

Modules
-------
client
    Creates and manages the ChromaDB client connection.

collections
    Handles creation, retrieval, and management of ChromaDB
    collections.

embedding_store
    Stores document embeddings, chunk data, IDs, and metadata.

vector_search
    Performs similarity search and retrieves relevant documents
    based on query embeddings.

The embedding generation logic is handled separately by the
'embeddings' package. This package focuses specifically on
ChromaDB client, collection, storage, and search operations.
"""

__version__ = "1.0.0"

__all__ = []