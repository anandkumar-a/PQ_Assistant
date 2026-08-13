"""
Retrieval Module
----------------
Provides document retrieval capabilities for the PQ Assistant.

The retrieval layer includes:
- Dense retrieval using vector similarity search
- Sparse retrieval using BM25
- Hybrid retrieval using Reciprocal Rank Fusion (RRF)
- Cross-encoder based document reranking
"""

from .dense import VectorRetriever
from .sparse import BM25Retriever
from .hybrid import HybridRetriever
from .reranker import Reranker


__all__ = [
    "VectorRetriever",
    "BM25Retriever",
    "HybridRetriever",
    "Reranker",
]