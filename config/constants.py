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
#
# These values are FIXED per the project spec: "Chunk size is
# fixed at 512 tokens with 50-token overlap -- do not change
# without re-embedding." They deliberately live here rather than
# in settings.py (which allows environment-variable overrides),
# because changing them silently via an env var would desync
# newly ingested chunks from whatever is already embedded in
# ChromaDB, without triggering the required re-embedding.
#
# CHUNK_ENCODING is the tiktoken encoding used to COUNT tokens
# when chunking (see ingestion/chunkers/recursive_chunker.py).
# It does not need to match Gemini's own tokenizer exactly --
# it only needs to give a consistent, reproducible token count
# so "512 tokens" means the same thing every time chunks are
# built.

CHUNK_SIZE = 512
CHUNK_OVERLAP = 50
CHUNK_ENCODING = "cl100k_base"
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
# Validation (Agent 4)
# ===========================================================

# Minimum embedding-similarity grounding score an answer must
# reach against its retrieved source chunks before it is shown
# to the user. Below this, Agent 4 suppresses the response.
GROUNDING_THRESHOLD = 0.70

# ===========================================================
# Database
# ===========================================================

DEFAULT_COLLECTION_NAME = "pq_documents"

# ===========================================================
# Logging
# ===========================================================

LOG_SEPARATOR = "=" * 60

