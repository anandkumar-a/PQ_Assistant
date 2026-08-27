"""
Evaluation report generator for PQ Assistant.

Provides utilities for converting evaluation results into
structured reports suitable for analysis and research reporting.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


class EvaluationReportGenerator:
    """
    Generate structured evaluation reports for PQ Assistant.
    """

    def __init__(self, project_name: str = "PQ Assistant") -> None:
        """
        Initialize the report generator.

        Args:
            project_name:
                Name of the system being evaluated.
        """

        self.project_name = project_name

    def generate(
        self,
        evaluation_results: Dict[str, Any],
        dataset_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Generate a structured evaluation report.

        Args:
            evaluation_results:
                Evaluation metrics and results.

            dataset_size:
                Number of evaluation questions.

        Returns:
            Structured evaluation report.
        """

        report = {
            "project": self.project_name,
            "generated_at": datetime.now().isoformat(),
            "dataset_size": dataset_size,
            "results": evaluation_results,
        }

        return report

    def save_json(
        self,
        report: Dict[str, Any],
        output_path: str,
    ) -> str:
        """
        Save the evaluation report as a JSON file.

        Args:
            report:
                Evaluation report dictionary.

            output_path:
                Destination path for the JSON report.

        Returns:
            Path to the generated report.
        """

        path = Path(output_path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                report,
                file,
                indent=4,
                ensure_ascii=False,
            )

        return str(path)

    def generate_summary(
        self,
        evaluation_results: Dict[str, Any],
    ) -> str:
        """
        Generate a human-readable evaluation summary.

        Args:
            evaluation_results:
                Evaluation results.

        Returns:
            Formatted text summary.
        """

        lines = [
            "=" * 60,
            f"{self.project_name.upper()}",
            "RAG EVALUATION REPORT",
            "=" * 60,
            "",
        ]

        retrieval_metrics = evaluation_results.get(
            "retrieval_metrics",
            {},
        )

        if retrieval_metrics:
            lines.extend(
                [
                    "RETRIEVAL PERFORMANCE",
                    "-" * 30,
                    self._format_metric(
                        "Precision@K",
                        retrieval_metrics.get("precision_at_k"),
                    ),
                    self._format_metric(
                        "Recall@K",
                        retrieval_metrics.get("recall_at_k"),
                    ),
                    self._format_metric(
                        "Reciprocal Rank",
                        retrieval_metrics.get("reciprocal_rank"),
                    ),
                    self._format_metric(
                        "Hit@K",
                        retrieval_metrics.get("hit_at_k"),
                    ),
                    "",
                ]
            )

        ragas_metrics = evaluation_results.get(
            "ragas",
            {},
        )

        if ragas_metrics:
            lines.extend(
                [
                    "RAG QUALITY",
                    "-" * 30,
                ]
            )

            summary = ragas_metrics.get(
                "summary",
                {},
            )

            for metric_name, score in summary.items():
                lines.append(
                    self._format_metric(
                        metric_name,
                        score,
                    )
                )

            lines.append("")

        lines.extend(
            [
                "=" * 60,
                "END OF REPORT",
                "=" * 60,
            ]
        )

        return "\n".join(lines)

    def save_summary(
        self,
        summary: str,
        output_path: str,
    ) -> str:
        """
        Save a human-readable summary to a text file.

        Args:
            summary:
                Formatted evaluation summary.

            output_path:
                Destination path.

        Returns:
            Path to the generated summary.
        """

        path = Path(output_path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with path.open(
            "w",
            encoding="utf-8",
        ) as file:
            file.write(summary)

        return str(path)

    @staticmethod
    def _format_metric(
        name: str,
        value: Any,
    ) -> str:
        """
        Format a metric for human-readable output.

        Args:
            name:
                Metric name.

            value:
                Metric value.

        Returns:
            Formatted metric string.
        """

        if value is None:
            return f"{name:<25} N/A"

        if isinstance(value, float):
            return f"{name:<25} {value:.4f}"

        return f"{name:<25} {value}"