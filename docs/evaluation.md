# PQ Assistant Evaluation Guide

## 1. Overview

The PQ Assistant evaluation framework measures the quality, reliability, and performance of the **Agentic AI-Based Product Query Assistant using Multi-Agent RAG**.

The evaluation system provides repeatable testing using predefined Product Query questions, expected answers, and relevant documents.

The evaluation module is designed to measure both:

* Retrieval quality
* Generated response quality

The framework uses **RAGAS** along with project-specific evaluation metrics.

---

## 2. Evaluation Objectives

The main objectives are to:

1. Measure the accuracy of generated answers.
2. Evaluate the relevance of retrieved documents.
3. Measure the faithfulness of responses to retrieved context.
4. Identify retrieval failures.
5. Identify response-generation failures.
6. Compare system performance across experiments.
7. Provide repeatable evaluation results.
8. Track system improvements over time.

---

## 3. Evaluation Architecture

```text
                    Evaluation Dataset
                           │
                           ▼
                    Evaluation Runner
                           │
                           ▼
                     PQ Assistant
                           │
                 ┌─────────┴─────────┐
                 │                   │
                 ▼                   ▼
            Retrieval            Generation
                 │                   │
                 └─────────┬─────────┘
                           ▼
                    Evaluation Metrics
                           │
                           ▼
                    RAGAS Evaluation
                           │
                           ▼
                    Evaluation Results
                           │
                           ▼
                    Report Generation
```

---

## 4. Evaluation Dataset

The evaluation dataset contains predefined Product Query test cases.

The dataset is maintained under:

```text
evaluation/
└── datasets/
    └── evaluation_questions.json
```

Each test case should contain enough information to evaluate the system consistently.

A conceptual example is:

```json
{
    "id": "PQ001",
    "question": "What should I check for fault code F102?",
    "expected_answer": "The recommended troubleshooting procedure is...",
    "relevant_documents": [
        "maintenance_manual.pdf"
    ]
}
```

---

## 5. Evaluation Dataset Components

A typical evaluation record contains:

| Field                | Description                                |
| -------------------- | ------------------------------------------ |
| `id`                 | Unique evaluation case identifier          |
| `question`           | Product Query submitted to the system      |
| `expected_answer`    | Reference or expected answer               |
| `relevant_documents` | Documents considered relevant              |
| `metadata`           | Optional additional evaluation information |

The dataset should remain stable between evaluation runs when comparing different system versions.

---

## 6. Evaluation Process

Each evaluation case follows the same processing pipeline used by the application.

```text
Evaluation Question
        │
        ▼
Query Understanding
        │
        ▼
Dense Retrieval
        │
        ▼
Sparse Retrieval
        │
        ▼
Hybrid RRF Retrieval
        │
        ▼
Reranking
        │
        ▼
Response Generation
        │
        ▼
Validation
        │
        ▼
Generated Answer
        │
        ▼
Evaluation
```

This ensures that evaluation reflects the actual system behavior.

---

## 7. Evaluation Metrics

The evaluation framework can measure multiple dimensions of system quality.

### 7.1 Faithfulness

Faithfulness measures whether the generated response is supported by the retrieved context.

A highly faithful response should avoid introducing unsupported facts.

Conceptually:

```text
Retrieved Context
       │
       ▼
Generated Answer
       │
       ▼
Are claims supported?
       │
       ▼
Faithfulness Score
```

A higher score indicates better grounding in the retrieved information.

---

### 7.2 Answer Relevancy

Answer relevancy measures how well the generated response addresses the user's question.

A relevant response should:

* Directly address the question
* Avoid unnecessary information
* Remain focused on the requested topic

---

### 7.3 Context Relevancy

Context relevancy evaluates whether the retrieved context is useful for answering the query.

Poor retrieval may result in:

```text
Query
  │
  ▼
Irrelevant Documents
  │
  ▼
Poor Context
  │
  ▼
Poor Answer
```

Good retrieval should provide context directly related to the Product Query.

---

### 7.4 Context Precision

Context precision evaluates whether relevant retrieved information is ranked ahead of irrelevant information.

This is particularly important for the hybrid retrieval system.

---

### 7.5 Context Recall

Context recall measures whether the retrieval system successfully retrieves the information required to answer the query.

High context recall means the required evidence is generally present among the retrieved results.

---

### 7.6 Answer Correctness

Answer correctness compares the generated answer with the expected/reference answer.

It helps determine whether the response actually provides the information required by the evaluation case.

---

