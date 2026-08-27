
"""
API routes for the PQ Assistant.

Defines HTTP endpoints for health checks, product queries,
and feedback submission.
"""

from flask import Blueprint, jsonify, request


web_bp = Blueprint("web", __name__)


@web_bp.route("/api/health", methods=["GET"])
def health_check():
    """
    Check whether the PQ Assistant API is running.

    Returns:
        JSON response containing API status.
    """
    return jsonify(
        {
            "status": "healthy",
            "service": "PQ Assistant API",
        }
    ), 200


@web_bp.route("/api/query", methods=["POST"])
def process_query():
    """
    Process a product query.

    Expected JSON:
        {
            "query": "User's product-related question"
        }

    Returns:
        JSON response containing the submitted query.
    """
    data = request.get_json(silent=True) or {}
    query = data.get("query")

    if not query:
        return jsonify(
            {
                "success": False,
                "error": "Query is required.",
            }
        ), 400

    query = query.strip()

    if not query:
        return jsonify(
            {
                "success": False,
                "error": "Query cannot be empty.",
            }
        ), 400

    # Pipeline/agent integration will be added here.
    return jsonify(
        {
            "success": True,
            "query": query,
            "message": "Query received successfully.",
        }
    ), 200


@web_bp.route("/api/feedback", methods=["POST"])
def submit_feedback():
    """
    Submit feedback for a PQ Assistant response.

    Expected JSON:
        {
            "query_id": "unique-query-id",
            "rating": 5,
            "feedback": "Helpful response"
        }

    Returns:
        JSON response confirming feedback submission.
    """
    data = request.get_json(silent=True) or {}

    query_id = data.get("query_id")
    rating = data.get("rating")
    feedback = data.get("feedback")

    if not query_id:
        return jsonify(
            {
                "success": False,
                "error": "query_id is required.",
            }
        ), 400

    if rating is None:
        return jsonify(
            {
                "success": False,
                "error": "rating is required.",
            }
        ), 400

    return jsonify(
        {
            "success": True,
            "query_id": query_id,
            "rating": rating,
            "feedback": feedback,
            "message": "Feedback received successfully.",
        }
    ), 200

