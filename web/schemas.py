"""
Request validation schemas for the PQ Assistant web API.
"""

from __future__ import annotations

from typing import Any


MIN_QUERY_LENGTH = 2
MAX_QUERY_LENGTH = 5000

DEFAULT_TOP_K = 5
MAX_TOP_K = 20

ALLOWED_UPLOAD_EXTENSIONS = {
    "pdf",
    "docx",
    "txt",
}


def validate_query_payload(
    payload: Any,
) -> tuple[dict[str, Any] | None, str | None]:
    """
    Validate /query request data.

    Expected:

    {
        "query": "What is fault code E101?",
        "top_k": 5
    }
    """

    if not isinstance(payload, dict):
        return None, "Request body must be a JSON object."

    query = payload.get("query")

    if query is None:
        return None, "Missing required field: query."

    if not isinstance(query, str):
        return None, "Field 'query' must be a string."

    query = query.strip()

    if len(query) < MIN_QUERY_LENGTH:
        return None, "Query must contain at least 2 characters."

    if len(query) > MAX_QUERY_LENGTH:
        return None, (
            f"Query must not exceed {MAX_QUERY_LENGTH} characters."
        )

    top_k = payload.get("top_k", DEFAULT_TOP_K)

    try:
        top_k = int(top_k)
    except (TypeError, ValueError):
        return None, "Field 'top_k' must be an integer."

    if top_k < 1:
        return None, "Field 'top_k' must be at least 1."

    if top_k > MAX_TOP_K:
        return None, (
            f"Field 'top_k' must not exceed {MAX_TOP_K}."
        )

    return {
        "query": query,
        "top_k": top_k,
    }, None


def validate_feedback_payload(
    payload: Any,
) -> tuple[dict[str, Any] | None, str | None]:
    """
    Validate /feedback request data.
    """

    if not isinstance(payload, dict):
        return None, "Request body must be a JSON object."

    query_id = payload.get("query_id")

    if query_id is None:
        return None, "Missing required field: query_id."

    rating = payload.get("rating")

    if rating is None:
        return None, "Missing required field: rating."

    try:
        rating = int(rating)
    except (TypeError, ValueError):
        return None, "Field 'rating' must be an integer."

    if not 1 <= rating <= 5:
        return None, "Rating must be between 1 and 5."

    feedback = payload.get("feedback", "")

    if feedback is None:
        feedback = ""

    if not isinstance(feedback, str):
        return None, "Field 'feedback' must be a string."

    return {
        "query_id": str(query_id),
        "rating": rating,
        "feedback": feedback.strip(),
    }, None


def allowed_upload_extension(filename: str) -> bool:
    """
    Check whether an uploaded document is supported.
    """

    if not filename or "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()

    return extension in ALLOWED_UPLOAD_EXTENSIONS