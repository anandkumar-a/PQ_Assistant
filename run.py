"""
PQ Assistant - Application Entry Point

Starts the Flask web application and exposes the complete
Agentic AI-Based Product Query Assistant workflow.

Workflow:
    User Query
        ↓
    Flask Web Layer
        ↓
    Pipeline / Orchestrator
        ↓
    Query Understanding Agent
        ↓
    Hybrid Retrieval
        ├── Dense Retrieval
        ├── Sparse BM25 Retrieval
        └── RRF Fusion
        ↓
    PQ Retrieval
        ↓
    Response Generation Agent
        ↓
    Validation Agent
        ↓
    Final Answer
        ↓
    Feedback / Analytics Storage

Run:
    python run.py

Production:
    gunicorn "web.app:create_app()"
"""

import os
import sys
import logging
from pathlib import Path

from dotenv import load_dotenv


# ---------------------------------------------------------------------------
# Project Root
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent

# Make sure the project root is available for imports
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ---------------------------------------------------------------------------
# Environment Configuration
# ---------------------------------------------------------------------------

ENV_FILE = PROJECT_ROOT / ".env"

if ENV_FILE.exists():
    load_dotenv(ENV_FILE)
else:
    # .env is optional because deployment platforms can provide
    # environment variables directly.
    load_dotenv()


# ---------------------------------------------------------------------------
# Logging Configuration
# ---------------------------------------------------------------------------

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    ),
)

logger = logging.getLogger("pq_assistant")


# ---------------------------------------------------------------------------
# Application Configuration
# ---------------------------------------------------------------------------

HOST = os.getenv("HOST", "0.0.0.0")

PORT = int(os.getenv("PORT", "5000"))

DEBUG = os.getenv("FLASK_DEBUG", "false").lower() in {
    "1",
    "true",
    "yes",
    "on",
}

# Flask development server should normally use threaded mode because
# your application supports SSE / streaming responses.
THREADED = os.getenv("FLASK_THREADED", "true").lower() in {
    "1",
    "true",
    "yes",
    "on",
}


# ---------------------------------------------------------------------------
# Required Project Directories
# ---------------------------------------------------------------------------

def create_required_directories():
    """
    Create runtime directories if they do not already exist.

    These directories are safe to create automatically and prevent
    runtime failures when the application starts for the first time.
    """

    directories = [
        PROJECT_ROOT / "logs",
        PROJECT_ROOT / "data",
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Application Factory
# ---------------------------------------------------------------------------

def create_application():
    """
    Import and create the Flask application.

    web.app is responsible for:
        - Flask initialization
        - Routes
        - Middleware
        - Request validation
        - Response handling
        - Pipeline integration
        - SSE responses
    """

    try:
        from web.app import create_app
    except ImportError as exc:
        logger.exception(
            "Unable to import Flask application from web.app"
        )
        raise ImportError(
            "\n\n"
            "Could not import create_app from web.app.\n"
            "Make sure web/app.py contains:\n\n"
            "    def create_app():\n"
            "        ...\n\n"
            f"Original error: {exc}\n"
        ) from exc

    return create_app()


# ---------------------------------------------------------------------------
# Startup Information
# ---------------------------------------------------------------------------

def print_startup_info():
    """
    Display useful startup information in the terminal.
    """

    logger.info("=" * 70)
    logger.info("PQ ASSISTANT")
    logger.info("Agentic AI-Based Product Query Assistant")
    logger.info("=" * 70)

    logger.info("Project Root : %s", PROJECT_ROOT)
    logger.info("Host         : %s", HOST)
    logger.info("Port         : %s", PORT)
    logger.info("Debug        : %s", DEBUG)
    logger.info("Threaded     : %s", THREADED)

    logger.info("-" * 70)
    logger.info("Workflow:")
    logger.info("  Query Understanding")
    logger.info("        ↓")
    logger.info("  Hybrid Retrieval")
    logger.info("        ↓")
    logger.info("  PQ Retrieval")
    logger.info("        ↓")
    logger.info("  Response Generation")
    logger.info("        ↓")
    logger.info("  Validation")
    logger.info("        ↓")
    logger.info("  Final Answer")
    logger.info("        ↓")
    logger.info("  Feedback / Analytics")
    logger.info("-" * 70)

    logger.info(
        "Application URL: http://localhost:%s",
        PORT,
    )

    logger.info("=" * 70)


# ---------------------------------------------------------------------------
# Main Entry Point
# ---------------------------------------------------------------------------

def main():
    """
    Main application entry point.

    This function:
        1. Creates required runtime directories.
        2. Creates the Flask application.
        3. Starts the Flask server.
        4. Exposes the complete PQ Assistant workflow.
    """

    try:
        create_required_directories()

        application = create_application()

        print_startup_info()

        logger.info("Starting PQ Assistant server...")

        application.run(
            host=HOST,
            port=PORT,
            debug=DEBUG,
            threaded=THREADED,
        )

    except KeyboardInterrupt:
        logger.info("PQ Assistant server stopped by user.")

    except Exception:
        logger.exception(
            "PQ Assistant failed during startup."
        )
        raise


# ---------------------------------------------------------------------------
# Script Execution
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    main()