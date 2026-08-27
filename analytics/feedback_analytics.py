"""
Feedback analytics for the PQ Assistant.

Tracks and summarizes user feedback, including:
- Positive and negative feedback
- Rating scores
- Feedback comments
- Satisfaction rate
- Feedback distribution
"""

from collections import Counter
from datetime import datetime
from typing import Any, Dict, List, Optional, Union


class FeedbackAnalytics:
    """Collects and analyzes user feedback."""

    def __init__(self) -> None:
        """Initialize the feedback analytics tracker."""
        self._feedback: List[Dict[str, Any]] = []

    def record_feedback(
        self,
        query: str,
        feedback: str,
        rating: Optional[Union[int, float]] = None,
        comment: Optional[str] = None,
        response_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Record feedback for a generated response.

        Args:
            query: Original user query.
            feedback: Feedback type, such as 'positive' or 'negative'.
            rating: Optional numerical rating, normally between 1 and 5.
            comment: Optional user feedback comment.
            response_id: Optional identifier for the associated response.

        Returns:
            Dictionary containing the feedback record.

        Raises:
            ValueError: If feedback type or rating is invalid.
        """
        normalized_feedback = feedback.strip().lower()

        if normalized_feedback not in {"positive", "negative"}:
            raise ValueError(
                "feedback must be either 'positive' or 'negative'."
            )

        if rating is not None and not 1 <= rating <= 5:
            raise ValueError(
                "rating must be between 1 and 5."
            )

        record = {
            "query": query,
            "feedback": normalized_feedback,
            "rating": rating,
            "comment": comment,
            "response_id": response_id,
            "timestamp": datetime.utcnow().isoformat(),
        }

        self._feedback.append(record)
        return record

    def total_feedback(self) -> int:
        """Return the total number of feedback records."""
        return len(self._feedback)

    def positive_feedback(self) -> int:
        """Return the number of positive feedback records."""
        return sum(
            item["feedback"] == "positive"
            for item in self._feedback
        )

    def negative_feedback(self) -> int:
        """Return the number of negative feedback records."""
        return sum(
            item["feedback"] == "negative"
            for item in self._feedback
        )

    def satisfaction_rate(self) -> float:
        """Return the positive feedback rate as a percentage."""
        total = self.total_feedback()

        if total == 0:
            return 0.0

        return (
            self.positive_feedback() / total
        ) * 100

    def average_rating(self) -> float:
        """Return the average numerical rating."""
        ratings = [
            item["rating"]
            for item in self._feedback
            if item.get("rating") is not None
        ]

        if not ratings:
            return 0.0

        return sum(ratings) / len(ratings)

    def rating_distribution(self) -> Dict[str, int]:
        """Return the distribution of numerical ratings."""
        ratings = [
            item["rating"]
            for item in self._feedback
            if item.get("rating") is not None
        ]

        return dict(
            Counter(str(rating) for rating in ratings)
        )

    def feedback_distribution(self) -> Dict[str, int]:
        """Return positive and negative feedback counts."""
        return {
            "positive": self.positive_feedback(),
            "negative": self.negative_feedback(),
        }

    def comments(self) -> List[str]:
        """Return all non-empty feedback comments."""
        return [
            item["comment"]
            for item in self._feedback
            if item.get("comment")
        ]

    def get_recent_feedback(
        self,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Return the most recent feedback records.

        Args:
            limit: Maximum number of records to return.

        Returns:
            List of recent feedback records.
        """
        if limit <= 0:
            return []

        return self._feedback[-limit:]

    def summary(self) -> Dict[str, Any]:
        """
        Generate an aggregate feedback analytics summary.

        Returns:
            Dictionary containing feedback metrics.
        """
        return {
            "total_feedback": self.total_feedback(),
            "positive_feedback": self.positive_feedback(),
            "negative_feedback": self.negative_feedback(),
            "satisfaction_rate": self.satisfaction_rate(),
            "average_rating": self.average_rating(),
            "rating_distribution": self.rating_distribution(),
            "feedback_distribution": self.feedback_distribution(),
            "comment_count": len(self.comments()),
        }

    def clear(self) -> None:
        """Clear all recorded feedback analytics."""
        self._feedback.clear()