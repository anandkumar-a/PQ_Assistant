from pathlib import Path
import os

from dotenv import load_dotenv

# ------------------------------------------------------------------
# Project Root
# ------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------------
# Load Environment Variables
# ------------------------------------------------------------------
load_dotenv(BASE_DIR / ".env")

# ------------------------------------------------------------------
# Application Settings
# ------------------------------------------------------------------
APP_NAME = "PQ Assistant"
APP_VERSION = "1.0.0"

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# ------------------------------------------------------------------
# API Keys
# ------------------------------------------------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# ------------------------------------------------------------------
# Directories
# ------------------------------------------------------------------
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
VECTOR_DB_DIR = DATA_DIR / "vector_store"
LOG_DIR = BASE_DIR / "logs"

# ------------------------------------------------------------------
# Models
# ------------------------------------------------------------------
EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2",
)

LLM_MODEL = os.getenv(
    "LLM_MODEL",
    "gpt-4.1-mini",
)

# ------------------------------------------------------------------
# Chunking Configuration
# ------------------------------------------------------------------
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 500))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 50))

# ------------------------------------------------------------------
# Retrieval Configuration
# ------------------------------------------------------------------
TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", 5))

# ------------------------------------------------------------------
# Logging
# ------------------------------------------------------------------
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")