## 8. Retrieval Evaluation

Retrieval quality is evaluated independently from response generation where possible.

The retrieval evaluation process is:

```text
Query
  │
  ▼
Retrieved Documents
  │
  ▼
Compare with Relevant Documents
  │
  ▼
Retrieval Metrics
```

Important retrieval metrics include:

* Precision
* Recall
* Precision@K
* Recall@K
* Mean Reciprocal Rank (MRR)
* Hit Rate
* Context Precision
* Context Recall

---

## 9. Precision@K

Precision@K measures how many of the top K retrieved documents are relevant.

Conceptually:

```text
Precision@K =
Relevant Documents in Top K
────────────────────────────
          K
```

For example, if 3 of the top 5 retrieved documents are relevant:

```text
Precision@5 = 3 / 5 = 0.60
```

---

## 10. Recall@K

Recall@K measures how many of the relevant documents were successfully retrieved within the top K results.

Conceptually:

```text
Recall@K =
Relevant Documents Retrieved
─────────────────────────────
Total Relevant Documents
```

Higher recall indicates that the retrieval system is finding more of the required evidence.

---

## 11. Mean Reciprocal Rank

MRR measures how highly the first relevant result appears in the ranking.

Conceptually:

```text
MRR = Average(1 / Rank of First Relevant Result)
```

If the first relevant document is ranked first:

```text
Reciprocal Rank = 1.0
```

If it is ranked fifth:

```text
Reciprocal Rank = 0.2
```

MRR is useful for evaluating Product Queries where the most relevant document should appear near the top.

---

## 12. RAGAS Evaluation

The evaluation framework integrates RAGAS for RAG-specific evaluation.

RAGAS can be used to evaluate dimensions such as:

* Faithfulness
* Answer relevancy
* Context precision
* Context recall

The RAGAS evaluator is implemented through:

```text
evaluation/ragas_evaluator.py
```

The exact metrics used should match the installed RAGAS version and project configuration.

---

## 13. Evaluation Components

The evaluation module contains:

```text
evaluation/
├── __init__.py
├── metrics.py
├── evaluator.py
├── ragas_evaluator.py
├── report_generator.py
│
├── datasets/
│   ├── __init__.py
│   └── evaluation_questions.json
│
└── results/
    └── .gitkeep
```

### `metrics.py`

Contains project-specific evaluation metric calculations.

### `evaluator.py`

Coordinates the evaluation process.

### `ragas_evaluator.py`

Handles RAGAS-based evaluation.

### `report_generator.py`

Generates structured evaluation reports.

### `evaluation_questions.json`

Stores repeatable evaluation cases.

### `results/`

Stores generated evaluation results.

---

## 14. Running an Evaluation

The evaluation should be executed using the project's evaluation entry point.

A typical workflow is:

```text
Load Dataset
     │
     ▼
Run Evaluation Cases
     │
     ▼
Collect Answers
     │
     ▼
Collect Retrieved Context
     │
     ▼
Calculate Metrics
     │
     ▼
Run RAGAS Evaluation
     │
     ▼
Generate Report
     │
     ▼
Save Results
```

The exact command depends on the project's implemented evaluation runner.

---

## 15. Evaluation Result Structure

A result can conceptually contain:

```json
{
    "question_id": "PQ001",
    "question": "What should I check for fault code F102?",
    "generated_answer": "The recommended procedure is...",
    "retrieved_documents": [
        "maintenance_manual.pdf"
    ],
    "metrics": {
        "faithfulness": 0.92,
        "answer_relevancy": 0.89,
        "context_precision": 0.90,
        "context_recall": 0.88
    }
}
```

The actual result structure should follow the implementation in the evaluation module.

---

## 16. Evaluation Reports

Evaluation reports summarize the performance of the system across the evaluation dataset.

A report can contain:

* Evaluation timestamp
* Number of test cases
* Successful cases
* Failed cases
* Average metric scores
* Per-question results
* Retrieval performance
* Response performance
* RAGAS scores

Example summary:

```text
Evaluation Summary
------------------
Total Questions: 100
Successful:      96
Failed:           4

Faithfulness:       0.91
Answer Relevancy:   0.89
Context Precision:  0.87
Context Recall:     0.90
```

These values are examples only and should not be interpreted as actual project results.

---

## 17. Failure Analysis

Evaluation should not focus only on average scores.

Individual failed cases should be inspected.

A typical failure-analysis process is:

