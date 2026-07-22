"""
Database package for the PQ Assistant application.

This package provides all database-related functionality used by the
application.

Package Structure
-----------------
chromadb/
    Components for vector database operations such as storing and
    retrieving embeddings for Retrieval-Augmented Generation (RAG).

sqlite/
    SQLite database configuration, connection management, and ORM models.

repositories/
    Repository classes that abstract database operations from the
    business logic layer.

The package follows a modular architecture, allowing each database
technology to evolve independently while exposing a unified interface
to the rest of the application.
"""

__version__ = "1.0.0"

__all__ = []