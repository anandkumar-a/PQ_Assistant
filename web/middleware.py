
"""
Web middleware for the PQ Assistant.

Provides request logging, error handling, and common
Flask application middleware.
"""

import logging
import time
import uuid

from flask import Flask, g, jsonify, request


logger = logging.getLogger(__name__)


def register_middleware(app: Flask) -> None:
    """
    Register middleware handlers with the Flask application.

    Args:
        app: Flask application instance.
    """

    @app.before_request
    def before_request():
        """Initialize request metadata before processing."""
        g.request_id = str(uuid.uuid4())
        g.request_start_time = time.perf_counter()

        logger.info(
            "Request started | request_id=%s | method=%s | path=%s",
            g.request_id,
            request.method,
            request.path,
        )

    @app.after_request
    def after_request(response):
        """Log request completion and attach request ID."""
        start_time = getattr(g, "request_start_time", None)

        duration = (
            time.perf_counter() - start_time
            if start_time is not None
            else 0.0
        )

        response.headers["X-Request-ID"] = getattr(
            g,
            "request_id",
            "unknown",
        )

        logger.info(
            "Request completed | request_id=%s | method=%s | "
            "path=%s | status=%s | duration=%.4fs",
            getattr(g, "request_id", "unknown"),
            request.method,
            request.path,
            response.status_code,
            duration,
        )

        return response

    @app.errorhandler(400)
    def bad_request(error):
        """Handle HTTP 400 errors."""
        logger.warning(
            "Bad request | request_id=%s | error=%s",
            getattr(g, "request_id", "unknown"),
            error,
        )

        return jsonify(
            {
                "success": False,
                "error": "Bad request.",
                "request_id": getattr(g, "request_id", None),
            }
        ), 400

    @app.errorhandler(404)
    def not_found(error):
        """Handle HTTP 404 errors."""
        logger.warning(
            "Route not found | request_id=%s | path=%s",
            getattr(g, "request_id", "unknown"),
            request.path,
        )

        return jsonify(
            {
                "success": False,
                "error": "Endpoint not found.",
                "request_id": getattr(g, "request_id", None),
            }
        ), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        """Handle HTTP 405 errors."""
        logger.warning(
            "Method not allowed | request_id=%s | method=%s | path=%s",
            getattr(g, "request_id", "unknown"),
            request.method,
            request.path,
        )

        return jsonify(
            {
                "success": False,
                "error": "HTTP method not allowed.",
                "request_id": getattr(g, "request_id", None),
            }
        ), 405

    @app.errorhandler(500)
    def internal_server_error(error):
        """Handle unexpected server errors."""
        logger.exception(
            "Internal server error | request_id=%s",
            getattr(g, "request_id", "unknown"),
        )

        return jsonify(
            {
                "success": False,
                "error": "Internal server error.",
                "request_id": getattr(g, "request_id", None),
            }
        ), 500
