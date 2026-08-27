"""
RAGAS-based evaluation for PQ Assistant.

Provides evaluation of RAG response quality using:
- Faithfulness
- Answer Relevancy
- Context Precision
- Context Recall
"""

from typing import Any, Dict, List, Optional

from ragas import EvaluationDataset, evaluate
from ragas.metrics import (
    AnswerRelevancy,
    ContextPrecision,
    ContextRecall,
    Faithfulness,
)


class RagasEvaluator:
    """
    Evaluate PQ Assistant responses using RAGAS.

    The evaluator expects:
        - User questions
        - Generated answers
        - Retrieved contexts
        - Ground-truth answers
    """

    def __init__(
        self,
        llm: Optional[Any] = None,
        embeddings: Optional[Any] = None,
    ) -> None:
        """
        Initialize the RAGAS evaluator.

        Args:
            llm:
                LLM used by RAGAS for evaluation.

            embeddings:
                Embedding model used by RAGAS for evaluation.
        """

        self.llm = llm
        self.embeddings = embeddings

        self.metrics = [
            Faithfulness(),
            AnswerRelevancy(),
            ContextPrecision(),
            ContextRecall(),
        ]

    def build_dataset(
        self,
        questions: List[str],
        answers: List[str],
        contexts: List[List[str]],
        ground_truths: List[str],
    ) -> EvaluationDataset:
        """
        Build a RAGAS evaluation dataset.

        Args:
            questions:
                User questions.

            answers:
                Generated answers.

            contexts:
                Retrieved document contexts for each question.

            ground_truths:
                Expected answers.

        Returns:
            RAGAS EvaluationDataset.
        """

        if not (
            len(questions)
            == len(answers)
            == len(contexts)
            == len(ground_truths)
        ):
            raise ValueError(
                "questions, answers, contexts, and ground_truths "
                "must contain the same number of items."
            )

        dataset = []

        for question, answer, context, ground_truth in zip(
            questions,
            answers,
            contexts,
            ground_truths,
        ):
            dataset.append(
                {
                    "user_input": question,
                    "response": answer,
                    "retrieved_contexts": context,
                    "reference": ground_truth,
                }
            )

        return EvaluationDataset.from_list(dataset)

    def evaluate(
        self,
        questions: List[str],
        answers: List[str],
        contexts: List[List[str]],
        ground_truths: List[str],
    ) -> Dict[str, Any]:
        """
        Run RAGAS evaluation.

        Args:
            questions:
                User questions.

            answers:
                Generated answers from PQ Assistant.

            contexts:
                Retrieved contexts used for answer generation.

            ground_truths:
                Expected answers.

        Returns:
            Dictionary containing RAGAS evaluation results.
        """

        dataset = self.build_dataset(
            questions=questions,
            answers=answers,
            contexts=contexts,
            ground_truths=ground_truths,
        )

        result = evaluate(
            dataset=dataset,
            metrics=self.metrics,
            llm=self.llm,
            embeddings=self.embeddings,
        )

        return self._format_result(result)

    @staticmethod
    def _format_result(result: Any) -> Dict[str, Any]:
        """
        Convert the RAGAS result into a serializable dictionary.

        Args:
            result:
                RAGAS evaluation result.

        Returns:
            Dictionary containing evaluation scores.
        """

        if hasattr(result, "to_pandas"):
            dataframe = result.to_pandas()

            return {
                "scores": dataframe.to_dict(orient="records"),
                "summary": {
                    column: float(dataframe[column].mean())
                    for column in dataframe.columns
                    if column not in {
                        "user_input",
                        "response",
                        "retrieved_contexts",
                        "reference",
                    }
                    and dataframe[column].dtype.kind in "fi"
                },
            }

        if hasattr(result, "to_dict"):
            return result.to_dict()

        return {
            "result": result,
        }