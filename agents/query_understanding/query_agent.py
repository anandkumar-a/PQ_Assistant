"""
Query Understanding Agent
-------------------------

Analyzes a user query and extracts structured information
that can be used by the retrieval and response generation agents.
"""

import re
from typing import Dict, List, Optional


class QueryUnderstandingAgent:
    """
    Agent responsible for understanding and preprocessing
    product-related user queries.
    """

    def __init__(self):
        """
        Initialize the Query Understanding Agent.
        """

        self.intent_patterns = {
            "fault_diagnosis": [
                "error",
                "fault",
                "issue",
                "problem",
                "failure",
                "not working",
                "malfunction",
            ],
            "installation": [
                "install",
                "installation",
                "setup",
                "configure",
                "configuration",
            ],
            "maintenance": [
                "maintenance",
                "service",
                "repair",
                "clean",
                "inspection",
            ],
            "troubleshooting": [
                "troubleshoot",
                "troubleshooting",
                "fix",
                "resolve",
                "solution",
            ],
            "product_information": [
                "what is",
                "specification",
                "details",
                "information",
                "features",
            ],
            "spare_parts": [
                "part number",
                "spare part",
                "replacement",
                "component",
            ],
        }

    def detect_intent(self, query: str) -> str:
        """
        Detect the primary intent of the user query.

        Args:
            query: User input query.

        Returns:
            Detected intent.
        """

        query_lower = query.lower()

        for intent, keywords in self.intent_patterns.items():
            for keyword in keywords:
                if keyword in query_lower:
                    return intent

        return "general_query"

    def extract_keywords(self, query: str) -> List[str]:
        """
        Extract meaningful keywords from the query.

        Args:
            query: User input query.

        Returns:
            List of extracted keywords.
        """

        stop_words = {
            "the",
            "is",
            "a",
            "an",
            "and",
            "or",
            "for",
            "to",
            "of",
            "in",
            "on",
            "with",
            "my",
            "i",
            "how",
            "what",
            "why",
            "when",
        }

        words = re.findall(r"\b\w+\b", query.lower())

        keywords = [
            word
            for word in words
            if word not in stop_words and len(word) > 2
        ]

        return list(set(keywords))

    def extract_fault_codes(self, query: str) -> List[str]:
        """
        Extract possible fault or error codes.

        Examples:
            E101
            ERR-404
            F23
            CODE123

        Args:
            query: User input query.

        Returns:
            List of detected fault codes.
        """

        pattern = r"\b(?:ERR[-_]?\d+|E\d+|F\d+|CODE[-_]?\d+)\b"

        matches = re.findall(
            pattern,
            query,
            flags=re.IGNORECASE,
        )

        return list(set(matches))

    def extract_part_numbers(self, query: str) -> List[str]:
        """
        Extract possible product or spare part numbers.

        Examples:
            ABC-123
            XZ456
            PART-001

        Args:
            query: User input query.

        Returns:
            List of detected part numbers.
        """

        pattern = r"\b[A-Z]{2,}[-_]?\d{2,}\b"

        matches = re.findall(
            pattern,
            query,
            flags=re.IGNORECASE,
        )

        return list(set(matches))

    def understand(
        self,
        query: str,
    ) -> Dict[str, object]:
        """
        Perform complete query understanding.

        Args:
            query: User input query.

        Returns:
            Dictionary containing structured query information.
        """

        if not query or not query.strip():
            raise ValueError("Query cannot be empty.")

        intent = self.detect_intent(query)

        keywords = self.extract_keywords(query)

        fault_codes = self.extract_fault_codes(query)

        part_numbers = self.extract_part_numbers(query)

        return {
            "original_query": query,
            "intent": intent,
            "keywords": keywords,
            "fault_codes": fault_codes,
            "part_numbers": part_numbers,
        }