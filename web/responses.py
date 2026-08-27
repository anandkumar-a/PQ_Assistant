
"""
Standardized API response utilities for the PQ Assistant.

Provides helper functions for creating consistent success,
error, and validation responses across the web layer.
"""

from typing import Any, Dict, Optional

from flask import jsonify


def success_response(
    data: Optional[Dict[str, Any]] = None,
    message: Optional[str] = None,
    status_code: int = 200,
):
    """
    Create a standardized successful API response.

    Args:
        data: Optional response data.
        message: Optional success message.
        status_code: HTTP status code.

    Returns:
        Flask JSON response.
    """
    response: Dict[str, Any] = {
        "success": True,
    }

    if message is not None:
        response["message"] = message

    if data is not None:
        response["data"] = data

    return jsonify(response), status_code


def error_response(
    message: str,
    status_code: int = 400,
    error_code: Optional[str] = None,
):
    """
    Create a standardized error API response.

    Args:
        message: Error description.
        status_code: HTTP status code.
        error_code: Optional application-specific error code.

    Returns:
        Flask JSON response.
    """
    response: Dict[str, Any] = {
        "success": False,
        "error": message,
    }

    if error_code is not None:
        response["error_code"] = error_code

    return jsonify(response), status_code


def validation_error_response(
    message: str = "Validation failed.",
    errors: Optional[Dict[str, Any]] = None,
):
    """
    Create a standardized validation error response.

    Args:
        message: Validation error message.
        errors: Optional field-level validation errors.

    Returns:
        Flask JSON response with HTTP 400 status.
    """
    response: Dict[str, Any] = {
        "success": False,
        "error": message,
    }

    if errors is not None:
        response["validation_errors"] = errors

    return jsonify(response), 400


def not_found_response(
    message: str = "Resource not found.",
):
    """
    Create a standardized 404 response.

    Args:
        message: Not-found message.

    Returns:
        Flask JSON response.
    """
    return error_response(
        message=message,
        status_code=404,
        error_code="NOT_FOUND",
    )


def server_error_response(
    message: str = "Internal server error.",
):
    """
    Create a standardized 500 response.

    Args:
        message: Error message.

    Returns:
        Flask JSON response.
    """
    return error_response(
        message=message,
        status_code=500,
        error_code="INTERNAL_SERVER_ERROR",
    )
