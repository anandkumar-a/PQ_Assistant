"""
Central analytics manager for the PQ Assistant.

Provides a unified interface for:
- Query analytics
- Retrieval analytics
- Response analytics
- Feedback analytics
- Performance analytics
"""

from typing import Any, Dict

from .query_analytics import QueryAnalytics
from .retrieval_analytics import RetrievalAnalytics
from .response_analytics import ResponseAnalytics
from .feedback_analytics import FeedbackAnalytics
from .performance_analytics import PerformanceAnalytics


class AnalyticsManager:
    """Coordinates all analytics components."""

    def __init__(self) -> None:
        """Initialize all analytics components."""
        self.query = QueryAnalytics()
        self.retrieval = RetrievalAnalytics()
        self.response = ResponseAnalytics()
        self.feedback = FeedbackAnalytics()
        self.performance = PerformanceAnalytics()

    def summary(self) -> Dict[str, Any]:
        """
        Return a complete analytics summary.

        Returns:
            Dictionary containing metrics from all analytics components.
        """
        return {
            "query": self.query.summary(),
            "retrieval": self.retrieval.summary(),
            "response": self.response.summary(),
            "feedback": self.feedback.summary(),
            "performance": self.performance.summary(),
        }

    def health_summary(self) -> Dict[str, Any]:
        """
        Return high-level system health metrics.

        Returns:
            Dictionary containing key health indicators.
        """
        query_summary = self.query.summary()
        retrieval_summary = self.retrieval.summary()
        response_summary = self.response.summary()
        feedback_summary = self.feedback.summary()
        performance_summary = self.performance.summary()

        return {
            "total_queries": query_summary["total_queries"],
            "query_success_rate": query_summary["success_rate"],
            "average_query_processing_time": (
                query_summary["average_processing_time"]
            ),
            "total_retrievals": retrieval_summary["total_retrievals"],
            "average_retrieval_time": (
                retrieval_summary["average_retrieval_time"]
            ),
            "total_responses": response_summary["total_responses"],
            "response_success_rate": (
                response_summary["success_rate"]
            ),
            "average_generation_time": (
                response_summary["average_generation_time"]
            ),
            "grounded_response_rate": (
                response_summary["grounded_response_rate"]
            ),
            "satisfaction_rate": (
                feedback_summary["satisfaction_rate"]
            ),
            "average_rating": (
                feedback_summary["average_rating"]
            ),
            "total_requests": performance_summary["total_requests"],
            "system_success_rate": (
                performance_summary["success_rate"]
            ),
            "average_request_time": (
                performance_summary["average_request_time"]
            ),
            "total_errors": performance_summary["total_errors"],
        }

    def clear_all(self) -> None:
        """Clear all analytics data."""
        self.query.clear()
        self.retrieval.clear()
        self.response.clear()
        self.feedback.clear()
        self.performance.clear()