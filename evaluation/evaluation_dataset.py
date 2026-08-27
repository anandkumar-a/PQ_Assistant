"""
Evaluation dataset utilities for PQ Assistant.

Provides structures and utilities for loading evaluation
questions, ground-truth answers, and relevant documents.
"""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class EvaluationSample:
    """
    Represents one evaluation sample.

    Attributes:
        question:
            User/PQ question used for evaluation.

        ground_truth:
            Expected answer for the question.

        relevant_documents:
            Document IDs that contain relevant information.

        category:
            Optional question category.

        metadata:
            Optional additional information.
    """

    question: str
    ground_truth: str
    relevant_documents: List[str]
    category: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class EvaluationDataset:
    """
    Collection of evaluation samples.

    Provides utilities for loading and accessing
    repeatable PQ Assistant evaluation data.
    """

    def __init__(self, samples: List[EvaluationSample]) -> None:
        """
        Initialize the evaluation dataset.

        Args:
            samples:
                List of evaluation samples.
        """

        self.samples = samples

    @classmethod
    def from_json(
        cls,
        file_path: str,
    ) -> "EvaluationDataset":
        """
        Load an evaluation dataset from a JSON file.

        Args:
            file_path:
                Path to the evaluation JSON file.

        Returns:
            EvaluationDataset instance.

        Raises:
            FileNotFoundError:
                If the dataset file does not exist.

            ValueError:
                If the dataset format is invalid.
        """

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Evaluation dataset not found: {file_path}"
            )

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError(
                "Evaluation dataset must contain a JSON list."
            )

        samples = []

        for index, item in enumerate(data):
            if not isinstance(item, dict):
                raise ValueError(
                    f"Invalid evaluation sample at index {index}."
                )

            required_fields = [
                "question",
                "ground_truth",
                "relevant_documents",
            ]

            for field in required_fields:
                if field not in item:
                    raise ValueError(
                        f"Missing required field '{field}' "
                        f"at sample index {index}."
                    )

            samples.append(
                EvaluationSample(
                    question=item["question"],
                    ground_truth=item["ground_truth"],
                    relevant_documents=item[
                        "relevant_documents"
                    ],
                    category=item.get("category"),
                    metadata=item.get("metadata"),
                )
            )

        return cls(samples)

    def __len__(self) -> int:
        """Return the number of evaluation samples."""

        return len(self.samples)

    def __iter__(self):
        """Iterate over evaluation samples."""

        return iter(self.samples)

    def get_questions(self) -> List[str]:
        """Return all evaluation questions."""

        return [
            sample.question
            for sample in self.samples
        ]

    def get_ground_truths(self) -> List[str]:
        """Return all ground-truth answers."""

        return [
            sample.ground_truth
            for sample in self.samples
        ]

    def get_relevant_documents(self) -> List[List[str]]:
        """Return relevant documents for all samples."""

        return [
            sample.relevant_documents
            for sample in self.samples
        ]

    def get_categories(self) -> List[Optional[str]]:
        """Return categories for all evaluation samples."""

        return [
            sample.category
            for sample in self.samples
        ]

    def to_ragas_format(self) -> List[Dict[str, Any]]:
        """
        Convert the dataset into a format suitable
        for RAGAS evaluation.

        Returns:
            List of dictionaries containing questions
            and ground-truth information.
        """

        return [
            {
                "user_input": sample.question,
                "reference": sample.ground_truth,
                "relevant_documents": sample.relevant_documents,
            }
            for sample in self.samples
        ]