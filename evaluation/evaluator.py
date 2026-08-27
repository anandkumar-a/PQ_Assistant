"""
Main evaluator for PQ Assistant.

Provides a unified interface for evaluating retrieval
performance and RAG pipeline responses.
"""

from typing import Any, Dict, List

from .metrics import (
    hit_at_k,
    mean_reciprocal_rank,
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
)


class Evaluator:
    """
    Main evaluation class for PQ Assistant.

    Evaluates retrieval quality using Precision@K, Recall@K,
    Reciprocal Rank, MRR, and Hit@K.
    """

    def __init__(self, top_k: int = 5) -> None:
        """
        Initialize the evaluator.

        Args:
            top_k: Number of top retrieved documents to evaluate.
        """

        if top_k <= 0:
            raise ValueError("top_k must be greater than 0.")

        self.top_k = top_k

    def evaluate_retrieval(
        self,
        retrieved_documents: List[str],
        relevant_documents: List[str],
    ) -> Dict[str, float]:
        """
        Evaluate retrieval performance for a single query.

        Args:
            retrieved_documents:
                Documents returned by the retrieval system.

            relevant_documents:
                Ground-truth relevant documents.

        Returns:
            Dictionary containing retrieval metrics.
        """

        return {
            "precision_at_k": precision_at_k(
                retrieved_documents,
                relevant_documents,
                self.top_k,
            ),
            "recall_at_k": recall_at_k(
                retrieved_documents,
                relevant_documents,
                self.top_k,
            ),
            "reciprocal_rank": reciprocal_rank(
                retrieved_documents,
                relevant_documents,
            ),
            "hit_at_k": hit_at_k(
                retrieved_documents,
                relevant_documents,
                self.top_k,
            ),
        }

    def evaluate_batch_retrieval(
        self,
        retrieval_results: List[List[str]],
        relevant_documents: List[List[str]],
    ) -> Dict[str, float]:
        """
        Evaluate retrieval performance across multiple queries.

        Args:
            retrieval_results:
                Retrieved documents for each query.

            relevant_documents:
                Ground-truth relevant documents for each query.

        Returns:
            Aggregated retrieval metrics.
        """

        if len(retrieval_results) != len(relevant_documents):
            raise ValueError(
                "retrieval_results and relevant_documents "
                "must contain the same number of queries."
            )

        if not retrieval_results:
            return {
                "mean_precision_at_k": 0.0,
                "mean_recall_at_k": 0.0,
                "mrr": 0.0,
                "mean_hit_at_k": 0.0,
            }

        query_metrics = [
            self.evaluate_retrieval(
                retrieved,
                relevant,
            )
            for retrieved, relevant in zip(
                retrieval_results,
                relevant_documents,
            )
        ]

        return {
            "mean_precision_at_k": sum(
                metric["precision_at_k"]
                for metric in query_metrics
            ) / len(query_metrics),

            "mean_recall_at_k": sum(
                metric["recall_at_k"]
                for metric in query_metrics
            ) / len(query_metrics),

            "mrr": mean_reciprocal_rank(
                retrieval_results,
                relevant_documents,
            ),

            "mean_hit_at_k": sum(
                metric["hit_at_k"]
                for metric in query_metrics
            ) / len(query_metrics),
        }

    def evaluate_response(
        self,
        query: str,
        answer: str,
        retrieved_documents: List[str],
    ) -> Dict[str, Any]:
        """
        Prepare response information for RAG evaluation.

        RAG-specific metrics such as faithfulness and answer
        relevancy are handled by the RAGAS evaluator.

        Args:
            query:
                User's original query.

            answer:
                Generated answer from the PQ Assistant.

            retrieved_documents:
                Context documents used to generate the answer.

        Returns:
            Dictionary containing response evaluation data.
        """

        return {
            "query": query,
            "answer": answer,
            "retrieved_documents": retrieved_documents,
            "retrieved_document_count": len(retrieved_documents),
        }

    def evaluate(
        self,
        query: str,
        retrieved_documents: List[str],
        relevant_documents: List[str],
        answer: str,
    ) -> Dict[str, Any]:
        """
        Perform complete evaluation for a single query.

        Args:
            query:
                User's original query.

            retrieved_documents:
                Documents returned by the retriever.

            relevant_documents:
                Ground-truth relevant documents.

            answer:
                Final generated answer.

        Returns:
            Complete evaluation result.
        """

        retrieval_metrics = self.evaluate_retrieval(
            retrieved_documents,
            relevant_documents,
        )

        response_data = self.evaluate_response(
            query,
            answer,
            retrieved_documents,
        )

        return {
            "query": query,
            "answer": answer,
            "retrieval_metrics": retrieval_metrics,
            "response": response_data,
        }