"""
Performance analytics for the PQ Assistant.

Tracks and summarizes system performance, including:
- End-to-end request latency
- Agent execution time
- Retrieval latency
- Response generation latency
- Successful and failed requests
- Error distribution
- Throughput
"""

from collections import Counter
from datetime import datetime
from typing import Any, Dict, List, Optional


class PerformanceAnalytics:
    """Collects and analyzes PQ Assistant performance metrics."""

    def __init__(self) -> None:
        """Initialize the performance analytics tracker."""
        self._requests: List[Dict[str, Any]] = []
        self._agent_metrics: List[Dict[str, Any]] = []
        self._errors: List[Dict[str, Any]] = []

    def record_request(
        self,
        request_id: str,
        total_time: float,
        success: bool = True,
        error_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Record end-to-end request performance.

        Args:
            request_id: Unique identifier for the request.
            total_time: Total request processing time in seconds.
            success: Whether the request completed successfully.
            error_type: Optional error category when the request fails.

        Returns:
            Recorded request performance data.
        """
        record = {
            "request_id": request_id,
            "total_time": total_time,
            "success": success,
            "error_type": error_type,
            "timestamp": datetime.utcnow().isoformat(),
        }

        self._requests.append(record)

        if not success and error_type:
            self.record_error(
                request_id=request_id,
                error_type=error_type,
            )

        return record

    def record_agent_execution(
        self,
        request_id: str,
        agent_name: str,
        execution_time: float,
        success: bool = True,
    ) -> Dict[str, Any]:
        """
        Record execution time for an individual agent.

        Args:
            request_id: Request associated with the agent execution.
            agent_name: Name of the executing agent.
            execution_time: Agent execution time in seconds.
            success: Whether the agent execution succeeded.

        Returns:
            Recorded agent performance data.
        """
        record = {
            "request_id": request_id,
            "agent_name": agent_name,
            "execution_time": execution_time,
            "success": success,
            "timestamp": datetime.utcnow().isoformat(),
        }

        self._agent_metrics.append(record)
        return record

    def record_error(
        self,
        request_id: str,
        error_type: str,
        message: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Record a system error.

        Args:
            request_id: Request associated with the error.
            error_type: Category of the error.
            message: Optional error message.

        Returns:
            Recorded error information.
        """
        record = {
            "request_id": request_id,
            "error_type": error_type,
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
        }

        self._errors.append(record)
        return record

    def total_requests(self) -> int:
        """Return the total number of recorded requests."""
        return len(self._requests)

    def successful_requests(self) -> int:
        """Return the number of successful requests."""
        return sum(
            request["success"]
            for request in self._requests
        )

    def failed_requests(self) -> int:
        """Return the number of failed requests."""
        return sum(
            not request["success"]
            for request in self._requests
        )

    def success_rate(self) -> float:
        """Return the request success rate as a percentage."""
        total = self.total_requests()

        if total == 0:
            return 0.0

        return (
            self.successful_requests() / total
        ) * 100

    def average_request_time(self) -> float:
        """Return average end-to-end request latency."""
        times = [
            request["total_time"]
            for request in self._requests
        ]

        if not times:
            return 0.0

        return sum(times) / len(times)

    def average_agent_time(
        self,
        agent_name: Optional[str] = None,
    ) -> float:
        """
        Return average execution time for agents.

        Args:
            agent_name: Optional agent name to filter by.

        Returns:
            Average execution time in seconds.
        """
        metrics = self._agent_metrics

        if agent_name:
            metrics = [
                metric
                for metric in metrics
                if metric["agent_name"] == agent_name
            ]

        times = [
            metric["execution_time"]
            for metric in metrics
        ]

        if not times:
            return 0.0

        return sum(times) / len(times)

    def agent_performance(self) -> Dict[str, Dict[str, Any]]:
        """
        Return performance statistics grouped by agent.

        Returns:
            Dictionary containing execution statistics for each agent.
        """
        performance: Dict[str, Dict[str, Any]] = {}

        for metric in self._agent_metrics:
            agent_name = metric["agent_name"]

            if agent_name not in performance:
                performance[agent_name] = {
                    "execution_count": 0,
                    "total_time": 0.0,
                    "successful_executions": 0,
                    "failed_executions": 0,
                }

            data = performance[agent_name]

            data["execution_count"] += 1
            data["total_time"] += metric["execution_time"]

            if metric["success"]:
                data["successful_executions"] += 1
            else:
                data["failed_executions"] += 1

        for data in performance.values():
            count = data["execution_count"]

            data["average_execution_time"] = (
                data["total_time"] / count
                if count
                else 0.0
            )

        return performance

    def error_distribution(self) -> Dict[str, int]:
        """Return errors grouped by error type."""
        error_types = [
            error["error_type"]
            for error in self._errors
        ]

        return dict(Counter(error_types))

    def total_errors(self) -> int:
        """Return the total number of recorded errors."""
        return len(self._errors)

    def get_recent_requests(
        self,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """Return the most recent request performance records."""
        if limit <= 0:
            return []

        return self._requests[-limit:]

    def summary(self) -> Dict[str, Any]:
        """
        Generate an aggregate performance summary.

        Returns:
            Dictionary containing system performance metrics.
        """
        return {
            "total_requests": self.total_requests(),
            "successful_requests": self.successful_requests(),
            "failed_requests": self.failed_requests(),
            "success_rate": self.success_rate(),
            "average_request_time": self.average_request_time(),
            "total_errors": self.total_errors(),
            "error_distribution": self.error_distribution(),
            "agent_performance": self.agent_performance(),
        }

    def clear(self) -> None:
        """Clear all performance analytics."""
        self._requests.clear()
        self._agent_metrics.clear()
        self._errors.clear()