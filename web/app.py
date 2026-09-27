"""
Flask application factory for PQ Assistant.
"""

from flask import Flask

from config.logging_config import configure_logging
from config import constants, settings
from agents.response_generator.llm_factory import build_gemini_llm
from web.routes import web_bp

from embeddings.embedding_generator import EmbeddingGenerator
from retrieval.dense.vector_retriever import VectorRetriever
from retrieval.sparse.bm25_retriever import BM25Retriever
from retrieval.hybrid.hybrid_retriever import HybridRetriever
from agents.query_understanding.query_agent import QueryUnderstandingAgent
from agents.retrieval_agent.retrieval_agent import RetrievalAgent
from agents.response_generator.response_agent import ResponseGeneratorAgent
from agents.validation_agent.validation_agent import ValidationAgent
from pipeline.pq_pipeline import PQPipeline


def _load_indexed_chunks(logger):
    """
    Load previously ingested chunks for BM25 indexing.

    TODO: there is currently no working ingestion -> persisted-chunk
    path wired end-to-end (see the two disconnected SQLite layers
    under database/sqlite/ vs database/repositories/, neither of
    which defines a chunks table yet). Until that is fixed, this
    always returns an empty list, and hybrid retrieval degrades
    gracefully (see build_pipeline() below) rather than crashing
    the app at startup.
    """

    logger.warning(
        "No chunk-loading path is wired yet; BM25 index will start "
        "empty until the ingestion pipeline is connected to "
        "persistent storage."
    )

    return []


def build_pipeline(logger) -> PQPipeline:
    """
    Construct the PQ Assistant pipeline with real, shared components.

    Falls back to an uninitialized RetrievalAgent/ResponseGeneratorAgent
    (which raise clear errors only when actually queried) if a
    dependency isn't ready yet, so the app always boots even before
    ingestion or LLM wiring is complete.
    """

    embedding_generator = EmbeddingGenerator()

    vector_retriever = VectorRetriever(
        collection_name=constants.DEFAULT_COLLECTION_NAME,
        persist_directory=str(settings.VECTOR_DB_DIR),
    )

    indexed_chunks = _load_indexed_chunks(logger)

    hybrid_retriever = None

    try:
        bm25_retriever = BM25Retriever(documents=indexed_chunks)

        hybrid_retriever = HybridRetriever(
            vector_retriever=vector_retriever,
            bm25_retriever=bm25_retriever,
        )

    except ValueError:
        logger.warning(
            "Hybrid retriever not built (no ingested documents yet). "
            "Queries will fail at Agent 2 with a clear error until "
            "the ingestion pipeline has been run."
        )

    retrieval_agent = RetrievalAgent(
        hybrid_retriever=hybrid_retriever,
        embedding_generator=embedding_generator,
    )

    # Build the real Gemini client. Falls back to llm=None (Agent 3
    # will then raise a clear "LLM has not been initialized" error
    # only when actually queried) if GOOGLE_API_KEY isn't set yet,
    # so the app still boots in a dev environment without a key.
    llm = None

    try:
        llm = build_gemini_llm()

    except RuntimeError as error:
        logger.warning(
            "Gemini LLM not initialized: %s",
            error,
        )

    response_agent = ResponseGeneratorAgent(llm=llm)

   
    validation_agent = ValidationAgent(
        embedding_generator=embedding_generator,
    )

    return PQPipeline(
        query_agent=QueryUnderstandingAgent(),
        retrieval_agent=retrieval_agent,
        response_agent=response_agent,
        validation_agent=validation_agent,
    )


def create_app():
    """
    Create and configure the PQ Assistant Flask application.

    Returns:
        Flask: Configured Flask application.
    """

    # --------------------------------------------------------------
    # Configure logging
    # --------------------------------------------------------------

    logger = configure_logging()

    # --------------------------------------------------------------
    # Create Flask application
    # --------------------------------------------------------------

    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )

    # --------------------------------------------------------------
    # Application configuration
    # --------------------------------------------------------------

    app.config["APP_NAME"] = settings.APP_NAME
    app.config["APP_VERSION"] = settings.APP_VERSION
    app.config["ENVIRONMENT"] = settings.ENVIRONMENT
    app.config["DEBUG"] = settings.DEBUG

    # --------------------------------------------------------------
    # Build and register the PQ pipeline
    # This previously never happened, so every request would fail
    # with "PQ pipeline is not initialized."
    # --------------------------------------------------------------

    app.extensions["pq_pipeline"] = build_pipeline(logger)

    # --------------------------------------------------------------
    # Register routes
    # --------------------------------------------------------------

    app.register_blueprint(web_bp)

    # --------------------------------------------------------------
    # Startup log
    # --------------------------------------------------------------

    logger.info(
        "%s v%s Flask application created.",
        settings.APP_NAME,
        settings.APP_VERSION,
    )

    return app