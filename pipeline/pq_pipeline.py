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
from agents.response_generator.response_agent import ResponseGeneratorAgent
from agents.validation_agent.validation_agent import ValidationAgent


class PQPipeline:
    """
    Orchestrates the complete Product Query Assistant workflow.
    """

    def __init__(
        self,
        query_agent: Optional[QueryUnderstandingAgent] = None,
        retrieval_agent: Optional[RetrievalAgent] = None,
        response_agent: Optional[ResponseGeneratorAgent] = None,
        validation_agent: Optional[ValidationAgent] = None,
    ):
        """
        Initialize the PQ pipeline with the required agents.

        Agents can be injected externally to make the pipeline
        easier to test and maintain. Note: the no-argument defaults
        below produce agents with no retriever/LLM wired in, which
        is only useful for interface/unit testing — the Flask app
        factory (web/app.py) should always inject fully configured
        agents.
        """

        self.query_agent = query_agent or QueryUnderstandingAgent()
        self.retrieval_agent = retrieval_agent or RetrievalAgent()
        self.response_agent = response_agent or ResponseGeneratorAgent()
        self.validation_agent = validation_agent or ValidationAgent()

    def run(
        self,
        query: str,
        top_k: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Execute the complete PQ Assistant workflow.

        Args:
            query: User's product-related question.
            top_k: Number of chunks Agent 2 should retrieve. Falls
                back to RetrievalAgent's own default when omitted.

        Returns:
            Dictionary containing the final answer and pipeline results.
        """

        if not query or not query.strip():
            raise ValueError("Query cannot be empty.")
            return {
            "query": query,
            "understood_query": understood_query,
            "retrieval_result": retrieval_result,
            "generated_response": generated_response,
            "validation": validation_result,
            "final_answer": validation_result.get("final_answer"),
            "answer_chunks": generated_response.get("answer_chunks", []),
            "sources": retrieval_result.get("retrieved_documents", []),
            "is_valid": validation_result.get("is_valid"),
        }
        # ---------------------------------------------------------
        # Step 1: Query Understanding
        # QueryUnderstandingAgent exposes .understand(), not .run().
        # ---------------------------------------------------------
        understood_query = self.query_agent.understand(query)

        # ---------------------------------------------------------
        # Step 2: Retrieval
        # RetrievalAgent exposes .process(), which internally embeds
        # the query and runs hybrid (dense + BM25 + RRF) retrieval.
        # ---------------------------------------------------------
        retrieval_result = self.retrieval_agent.process(
            query_data=understood_query,
            top_k=top_k,
        )

        # ---------------------------------------------------------
        # Step 3: Response Generation
        # ResponseGeneratorAgent.process() expects the query-agent
        # output and the retrieval-agent output as two named dicts.
        # ---------------------------------------------------------
        generated_response = self.response_agent.process(
            query_data=understood_query,
            retrieval_result=retrieval_result,
        )

        # ---------------------------------------------------------
        # Step 4: Validation
        # ValidationAgent.process() expects the response-agent output
        # and the retrieval-agent output as two named dicts.
        # ---------------------------------------------------------
        validation_result = self.validation_agent.process(
            response_data=generated_response,
            retrieval_result=retrieval_result,
        )

        # ---------------------------------------------------------
        # Step 5: Final Pipeline Output
        # Keys match what web/routes.py._normalize_result() already
        # looks for (final_answer, sources/documents, is_valid), so
        # no further translation is needed at the web layer.
        # ---------------------------------------------------------
        return {
            "query": query,
            "understood_query": understood_query,
            "retrieval_result": retrieval_result,
            "generated_response": generated_response,
            "validation": validation_result,
            "final_answer": validation_result.get("final_answer"),
            "sources": retrieval_result.get("retrieved_documents", []),
            "is_valid": validation_result.get("is_valid"),
        }