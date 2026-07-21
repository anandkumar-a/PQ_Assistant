"""
===========================================================
Project: PQ Assistant
Module : Configuration Constants
File   : constants.py
===========================================================

This module contains reusable constant values that remain
fixed throughout the application.

Do not store:
- API Keys
- Passwords
- Secrets
- Environment-specific configurations

Those belong in settings.py.
"""

# ===========================================================
# Document Processing
# ===========================================================

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
MIN_CHUNK_LENGTH = 100

# ===========================================================
# Retrieval
# ===========================================================

DEFAULT_TOP_K = 5
SIMILARITY_THRESHOLD = 0.75

# ===========================================================
# API
# ===========================================================

DEFAULT_TIMEOUT = 30  # seconds
MAX_RETRIES = 3

# ===========================================================
# Upload
# ===========================================================

MAX_FILE_SIZE_MB = 20

SUPPORTED_FILE_TYPES = (
    ".pdf",
    ".docx",
    ".txt",
    ".md",
)

# ===========================================================
# Query Validation
# ===========================================================

MIN_QUERY_LENGTH = 3
MAX_QUERY_LENGTH = 1000

# ===========================================================
# Database
# ===========================================================

DEFAULT_COLLECTION_NAME = "pq_documents"

# ===========================================================
# Logging
# ===========================================================

LOG_SEPARATOR = "=" * 60