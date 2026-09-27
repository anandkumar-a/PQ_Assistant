"""
Flask middleware for the PQ Assistant.
"""

from __future__ import annotations

import time
import uuid

from flask import Flask, g


def register_middleware(app: Flask) -> None:
    """
    Register application middleware.
    """

    @app.before_request
    def before_request():
        g.request_id = str(uuid.uuid4())
        g.request_start_time = time.perf_counter()

    @app.after_request
    def after_request(response):
        start_time = getattr(
            g,
            "request_start_time",
            None,
        )

        if start_time is not None:
            elapsed = time.perf_counter() - start_time

            response.headers["X-Response-Time"] = (
                f"{elapsed:.4f}s"
            )

        request_id = getattr(
            g,
            "request_id",
            None,
        )

        if request_id:
            response.headers["X-Request-ID"] = request_id

        return response

    @app.after_request
    def security_headers(response):
        response.headers.setdefault(
            "X-Content-Type-Options",
            "nosniff",
        )

        response.headers.setdefault(
            "X-Frame-Options",
            "SAMEORIGIN",
        )

        response.headers.setdefault(
            "Referrer-Policy",
            "strict-origin-when-cross-origin",
        )

        return response