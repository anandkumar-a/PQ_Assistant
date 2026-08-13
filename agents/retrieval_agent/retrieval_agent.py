"""
Retrieval Agent
---------------

Coordinates document retrieval for the PQ Assistant.

The agent receives structured query information from the
Query Understanding Agent and uses the Hybrid Retriever
to find the most relevant documents.
"""

import logging
from typing import Any, Dict, List, Optional


logger = logging.getLogger(__name__)


class RetrievalAgent:
    """
    Agent responsible for retrieving relevant information
    from the knowledge base.
    """

    def __init__(
        self,
        hybrid_retriever=None,
        default_top_k: int = 5,
    ):
        """
        Initialize the Retrieval Agent.

        Args:
            hybrid_retriever:
                Instance of the HybridRetriever.
            default_top_k:
                Default number of documents to retrieve.
        """

        self.hybrid_retriever = hybrid_retriever
        self.default_top_k = default_top_k

    def build_search_query(
        self,
        query_data: Dict[str, Any],
    ) -> str:
        """
        Build an optimized search query from the structured
        query understanding result.

        Args:
            query_data:
                Structured output from QueryUnderstandingAgent.

        Returns:
            Optimized query string.
        """

        original_query = query_data.get(
            "original_query",
            "",
        )

        keywords = query_data.get(
            "keywords",
            [],
        )

        fault_codes = query_data.get(
            "fault_codes",
            [],
        )

        part_numbers = query_data.get(
            "part_numbers",
            [],
        )

        search_terms = []

        if original_query:
            search_terms.append(original_query)

        search_terms.extend(fault_codes)
        search_terms.extend(part_numbers)
        search_terms.extend(keywords)

        return " ".join(
            dict.fromkeys(search_terms)
        )

    def retrieve(
        self,
        query_data: Dict[str, Any],
        top_k: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents using the Hybrid Retriever.

        Args:
            query_data:
                Output from QueryUnderstandingAgent.
            top_k:
                Number of documents to retrieve.

        Returns:
            List of relevant retrieved documents.
        """

        if self.hybrid_retriever is None:
            raise ValueError(
                "HybridRetriever has not been initialized."
            )

        top_k = top_k or self.default_top_k

        search_query = self.build_search_query(
            query_data
        )

        logger.info(
            "Retrieving documents for query: %s",
            search_query,
        )

        try:
            results = self.hybrid_retriever.retrieve(
                query=search_query,
                top_k=top_k,
            )

            logger.info(
                "Retrieved %d documents.",
                len(results),
            )

            return results

        except Exception as error:

            logger.exception(
                "Document retrieval failed."
            )

            raise RuntimeError(
                f"Retrieval failed: {str(error)}"
            ) from error

    def process(
        self,
        query_data: Dict[str, Any],
        top_k: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Execute the complete retrieval process.

        Args:
            query_data:
                Structured query information.
            top_k:
                Number of documents to retrieve.

        Returns:
            Dictionary containing query details and
            retrieved documents.
        """

        search_query = self.build_search_query(
            query_data
        )

        results = self.retrieve(
            query_data=query_data,
            top_k=top_k,
        )

        return {
            "search_query": search_query,
            "intent": query_data.get(
                "intent",
                "general_query",
            ),
            "retrieved_documents": results,
            "total_results": len(results),
        }