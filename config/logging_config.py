"""
Logging configuration for PQ Assistant.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from config.settings import LOG_DIR, LOG_LEVEL


def configure_logging() -> logging.Logger:
    """
    Configure application logging.

    Returns:
        logging.Logger: PQ Assistant logger.
    """

    # --------------------------------------------------------------
    # Create log directory
    # --------------------------------------------------------------

    log_directory = Path(LOG_DIR)

    log_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    # --------------------------------------------------------------
    # Determine logging level
    # --------------------------------------------------------------

    level = getattr(
        logging,
        LOG_LEVEL.upper(),
        logging.INFO,
    )

    # --------------------------------------------------------------
    # Application logger
    # --------------------------------------------------------------

    logger = logging.getLogger(
        "pq_assistant"
    )

    logger.setLevel(level)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    # --------------------------------------------------------------
    # Formatter
    # --------------------------------------------------------------

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # --------------------------------------------------------------
    # Console handler
    # --------------------------------------------------------------

    console_handler = logging.StreamHandler()

    console_handler.setLevel(level)

    console_handler.setFormatter(
        formatter
    )

    # --------------------------------------------------------------
    # Application log
    # --------------------------------------------------------------

    application_log = (
        log_directory / "application.log"
    )

    application_handler = RotatingFileHandler(
        application_log,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )

    application_handler.setLevel(level)

    application_handler.setFormatter(
        formatter
    )

    # --------------------------------------------------------------
    # Error log
    # --------------------------------------------------------------

    error_log = (
        log_directory / "error.log"
    )

    error_handler = RotatingFileHandler(
        error_log,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )

    error_handler.setLevel(
        logging.ERROR
    )

    error_handler.setFormatter(
        formatter
    )

    # --------------------------------------------------------------
    # Register handlers
    # --------------------------------------------------------------

    logger.addHandler(
        console_handler
    )

    logger.addHandler(
        application_handler
    )

    logger.addHandler(
        error_handler
    )

    return logger