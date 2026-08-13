"""
Sparse Retrieval Module
-----------------------
This package contains components for keyword-based
document retrieval using the BM25 algorithm.
"""

from .bm25_retriever import BM25Retriever

__all__ = [
    "BM25Retriever",
]