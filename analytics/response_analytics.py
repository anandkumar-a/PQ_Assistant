"""
Response analytics for the PQ Assistant.

Tracks and summarizes generated response performance, including:
- Response generation time
- Response length
- Validation status
- Confidence scores
- Response success and failure
- Groundedness indicators
"""

from datetime import datetime
from typing import Any, Dict, List, Optional


class ResponseAnalytics:
    """Collects and analyzes response-generation metrics."""

    def __init__(self) -> None:
        """Initialize the response analytics tracker."""
        self._responses: List[Dict[str, Any]] = []

    def record_response(
        self,
        query: str,
        response: str,
        generation_time: Optional[float] = None,
        validation_status: Optional[str] = None,
        confidence_score: Optional[float] = None,
        grounded: Optional[bool] = None,
        success: bool = True,
    ) -> Dict[str, Any]:
        """
        Record analytics for a generated response.

        Args:
            query: Original user query.
            response: Generated response.
            generation_time: Response generation time in seconds.
            validation_status: Validation result such as
                'passed', 'failed', or 'warning'.
            confidence_score: Model or validation confidence score.
            grounded: Whether the response is grounded in retrieved
                enterprise documents.
            success: Whether response generation completed successfully.

        Returns:
            Dictionary containing the response analytics record.
        """
        record = {
            "query": query,
            "response": response,
            "response_length": len(response),
            "generation_time": generation_time,
            "validation_status": validation_status,
            "confidence_score": confidence_score,
            "grounded": grounded,
            "success": success,
            "timestamp": datetime.utcnow().isoformat(),
        }

        self._responses.append(record)
        return record

    def total_responses(self) -> int:
        """Return the total number of recorded responses."""
        return len(self._responses)

    def successful_responses(self) -> int:
        """Return the number of successfully generated responses."""
        return sum(
            response["success"]
            for response in self._responses
        )

    def failed_responses(self) -> int:
        """Return the number of failed responses."""
        return sum(
            not response["success"]
            for response in self._responses
        )

    def success_rate(self) -> float:
        """Return the response success rate as a percentage."""
        total = self.total_responses()

        if total == 0:
            return 0.0

        return (
            self.successful_responses() / total
        ) * 100

    def average_generation_time(self) -> float:
        """Return average response generation time in seconds."""
        times = [
            response["generation_time"]
            for response in self._responses
            if response.get("generation_time") is not None
        ]

        if not times:
            return 0.0

        return sum(times) / len(times)

    def average_response_length(self) -> float:
        """Return average response length in characters."""
        lengths = [
            response["response_length"]
            for response in self._responses
        ]

        if not lengths:
            return 0.0

        return sum(lengths) / len(lengths)

    def average_confidence_score(self) -> float:
        """Return the average confidence score."""
        scores = [
            response["confidence_score"]
            for response in self._responses
            if response.get("confidence_score") is not None
        ]

        if not scores:
            return 0.0

        return sum(scores) / len(scores)

    def validation_distribution(self) -> Dict[str, int]:
        """Return the distribution of validation outcomes."""
        distribution: Dict[str, int] = {}

        for response in self._responses:
            status = response.get("validation_status")

            if status:
                distribution[status] = (
                    distribution.get(status, 0) + 1
                )

        return distribution

    def grounded_response_rate(self) -> float:
        """
        Return the percentage of responses marked as grounded.

        Only responses with an explicit grounded value are considered.
        """
        grounded_values = [
            response["grounded"]
            for response in self._responses
            if response.get("grounded") is not None
        ]

        if not grounded_values:
            return 0.0

        grounded_count = sum(grounded_values)

        return (grounded_count / len(grounded_values)) * 100

    def get_recent_responses(
        self,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Return the most recently recorded responses.

        Args:
            limit: Maximum number of responses to return.

        Returns:
            List of recent response records.
        """
        if limit <= 0:
            return []

        return self._responses[-limit:]

    def summary(self) -> Dict[str, Any]:
        """
        Generate an aggregate response analytics summary.

        Returns:
            Dictionary containing response metrics.
        """
        return {
            "total_responses": self.total_responses(),
            "successful_responses": self.successful_responses(),
            "failed_responses": self.failed_responses(),
            "success_rate": self.success_rate(),
            "average_generation_time": (
                self.average_generation_time()
            ),
            "average_response_length": (
                self.average_response_length()
            ),
            "average_confidence_score": (
                self.average_confidence_score()
            ),
            "validation_distribution": (
                self.validation_distribution()
            ),
            "grounded_response_rate": (
                self.grounded_response_rate()
            ),
        }

    def clear(self) -> None:
        """Clear all recorded response analytics."""
        self._responses.clear()