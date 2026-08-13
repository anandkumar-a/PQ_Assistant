"""
BM25 Retriever Module
---------------------
Provides sparse/keyword-based document retrieval using
the BM25 algorithm.

This retriever is particularly useful for exact keyword matching,
such as fault codes, error IDs, part numbers, and technical terms.
"""

import re
from typing import Any, Dict, List

from rank_bm25 import BM25Okapi

from config.logging_config import get_logger


logger = get_logger(__name__)


class BM25Retriever:
    """
    Sparse document retriever using the BM25 algorithm.

    The retriever builds a BM25 index from a collection of documents
    and retrieves the most relevant documents based on keyword
    matching.
    """

    def __init__(
        self,
        documents: List[Dict[str, Any]],
    ) -> None:
        """
        Initialize the BM25 retriever.

        Args:
            documents: List of documents. Each document should contain
                at least a 'content' field.
        """

        self.documents = documents
        self.tokenized_documents: List[List[str]] = []

        try:
            self._build_index()

            logger.info(
                "BM25Retriever initialized with %s documents.",
                len(self.documents),
            )

        except Exception as error:
            logger.exception(
                "Failed to initialize BM25Retriever: %s",
                error,
            )
            raise

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        """
        Convert text into lowercase tokens.

        Args:
            text: Input text to tokenize.

        Returns:
            List of normalized tokens.
        """

        if not text:
            return []

        return re.findall(
            r"\b[\w\-]+\b",
            text.lower(),
        )

    def _build_index(self) -> None:
        """
        Build the BM25 index from the provided documents.
        """

        self.tokenized_documents = [
            self._tokenize(
                document.get("content", "")
            )
            for document in self.documents
        ]

        if not self.tokenized_documents:
            raise ValueError(
                "Cannot build BM25 index with an empty document list."
            )

        self.bm25 = BM25Okapi(
            self.tokenized_documents
        )

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve the most relevant documents using BM25.

        Args:
            query: User search query.
            top_k: Number of top documents to retrieve.

        Returns:
            List of retrieved documents with their BM25 scores.
        """

        if not query:
            logger.warning(
                "Empty query received for BM25 retrieval."
            )
            return []

        try:
            tokenized_query = self._tokenize(query)

            if not tokenized_query:
                return []

            scores = self.bm25.get_scores(
                tokenized_query
            )

            ranked_indices = sorted(
                range(len(scores)),
                key=lambda index: scores[index],
                reverse=True,
            )[:top_k]

            retrieved_documents = []

            for index in ranked_indices:

                document = self.documents[index].copy()

                document["score"] = float(
                    scores[index]
                )

                retrieved_documents.append(
                    document
                )

            logger.info(
                "Retrieved %s documents using BM25.",
                len(retrieved_documents),
            )

            return retrieved_documents

        except Exception as error:
            logger.exception(
                "BM25 retrieval failed: %s",
                error,
            )
            return []

    def get_document_count(self) -> int:
        """
        Get the number of indexed documents.

        Returns:
            Total number of documents.
        """

        return len(self.documents)

    def rebuild_index(
        self,
        documents: List[Dict[str, Any]],
    ) -> None:
        """
        Rebuild the BM25 index with new documents.

        Args:
            documents: Updated list of documents.
        """

        try:
            self.documents = documents

            self._build_index()

            logger.info(
                "BM25 index rebuilt with %s documents.",
                len(self.documents),
            )

        except Exception as error:
            logger.exception(
                "Failed to rebuild BM25 index: %s",
                error,
            )
            raise