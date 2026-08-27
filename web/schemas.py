
"""
Request and response schemas for the PQ Assistant web API.

Provides lightweight validation helpers for incoming requests
and standardized response structures.
"""

from typing import Any, Dict, Optional


class QueryRequestSchema:
    """Schema for validating PQ Assistant query requests."""

    REQUIRED_FIELDS = {"query"}

    @classmethod
    def validate(cls, data: Optional[Dict[str, Any]]) -> tuple[bool, Optional[str]]:
        """
        Validate a query request.

        Args:
            data: Request payload.

        Returns:
            Tuple containing validation status and error message.
        """
        if not isinstance(data, dict):
            return False, "Request body must be a JSON object."

        query = data.get("query")

        if query is None:
            return False, "Query is required."

        if not isinstance(query, str):
            return False, "Query must be a string."

        if not query.strip():
            return False, "Query cannot be empty."

        return True, None


class FeedbackRequestSchema:
    """Schema for validating feedback requests."""

    REQUIRED_FIELDS = {"query_id", "rating"}

    @classmethod
    def validate(cls, data: Optional[Dict[str, Any]]) -> tuple[bool, Optional[str]]:
        """
        Validate a feedback request.

        Args:
            data: Request payload.

        Returns:
            Tuple containing validation status and error message.
        """
        if not isinstance(data, dict):
            return False, "Request body must be a JSON object."

        query_id = data.get("query_id")
        rating = data.get("rating")

        if not query_id:
            return False, "query_id is required."

        if not isinstance(query_id, str):
            return False, "query_id must be a string."

        if rating is None:
            return False, "rating is required."

        if not isinstance(rating, (int, float)) or isinstance(rating, bool):
            return False, "rating must be a number."

        if not 1 <= rating <= 5:
            return False, "rating must be between 1 and 5."

        return True, None


class QueryResponseSchema:
    """Schema for standardized PQ query responses."""

    @staticmethod
    def success(
        query: str,
        answer: str,
        query_id: Optional[str] = None,
        sources: Optional[list] = None,
    ) -> Dict[str, Any]:
        """
        Build a successful query response.

        Args:
            query: Original user query.
            answer: Generated answer.
            query_id: Optional query identifier.
            sources: Optional source documents.

        Returns:
            Standardized response dictionary.
        """
        response = {
            "success": True,
            "query": query,
            "answer": answer,
            "sources": sources or [],
        }

        if query_id:
            response["query_id"] = query_id

        return response

    @staticmethod
    def error(message: str) -> Dict[str, Any]:
        """
        Build a standardized error response.

        Args:
            message: Error description.

        Returns:
            Standardized error dictionary.
        """
        return {
            "success": False,
            "error": message,
        }


class FeedbackResponseSchema:
    """Schema for standardized feedback responses."""

    @staticmethod
    def success(query_id: str) -> Dict[str, Any]:
        """
        Build a successful feedback response.

        Args:
            query_id: Identifier of the related query.

        Returns:
            Standardized response dictionary.
        """
        return {
            "success": True,
            "query_id": query_id,
            "message": "Feedback submitted successfully.",
        }

    @staticmethod
    def error(message: str) -> Dict[str, Any]:
        """
        Build a standardized feedback error response.

        Args:
            message: Error description.

        Returns:
            Standardized error dictionary.
        """
        return {
            "success": False,
            "error": message,
        }
