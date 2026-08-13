"""
Reranker Module
---------------
Provides document reranking functionality to improve the
relevance of retrieved documents.

The reranker receives documents from the retrieval pipeline
and scores each query-document pair using a cross-encoder model.
"""

from typing import Any, Dict, List

from sentence_transformers import CrossEncoder

from config.logging_config import get_logger


logger = get_logger(__name__)


class Reranker:
    """
    Cross-encoder based document reranker.

    This class reranks retrieved documents by evaluating the
    relevance between a user query and each document.
    """

    def __init__(
        self,
        model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
    ) -> None:
        """
        Initialize the reranker.

        Args:
            model_name: Name of the CrossEncoder model used
                for reranking query-document pairs.
        """

        self.model_name = model_name

        try:
            self.model = CrossEncoder(
                self.model_name
            )

            logger.info(
                "Reranker initialized successfully with model: %s",
                self.model_name,
            )

        except Exception as error:
            logger.exception(
                "Failed to initialize Reranker: %s",
                error,
            )
            raise

    def rerank(
        self,
        query: str,
        documents: List[Dict[str, Any]],
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Rerank retrieved documents based on query relevance.

        Args:
            query: User search query.
            documents: Documents returned by the retrieval system.
            top_k: Number of top documents to return.

        Returns:
            Reranked list of documents with relevance scores.
        """

        if not query:
            logger.warning(
                "Empty query received for reranking."
            )
            return []

        if not documents:
            logger.warning(
                "No documents provided for reranking."
            )
            return []

        try:
            # Create query-document pairs
            query_document_pairs = [
                (
                    query,
                    document.get("content", ""),
                )
                for document in documents
            ]

            # Generate relevance scores
            scores = self.model.predict(
                query_document_pairs
            )

            # Attach scores to documents
            reranked_documents = []

            for document, score in zip(
                documents,
                scores,
            ):
                reranked_document = document.copy()

                reranked_document["rerank_score"] = float(
                    score
                )

                reranked_documents.append(
                    reranked_document
                )

            # Sort documents by relevance score
            reranked_documents.sort(
                key=lambda item: item["rerank_score"],
                reverse=True,
            )

            final_results = reranked_documents[:top_k]

            logger.info(
                "Reranking completed. "
                "Input documents: %s | Output documents: %s",
                len(documents),
                len(final_results),
            )

            return final_results

        except Exception as error:
            logger.exception(
                "Document reranking failed: %s",
                error,
            )
            return []

    def get_model_name(self) -> str:
        """
        Get the name of the currently loaded reranking model.

        Returns:
            Name of the CrossEncoder model.
        """

        return self.model_name