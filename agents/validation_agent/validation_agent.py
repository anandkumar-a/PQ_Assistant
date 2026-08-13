"""
Validation Agent
----------------

Validates the generated response before returning the
final answer to the user.

The agent performs basic checks for response quality,
retrieval availability, and possible unsupported answers.
"""

import logging
from typing import Any, Dict, List


logger = logging.getLogger(__name__)


class ValidationAgent:
    """
    Agent responsible for validating generated responses.
    """

    def __init__(
        self,
        min_answer_length: int = 10,
    ):
        """
        Initialize the Validation Agent.

        Args:
            min_answer_length:
                Minimum number of characters required
                for a valid response.
        """

        self.min_answer_length = min_answer_length

    def validate_answer(
        self,
        answer: str,
    ) -> Dict[str, Any]:
        """
        Validate whether the generated answer is usable.

        Args:
            answer:
                Generated response from ResponseGeneratorAgent.

        Returns:
            Validation result.
        """

        if not answer:
            return {
                "is_valid": False,
                "reason": "Generated answer is empty.",
            }

        if len(answer.strip()) < self.min_answer_length:
            return {
                "is_valid": False,
                "reason": (
                    "Generated answer is too short."
                ),
            }

        return {
            "is_valid": True,
            "reason": "Answer passed basic validation.",
        }

    def validate_retrieval(
        self,
        retrieved_documents: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Validate whether relevant documents were retrieved.

        Args:
            retrieved_documents:
                Documents returned by the Retrieval Agent.

        Returns:
            Retrieval validation result.
        """

        if not retrieved_documents:
            return {
                "is_valid": False,
                "reason": (
                    "No relevant documents were retrieved."
                ),
            }

        return {
            "is_valid": True,
            "reason": (
                f"{len(retrieved_documents)} document(s) "
                "available for validation."
            ),
        }

    def validate_response(
        self,
        response_data: Dict[str, Any],
        retrieval_result: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Perform complete response validation.

        Args:
            response_data:
                Output from ResponseGeneratorAgent.
            retrieval_result:
                Output from RetrievalAgent.

        Returns:
            Complete validation result.
        """

        answer = response_data.get(
            "answer",
            "",
        )

        retrieved_documents = retrieval_result.get(
            "retrieved_documents",
            [],
        )

        answer_validation = self.validate_answer(
            answer
        )

        retrieval_validation = self.validate_retrieval(
            retrieved_documents
        )

        is_valid = (
            answer_validation["is_valid"]
            and retrieval_validation["is_valid"]
        )

        validation_result = {
            "is_valid": is_valid,
            "answer_validation": answer_validation,
            "retrieval_validation": retrieval_validation,
        }

        if is_valid:
            validation_result["status"] = "approved"
            validation_result["final_answer"] = answer

            logger.info(
                "Response validation approved."
            )

        else:
            validation_result["status"] = "rejected"

            validation_result["final_answer"] = (
                "I could not find enough reliable information "
                "in the available knowledge base to provide "
                "a confident answer."
            )

            logger.warning(
                "Response validation rejected: %s",
                validation_result,
            )

        return validation_result

    def process(
        self,
        response_data: Dict[str, Any],
        retrieval_result: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Execute the complete validation process.

        Args:
            response_data:
                Output from ResponseGeneratorAgent.
            retrieval_result:
                Output from RetrievalAgent.

        Returns:
            Final validated response.
        """

        try:
            return self.validate_response(
                response_data=response_data,
                retrieval_result=retrieval_result,
            )

        except Exception as error:

            logger.exception(
                "Validation process failed."
            )

            raise RuntimeError(
                f"Validation failed: {str(error)}"
            ) from error