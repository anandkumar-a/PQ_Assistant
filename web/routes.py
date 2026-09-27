"""
PQ Assistant Flask routes.

Endpoints:

GET  /
GET  /health

POST /query
POST /query/stream

POST /upload
POST /feedback

GET  /analytics
"""

from __future__ import annotations

import json
import logging
import time
import uuid
from pathlib import Path
from typing import Any

from flask import (
    Blueprint,
    Response,
    current_app,
    render_template,
    request,
    stream_with_context,
)

from .responses import (
    error_response,
    health_response,
    success_response,
)

from .schemas import (
    allowed_upload_extension,
    validate_feedback_payload,
    validate_query_payload,
)


logger = logging.getLogger(__name__)


# ============================================================
# BLUEPRINT
# ============================================================

web_bp = Blueprint(
    "web",
    __name__,
)


# ============================================================
# FRONTEND
# ============================================================

@web_bp.get("/")
def index():
    """
    Render the PQ Assistant frontend.
    """

    return render_template("index.html")


# ============================================================
# HEALTH
# ============================================================

@web_bp.get("/health")
def health():
    """
    Application health check.
    """

    return health_response()


# ============================================================
# PIPELINE ADAPTER
# ============================================================

def _get_pipeline():
    """
    Get the initialized PQ pipeline.

    The application factory stores the pipeline in:

        app.extensions["pq_pipeline"]
    """

    pipeline = current_app.extensions.get(
        "pq_pipeline"
    )

    if pipeline is None:
        raise RuntimeError(
            "PQ pipeline is not initialized."
        )

    return pipeline


def _execute_pipeline(
    query: str,
    top_k: int,
) -> dict[str, Any]:
    """
    Execute the existing PQ Assistant pipeline.

    This web layer does NOT implement RAG itself.

    The intended architecture remains:

        Query Understanding
                ↓
        Hybrid Retrieval
                ↓
        Response Generation
                ↓
        Validation
                ↓
        Final Answer
    """

    pipeline = _get_pipeline()

    try:
        result = pipeline.run(
            query=query,
            top_k=top_k,
        )

    except Exception:
        logger.exception(
            "PQ pipeline execution failed."
        )
        raise

    return _normalize_result(result)


def _sse_event(payload: dict[str, Any]) -> str:
    """
    Format a dictionary as a single Server-Sent Events message.
    """

    return (
        "data: "
        + json.dumps(
            payload,
            default=str,
        )
        + "\n\n"
    )


def _normalize_result(
    result: Any,
) -> dict[str, Any]:
    """
    Normalize pipeline output.
    """

    if isinstance(result, str):
        return {
            "answer": result,
            "sources": [],
            "confidence": None,
            "validated": True,
        }

    if not isinstance(result, dict):
        return {
            "answer": str(result),
            "sources": [],
            "confidence": None,
            "validated": True,
        }

    answer = (
        result.get("answer")
        or result.get("response")
        or result.get("final_answer")
        or result.get("content")
        or ""
    )

    sources = (
        result.get("sources")
        or result.get("documents")
        or result.get("contexts")
        or []
    )

    confidence = result.get(
        "confidence"
    )

    validated = result.get(
        "validated",
        result.get("is_valid", True),
    )

    return {
        **result,
        "answer": answer,
        "sources": sources,
        "confidence": confidence,
        "validated": validated,
    }


# ============================================================
# QUERY
# ============================================================

@web_bp.post("/query")
def query():
    """
    Process a Product Query.
    """

    if not request.is_json:
        return error_response(
            "Content-Type must be application/json.",
            415,
            "INVALID_CONTENT_TYPE",
        )

    payload = request.get_json(
        silent=True
    )

    validated, validation_error = (
        validate_query_payload(payload)
    )

    if validation_error:
        return error_response(
            validation_error,
            400,
            "VALIDATION_ERROR",
        )

    start_time = time.perf_counter()

    query_id = str(uuid.uuid4())

    try:
        result = _execute_pipeline(
            query=validated["query"],
            top_k=validated["top_k"],
        )

        elapsed = (
            time.perf_counter()
            - start_time
        )

        data = {
            "query_id": query_id,
            "query": validated["query"],
            "answer": result["answer"],
            "sources": result["sources"],
            "confidence": result["confidence"],
            "validated": result["validated"],
            "response_time": round(
                elapsed,
                4,
            ),
        }

        return success_response(
            data,
            "Query processed successfully.",
        )

    except Exception as exc:
        logger.exception(
            "Unable to process query %s.",
            query_id,
        )

        return error_response(
            "Unable to process the query.",
            500,
            str(exc),
        )


# ============================================================
# STREAMING QUERY
# ============================================================