```text
Failed Query
     │
     ▼
Inspect Retrieval
     │
     ├── Wrong documents?
     │
     ├── Missing documents?
     │
     └── Correct documents?
            │
            ▼
       Inspect Answer
            │
            ├── Unsupported claim?
            ├── Incomplete answer?
            ├── Incorrect answer?
            └── Correct answer?
```

This helps determine whether improvements should be made to retrieval, generation, or validation.

---

## 18. Retrieval Failure Categories

Common retrieval failures include:

### Missing Relevant Document

The correct document was not retrieved.

### Poor Ranking

The correct document was retrieved but ranked too low.

### Keyword Mismatch

BM25 fails because the query and document use different terminology.

### Semantic Mismatch

Dense retrieval fails to identify the correct semantic relationship.

### Metadata Problem

Incorrect or incomplete document metadata affects retrieval.

---

## 19. Response Failure Categories

Common response failures include:

* Incorrect answer
* Incomplete answer
* Unsupported claim
* Irrelevant information
* Hallucination
* Poor technical explanation
* Incorrect interpretation of retrieved context

These failures should be recorded and analyzed during system improvement.

---

## 20. Evaluation and Validation

Evaluation and response validation serve different purposes.

### Validation

Validation happens during normal query processing:

```text
Query
  │
  ▼
Generate Answer
  │
  ▼
Validate Answer
  │
  ▼
Return Response
```

### Evaluation

Evaluation happens periodically to measure overall system quality:

```text
Evaluation Dataset
       │
       ▼
Run System
       │
       ▼
Measure Performance
       │
       ▼
Generate Evaluation Report
```

Validation protects individual responses, while evaluation measures the overall system.

---

## 21. Evaluation Baselines

A baseline should be established before major system improvements.

Possible baselines include:

```text
Baseline 1:
Dense Retrieval + LLM

Baseline 2:
BM25 + LLM

Baseline 3:
Hybrid Retrieval + LLM

Baseline 4:
Hybrid Retrieval + Reranking + LLM
```

The results can then be compared to determine which architecture provides the best performance.

---

## 22. Experiment Tracking

Each evaluation run should ideally record:

* Model version
* Embedding model
* Retrieval configuration
* Top-K value
* Reranker configuration
* LLM configuration
* Evaluation dataset version
* Evaluation timestamp
* Metric results

This makes experiments reproducible.

---

## 23. Recommended Evaluation Strategy

A practical evaluation strategy is:

```text
Step 1
Create Evaluation Dataset
        │
        ▼
Step 2
Establish Baseline
        │
        ▼
Step 3
Evaluate Retrieval
        │
        ▼
Step 4
Evaluate Generated Answers
        │
        ▼
Step 5
Run RAGAS
        │
        ▼
Step 6
Analyze Failures
        │
        ▼
Step 7
Improve System
        │
        ▼
Step 8
Run Evaluation Again
        │
        ▼
Step 9
Compare Results
```

---

## 24. Evaluation Checklist

* [ ] Evaluation dataset is versioned.
* [ ] Questions are representative of real Product Queries.
* [ ] Expected answers are reviewed.
* [ ] Relevant documents are identified.
* [ ] Retrieval metrics are calculated.
* [ ] Response metrics are calculated.
* [ ] RAGAS evaluation is executed.
* [ ] Failed cases are analyzed.
* [ ] Evaluation results are stored.
* [ ] Results are compared across system versions.

---

## 25. Continuous Improvement

Evaluation results should feed back into system development.

```text
Evaluation
    │
    ▼
Identify Weakness
    │
    ▼
Improve Component
    │
    ├── Query Understanding
    ├── Retrieval
    ├── Reranking
    ├── Prompting
    ├── Generation
    └── Validation
    │
    ▼
Run Evaluation Again
    │
    ▼
Compare Results
```

This creates a continuous improvement cycle for PQ Assistant.

---

## 26. Important Considerations

Evaluation scores should not be treated as the only measure of system quality.

A strong evaluation should combine:

* Automated metrics
* RAGAS evaluation
* Retrieval metrics
* Human review
* Failure analysis
* User feedback
* Production analytics

This combination provides a more complete understanding of PQ Assistant performance.

---

## 27. Related Documentation

* [`README.md`](README.md) — Documentation overview
* [`architecture.md`](architecture.md) — System architecture
* [`api.md`](api.md) — API reference
* [`setup.md`](setup.md) — Installation and configuration
* [`usage.md`](usage.md) — Usage instructions
* [`deployment.md`](deployment.md) — Deployment guide
s