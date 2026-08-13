"""
Embeddings Module

This package provides utilities for generating vector embeddings,
managing embedding workflows, and storing embeddings in ChromaDB.

Modules
-------
embedding_generator : Generates embeddings using Sentence Transformers
embedding_manager   : Coordinates embedding generation and storage
chroma_store        : ChromaDB vector database interface
"""

from .embedding_generator import EmbeddingGenerator
from .embedding_manager import EmbeddingManager
from .chroma_store import ChromaStore

__version__ = "1.0.0"

__all__ = [
    "EmbeddingGenerator",
    "EmbeddingManager",
    "ChromaStore",
]