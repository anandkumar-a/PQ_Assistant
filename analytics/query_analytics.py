"""
Query analytics for the PQ Assistant.

Tracks and summarizes user-query activity, including:
- Query volume
- Query intent distribution
- Extracted entities
- Query processing time
- Query success and failure
"""

from collections import Counter
from datetime import datetime
from typing import Any, Dict, List, Optional


class QueryAnalytics:
    """Collects and analyzes query-level analytics."""

    def __init__(self) -> None:
        """Initialize the query analytics tracker."""
        self._queries: List[Dict[str, Any]] = []

    def record_query(
        self,
        query: str,
        intent: Optional[str] = None,
        entities: Optional[Dict[str, Any]] = None,
        processing_time: Optional[float] = None,
        success: bool = True,
    ) -> Dict[str, Any]:
        """
        Record analytics for a single user query.

        Args:
            query: User's original query.
            intent: Detected query intent.
            entities: Extracted entities such as fault codes or part numbers.
            processing_time: Query processing time in seconds.
            success: Whether query processing completed successfully.

        Returns:
            Dictionary containing the recorded query analytics.
        """
        record = {
            "query": query,
            "intent": intent,
            "entities": entities or {},
            "processing_time": processing_time,
            "success": success,
            "timestamp": datetime.utcnow().isoformat(),
        }

        self._queries.append(record)
        return record

    def total_queries(self) -> int:
        """Return the total number of recorded queries."""
        return len(self._queries)

    def successful_queries(self) -> int:
        """Return the number of successfully processed queries."""
        return sum(query["success"] for query in self._queries)

    def failed_queries(self) -> int:
        """Return the number of failed queries."""
        return sum(not query["success"] for query in self._queries)

    def success_rate(self) -> float:
        """Return the query success rate as a percentage."""
        total = self.total_queries()

        if total == 0:
            return 0.0

        return (self.successful_queries() / total) * 100

    def intent_distribution(self) -> Dict[str, int]:
        """Return the distribution of detected query intents."""
        intents = [
            query["intent"]
            for query in self._queries
            if query.get("intent")
        ]

        return dict(Counter(intents))

    def average_processing_time(self) -> float:
        """Return the average query processing time in seconds."""
        times = [
            query["processing_time"]
            for query in self._queries
            if query.get("processing_time") is not None
        ]

        if not times:
            return 0.0

        return sum(times) / len(times)

    def get_recent_queries(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Return the most recently recorded queries.

        Args:
            limit: Maximum number of queries to return.

        Returns:
            List of recent query records.
        """
        if limit <= 0:
            return []

        return self._queries[-limit:]

    def summary(self) -> Dict[str, Any]:
        """
        Generate a summary of query analytics.

        Returns:
            Dictionary containing aggregate query metrics.
        """
        return {
            "total_queries": self.total_queries(),
            "successful_queries": self.successful_queries(),
            "failed_queries": self.failed_queries(),
            "success_rate": self.success_rate(),
            "average_processing_time": self.average_processing_time(),
            "intent_distribution": self.intent_distribution(),
        }

    def clear(self) -> None:
        """Clear all recorded query analytics."""
        self._queries.clear()