"""
Query Understanding Agent
-------------------------

This package analyzes incoming user queries and extracts
structured information required for the PQ Assistant pipeline.

Responsibilities:
    - Detect user intent
    - Extract important keywords
    - Identify product names
    - Identify part numbers
    - Identify fault/error codes
    - Classify query category
"""

from .query_agent import QueryUnderstandingAgent

__all__ = [
    "QueryUnderstandingAgent",
]