@web_bp.post("/query/stream")
def query_stream():
    """
    Server-Sent Events endpoint.

    The frontend can consume this endpoint for
    ChatGPT-style streamed responses.
    """

    if not request.is_json:
        return error_response(
            "Content-Type must be application/json.",
            415,
            "INVALID_CONTENT_TYPE",
        )

    payload = request.get_json(
        silent=True
    )

    validated, validation_error = (
        validate_query_payload(payload)
    )

    if validation_error:
        return error_response(
            validation_error,
            400,
            "VALIDATION_ERROR",
        )

    def generate():
        query_id = str(uuid.uuid4())

        try:
            # Runs the full pipeline. Agent 3 already called Gemini
            # through its streaming API (see response_agent.generate);
            # this just means we now have the complete, Agent-4
            # validated answer plus the raw chunks Gemini produced it
            # in, ready to replay below.
            result = _execute_pipeline(
                query=validated["query"],
                top_k=validated["top_k"],
            )

            is_valid = result["validated"]

            yield _sse_event(
                {
                    "type": "status",
                    "query_id": query_id,
                    "stage": "validated",
                    "validated": is_valid,
                }
            )

            answer_chunks = result.get(
                "answer_chunks"
            ) or []

            if is_valid and answer_chunks:
                # Replay the already-validated tokens one at a time,
                # so the client still gets a live typing effect --
                # just after validation instead of before it.
                for chunk_text in answer_chunks:

                    yield _sse_event(
                        {
                            "type": "token",
                            "query_id": query_id,
                            "token": chunk_text,
                        }
                    )

            else:
                # Suppressed by Agent 4, or no chunk list was
                # available for some reason: send the answer
                # (e.g. "Insufficient evidence found") as one event.
                yield _sse_event(
                    {
                        "type": "token",
                        "query_id": query_id,
                        "token": result["answer"],
                    }
                )

            yield _sse_event(
                {
                    "type": "done",
                    "query_id": query_id,
                    "sources": result["sources"],
                    "confidence": result["confidence"],
                    "validated": is_valid,
                }
            )

            yield "data: [DONE]\n\n"

        except Exception as exc:
            logger.exception(
                "Streaming query failed."
            )

            yield _sse_event(
                {
                    "type": "error",
                    "query_id": query_id,
                    "message": str(exc),
                }
            )

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )
# ============================================================
# UPLOAD
# ============================================================

@web_bp.post("/upload")
def upload():
    """
    Upload enterprise knowledge documents.
    """

    if "file" not in request.files:
        return error_response(
            "No file was provided.",
            400,
            "FILE_MISSING",
        )

    uploaded_file = request.files["file"]

    if not uploaded_file.filename:
        return error_response(
            "Filename is missing.",
            400,
            "FILENAME_MISSING",
        )

    filename = Path(
        uploaded_file.filename
    ).name

    if not allowed_upload_extension(
        filename
    ):
        return error_response(
            (
                "Unsupported file type. "
                "Allowed types: PDF, DOCX, TXT."
            ),
            400,
            "UNSUPPORTED_FILE_TYPE",
        )

    upload_folder = Path(
        current_app.config[
            "UPLOAD_FOLDER"
        ]
    )

    upload_folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    destination = (
        upload_folder / filename
    )

    uploaded_file.save(
        destination
    )

    return success_response(
        {
            "filename": filename,
            "path": str(destination),
        },
        "File uploaded successfully.",
        201,
    )


# ============================================================
# FEEDBACK
# ============================================================

@web_bp.post("/feedback")
def feedback():
    """
    Store user feedback.
    """

    if not request.is_json:
        return error_response(
            "Content-Type must be application/json.",
            415,
            "INVALID_CONTENT_TYPE",
        )

    payload = request.get_json(
        silent=True
    )

    validated, validation_error = (
        validate_feedback_payload(payload)
    )

    if validation_error:
        return error_response(
            validation_error,
            400,
            "VALIDATION_ERROR",
        )

    feedback_service = (
        current_app.extensions.get(
            "feedback_service"
        )
    )

    if feedback_service is not None:

        create_method = getattr(
            feedback_service,
            "create",
            None,
        )

        if callable(create_method):
            try:
                create_method(
                    **validated
                )
            except Exception:
                logger.exception(
                    "Feedback service failed."
                )

    logger.info(
        "Feedback received | query_id=%s | rating=%s",
        validated["query_id"],
        validated["rating"],
    )

    return success_response(
        validated,
        "Feedback recorded successfully.",
    )


# ============================================================
# ANALYTICS
# ============================================================

@web_bp.get("/analytics")
def analytics():
    """
    Return analytics dashboard information.
    """

    manager = (
        current_app.extensions.get(
            "analytics_manager"
        )
    )

    if manager is not None:

        for method_name in (
            "summary",
            "get_summary",
            "dashboard",
            "get_dashboard",
        ):

            method = getattr(
                manager,
                method_name,
                None,
            )

            if callable(method):

                try:
                    result = method()

                    return success_response(
                        result,
                        "Analytics retrieved successfully.",
                    )

                except Exception:
                    logger.exception(
                        "Analytics retrieval failed."
                    )

    # Safe fallback.
    return success_response(
        {
            "total_queries": 0,
            "average_response_time": 0.0,
            "query_categories": {},
            "user_ratings": {},
            "validation_success_rate": 0.0,
            "retrieval_statistics": {},
        },
        "Analytics retrieved successfully.",
    )


# ============================================================
# ERROR HANDLERS
# ============================================================

@web_bp.errorhandler(404)
def not_found(error):
    return error_response(
        "The requested endpoint was not found.",
        404,
        "NOT_FOUND",
    )


@web_bp.errorhandler(405)
def method_not_allowed(error):
    return error_response(
        "HTTP method is not allowed.",
        405,
        "METHOD_NOT_ALLOWED",
    )


@web_bp.errorhandler(500)
def internal_server_error(error):
    logger.exception(
        "Unhandled internal server error."
    )

    return error_response(
        "Internal server error.",
        500,
        "INTERNAL_SERVER_ERROR",
    )