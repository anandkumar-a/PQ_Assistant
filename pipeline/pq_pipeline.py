"""
Main orchestration pipeline for the PQ Assistant.

Workflow:
Query Understanding
        ↓
Retrieval
        ↓
Response Generation
        ↓
Validation
        ↓
Final Answer
"""

from typing import Any, Dict, Optional

from agents.query_understanding.query_agent import QueryUnderstandingAgent
from agents.retrieval_agent.retrieval_agent import RetrievalAgent
from agents.response_generator.response_agent import ResponseGenerationAgent
from agents.validation_agent.validation_agent import ValidationAgent


class PQPipeline:
    """
    Orchestrates the complete Product Query Assistant workflow.
    """

    def __init__(
        self,
        query_agent: Optional[QueryUnderstandingAgent] = None,
        retrieval_agent: Optional[RetrievalAgent] = None,
        response_agent: Optional[ResponseGenerationAgent] = None,
        validation_agent: Optional[ValidationAgent] = None,
    ):
        """
        Initialize the PQ pipeline with the required agents.

        Agents can be injected externally to make the pipeline
        easier to test and maintain.
        """

        self.query_agent = query_agent or QueryUnderstandingAgent()
        self.retrieval_agent = retrieval_agent or RetrievalAgent()
        self.response_agent = response_agent or ResponseGenerationAgent()
        self.validation_agent = validation_agent or ValidationAgent()

    def run(self, query: str) -> Dict[str, Any]:
        """
        Execute the complete PQ Assistant workflow.

        Args:
            query: User's product-related question.

        Returns:
            Dictionary containing the final answer and pipeline results.
        """

        if not query or not query.strip():
            raise ValueError("Query cannot be empty.")

        # ---------------------------------------------------------
        # Step 1: Query Understanding
        # ---------------------------------------------------------
        understood_query = self.query_agent.run(query)

        # ---------------------------------------------------------
        # Step 2: Retrieval
        # ---------------------------------------------------------
        retrieved_context = self.retrieval_agent.run(understood_query)

        # ---------------------------------------------------------
        # Step 3: Response Generation
        # ---------------------------------------------------------
        generated_response = self.response_agent.run(
            query=query,
            context=retrieved_context,
        )

        # ---------------------------------------------------------
        # Step 4: Validation
        # ---------------------------------------------------------
        validation_result = self.validation_agent.run(
            query=query,
            response=generated_response,
            context=retrieved_context,
        )

        # ---------------------------------------------------------
        # Step 5: Final Pipeline Output
        # ---------------------------------------------------------
        return {
            "query": query,
            "understood_query": understood_query,
            "retrieved_context": retrieved_context,
            "generated_response": generated_response,
            "validation": validation_result,
            "final_answer": self._get_final_answer(
                generated_response,
                validation_result,
            ),
        }

    @staticmethod
    def _get_final_answer(
        generated_response: Any,
        validation_result: Any,
    ) -> Any:
        """
        Determine the final answer based on validation.

        The exact validation structure can be refined when the
        validation agent is fully integrated.
        """

        if isinstance(validation_result, dict):
            is_valid = validation_result.get("is_valid", True)

            if not is_valid:
                return validation_result.get(
                    "corrected_response",
                    generated_response,
                )

        return generated_response