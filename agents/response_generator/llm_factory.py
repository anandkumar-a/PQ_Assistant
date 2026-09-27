"""
Gemini LLM Factory
------------------

Builds the LangChain-compatible Gemini chat model used by the
Response Generation Agent (Agent 3).

Centralizing construction here means API-key validation and model
selection happen in exactly one place, instead of being duplicated
anywhere an LLM is needed (e.g. evaluation scripts, future agents).
"""

import logging

from langchain_google_genai import ChatGoogleGenerativeAI

from config import settings


logger = logging.getLogger(__name__)


def build_gemini_llm() -> ChatGoogleGenerativeAI:
    """
    Construct a configured Gemini chat model.

    Returns:
        ChatGoogleGenerativeAI: a LangChain chat model. It exposes
        .invoke() (used today by ResponseGeneratorAgent.generate())
        and .stream() (needed for real token-by-token SSE streaming,
        which is the next fix after this one).

    Raises:
        RuntimeError: if GOOGLE_API_KEY is not set, so the app fails
            with a clear message instead of a confusing traceback
            deep inside the Gemini SDK.
    """

    if not settings.GOOGLE_API_KEY:
        raise RuntimeError(
            "GOOGLE_API_KEY is not set. Add it to your .env file "
            "(see .env.example) before starting the app."
        )

    logger.info(
        "Initializing Gemini LLM: %s",
        settings.LLM_MODEL,
    )

    return ChatGoogleGenerativeAI(
        model=settings.LLM_MODEL,
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=0.2,
        convert_system_message_to_human=True,
    )