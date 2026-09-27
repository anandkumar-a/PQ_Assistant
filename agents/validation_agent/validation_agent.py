"""
Validation Agent
----------------

Validates the generated response before returning the
final answer to the user.

The agent performs basic checks for response quality and
retrieval availability, plus the project's core hallucination
guard: a grounding score comparing the generated answer against
its retrieved source chunks using embedding similarity. Answers
scoring below GROUNDING_THRESHOLD are suppressed rather than
shown to the user.
"""

import logging
import re
from typing import Any, Dict, List, Optional

import numpy as np

from config import constants


logger = logging.getLogger(__name__)


class ValidationAgent:
    """
    Agent responsible for validating generated responses.
    """

    def __init__(
        self,
        min_answer_length: int = 10,
        embedding_generator=None,
        grounding_threshold: Optional[float] = None,
    ):
        """
        Initialize the Validation Agent.

        Args:
            min_answer_length:
                Minimum number of characters required
                for a valid response.
            embedding_generator:
                Instance of EmbeddingGenerator, used to embed
                the answer's sentences and the retrieved source
                chunks for grounding-score computation. This
                should be the same shared instance used by the
                Retrieval Agent (see web/app.py) rather than a
                second copy of the model, to keep memory usage
                low on the Render free tier.
            grounding_threshold:
                Minimum grounding score required to approve a
                response. Defaults to
                config.constants.GROUNDING_THRESHOLD (0.70) when
                not given explicitly.
        """

        self.min_answer_length = min_answer_length
        self.embedding_generator = embedding_generator

        self.grounding_threshold = (
            grounding_threshold
            if grounding_threshold is not None
            else constants.GROUNDING_THRESHOLD
        )

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

    @staticmethod
    def _split_into_sentences(text: str) -> List[str]:
        """
        Split an answer into sentences for per-sentence grounding
        checks. Deliberately a lightweight regex splitter rather
        than pulling in spaCy here -- Agent 1 already loads spaCy
        for NER, and loading a second NLP pipeline just to split
        sentences would be wasted memory on the Render free tier.
        """

        sentences = re.split(
            r"(?<=[.!?])\s+",
            text.strip(),
        )

        return [
            sentence.strip()
            for sentence in sentences
            if sentence.strip()
        ]

    @staticmethod
    def _cosine_similarity(
        vector_a: List[float],
        vector_b: List[float],
    ) -> float:
        """
        Cosine similarity between two embedding vectors.
        """

        a = np.array(vector_a)
        b = np.array(vector_b)

        denominator = (
            np.linalg.norm(a) * np.linalg.norm(b)
        )

        if denominator == 0:
            return 0.0

        return float(
            np.dot(a, b) / denominator
        )

    def compute_grounding_score(
        self,
        answer: str,
        retrieved_documents: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Compute how well the generated answer is supported by the
        retrieved source chunks.

        Method: embed each sentence of the answer and each
        retrieved chunk with the same model used for retrieval
        (all-MiniLM-L6-v2), then score each answer sentence by its
        best cosine-similarity match against any retrieved chunk.
        The overall grounding score is the average of those
        per-sentence best-match scores. This is a lightweight,
        RAM-cheap proxy for semantic entailment -- appropriate for
        the 512MB Render limit -- rather than a second, heavier
        cross-encoder/NLI model.

        Args:
            answer:
                The generated answer text.
            retrieved_documents:
                Documents returned by the Retrieval Agent.

        Returns:
            Dictionary with the overall "score" (0.0-1.0),
            per-sentence "sentence_scores", and a human-readable
            "reason".
        """

        if self.embedding_generator is None:
            raise ValueError(
                "EmbeddingGenerator has not been initialized. "
                "It is required to compute the grounding score."
            )

        if not answer or not answer.strip():
            return {
                "score": 0.0,
                "sentence_scores": [],
                "reason": "Answer is empty; nothing to ground.",
            }

        if not retrieved_documents:
            return {
                "score": 0.0,
                "sentence_scores": [],
                "reason": (
                    "No retrieved documents to ground "
                    "the answer against."
                ),
            }

        source_texts = []

        for document in retrieved_documents:

            content = (
                document.get("content")
                or document.get("text")
                or document.get("document")
                or ""
            )

            if content:
                source_texts.append(content)

        if not source_texts:
            return {
                "score": 0.0,
                "sentence_scores": [],
                "reason": (
                    "Retrieved documents had no usable "
                    "text content."
                ),
            }

        source_embeddings = [
            self.embedding_generator.generate_embedding(text)
            for text in source_texts
        ]

        sentences = self._split_into_sentences(answer)

        if not sentences:
            return {
                "score": 0.0,
                "sentence_scores": [],
                "reason": "Answer had no extractable sentences.",
            }

        sentence_scores = []

        for sentence in sentences:

            sentence_embedding = (
                self.embedding_generator.generate_embedding(
                    sentence
                )
            )

            best_match = max(
                self._cosine_similarity(
                    sentence_embedding,
                    source_embedding,
                )
                for source_embedding in source_embeddings
            )

            sentence_scores.append(best_match)

        overall_score = sum(sentence_scores) / len(
            sentence_scores
        )

        return {
            "score": round(overall_score, 4),
            "sentence_scores": [
                round(score, 4) for score in sentence_scores
            ],
            "reason": (
                f"Grounding score computed from {len(sentences)} "
                f"answer sentence(s) against {len(source_texts)} "
                "retrieved chunk(s)."
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

        grounding_result = self.compute_grounding_score(
            answer,
            retrieved_documents,
        )

        grounding_score = grounding_result["score"]

        grounding_passed = (
            grounding_score >= self.grounding_threshold
        )

        is_valid = (
            answer_validation["is_valid"]
            and retrieval_validation["is_valid"]
            and grounding_passed
        )

        validation_result = {
            "is_valid": is_valid,
            "answer_validation": answer_validation,
            "retrieval_validation": retrieval_validation,
            "grounding_score": grounding_score,
            "grounding_threshold": self.grounding_threshold,
            "grounding_details": grounding_result,
        }

        if is_valid:
            validation_result["status"] = "approved"
            validation_result["final_answer"] = answer

            logger.info(
                "Response validation approved "
                "(grounding=%.2f, threshold=%.2f).",
                grounding_score,
                self.grounding_threshold,
            )

        else:
            validation_result["status"] = "rejected"

            if (
                answer_validation["is_valid"]
                and retrieval_validation["is_valid"]
                and not grounding_passed
            ):
                # Failed specifically on grounding: this is Agent
                # 4's headline hallucination-suppression behavior,
                # using the exact message the project spec requires.
                validation_result["final_answer"] = (
                    "Insufficient evidence found"
                )
            else:
                validation_result["final_answer"] = (
                    "I could not find enough reliable information "
                    "in the available knowledge base to provide "
                    "a confident answer."
                )

            logger.warning(
                "Response validation rejected "
                "(grounding=%.2f, threshold=%.2f): %s",
                grounding_score,
                self.grounding_threshold,
                validation_result["status"],
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