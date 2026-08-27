"""
Retrieval analytics for the PQ Assistant.

Tracks and summarizes retrieval performance across:
- Dense/vector retrieval
- Sparse/BM25 retrieval
- Hybrid/RRF retrieval
- Reranking
- Top-K document retrieval
- Retrieval latency and scores
"""

from collections import Counter
from datetime import datetime
from typing import Any, Dict, List, Optional


class RetrievalAnalytics:
    """Collects and analyzes document retrieval metrics."""

    def __init__(self) -> None:
        """Initialize the retrieval analytics tracker."""
        self._retrievals: List[Dict[str, Any]] = []

    def record_retrieval(
        self,
        query: str,
        retriever_type: str,
        retrieved_documents: Optional[List[Dict[str, Any]]] = None,
        top_k: Optional[int] = None,
        retrieval_time: Optional[float] = None,
        reranked: bool = False,
    ) -> Dict[str, Any]:
        """
        Record analytics for a retrieval operation.

        Args:
            query: User query used for retrieval.
            retriever_type: Retrieval method, e.g. vector, bm25, hybrid, or rrf.
            retrieved_documents: Documents returned by the retriever.
            top_k: Number of requested documents.
            retrieval_time: Retrieval latency in seconds.
            reranked: Whether the retrieved documents were reranked.

        Returns:
            Dictionary containing the retrieval analytics record.
        """
        documents = retrieved_documents or []

        record = {
            "query": query,
            "retriever_type": retriever_type,
            "retrieved_documents": documents,
            "retrieved_count": len(documents),
            "top_k": top_k,
            "retrieval_time": retrieval_time,
            "reranked": reranked,
            "timestamp": datetime.utcnow().isoformat(),
        }

        self._retrievals.append(record)
        return record

    def total_retrievals(self) -> int:
        """Return the total number of retrieval operations."""
        return len(self._retrievals)

    def retriever_distribution(self) -> Dict[str, int]:
        """Return the number of retrievals by retriever type."""
        retrievers = [
            record["retriever_type"]
            for record in self._retrievals
            if record.get("retriever_type")
        ]

        return dict(Counter(retrievers))

    def average_retrieval_time(self) -> float:
        """Return average retrieval latency in seconds."""
        times = [
            record["retrieval_time"]
            for record in self._retrievals
            if record.get("retrieval_time") is not None
        ]

        if not times:
            return 0.0

        return sum(times) / len(times)

    def average_documents_retrieved(self) -> float:
        """Return the average number of documents retrieved."""
        counts = [
            record["retrieved_count"]
            for record in self._retrievals
        ]

        if not counts:
            return 0.0

        return sum(counts) / len(counts)

    def reranking_rate(self) -> float:
        """Return the percentage of retrievals that used reranking."""
        total = self.total_retrievals()

        if total == 0:
            return 0.0

        reranked_count = sum(
            record["reranked"]
            for record in self._retrievals
        )

        return (reranked_count / total) * 100

    def top_k_distribution(self) -> Dict[str, int]:
        """Return the distribution of requested top-K values."""
        top_k_values = [
            record["top_k"]
            for record in self._retrievals
            if record.get("top_k") is not None
        ]

        return dict(Counter(map(str, top_k_values)))

    def get_recent_retrievals(
        self,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Return the most recent retrieval records.

        Args:
            limit: Maximum number of records to return.

        Returns:
            List of recent retrieval records.
        """
        if limit <= 0:
            return []

        return self._retrievals[-limit:]

    def summary(self) -> Dict[str, Any]:
        """
        Generate an aggregate retrieval analytics summary.

        Returns:
            Dictionary containing retrieval metrics.
        """
        return {
            "total_retrievals": self.total_retrievals(),
            "retriever_distribution": self.retriever_distribution(),
            "average_retrieval_time": self.average_retrieval_time(),
            "average_documents_retrieved": (
                self.average_documents_retrieved()
            ),
            "reranking_rate": self.reranking_rate(),
            "top_k_distribution": self.top_k_distribution(),
        }

    def clear(self) -> None:
        """Clear all recorded retrieval analytics."""
        self._retrievals.clear()