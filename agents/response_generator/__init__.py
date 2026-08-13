"""
Response Generator Agent
------------------------

This package generates grounded responses using the user's
query and the documents retrieved from the knowledge base.
"""

from .response_agent import ResponseGeneratorAgent

__all__ = [
    "ResponseGeneratorAgent",
]