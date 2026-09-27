"""
Standardized Flask API responses.
"""

from __future__ import annotations

from typing import Any

from flask import jsonify


def success_response(
    data: Any = None,
    message: str = "Request successful.",
    status_code: int = 200,
):
    """
    Create a standard success response.
    """

    return jsonify(
        {
            "success": True,
            "message": message,
            "data": data,
        }
    ), status_code


def error_response(
    message: str,
    status_code: int = 400,
    error: str | None = None,
):
    """
    Create a standard error response.
    """

    response = {
        "success": False,
        "message": message,
    }

    if error:
        response["error"] = error

    return jsonify(response), status_code


def health_response():
    """
    Health-check response.
    """

    return jsonify(
        {
            "success": True,
            "status": "healthy",
            "service": "PQ Assistant",
        }
    ), 200