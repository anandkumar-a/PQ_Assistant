# PQ Assistant Usage Guide

## 1. Overview

This document explains how to use the **PQ Assistant** for submitting Product Queries, retrieving enterprise knowledge, reviewing generated responses, and providing feedback.

PQ Assistant is designed to help users quickly find answers from technical documents and historical Product Queries using a multi-agent RAG architecture.

---

## 2. Basic Workflow

The typical user workflow is:

```text
Open PQ Assistant
      │
      ▼
Enter Product Query
      │
      ▼
Submit Query
      │
      ▼
Query Understanding
      │
      ▼
Knowledge Retrieval
      │
      ▼
Response Generation
      │
      ▼
Response Validation
      │
      ▼
View Final Answer
      │
      ▼
Provide Feedback
```

---

## 3. Starting PQ Assistant

Ensure that the project has been configured according to [`setup.md`](setup.md).

Start the application:

```bash
python run.py
```

The local application is expected to run at:

```text
http://localhost:5000
```

---

## 4. Submitting a Product Query

A Product Query should be written as a clear natural-language question.

### Example

```text
What is the recommended troubleshooting procedure for fault code F102?
```

The system processes the query through the following stages:

```text
User Query
    │
    ▼
Query Understanding Agent
    │
    ▼
Retrieval Agent
    │
    ▼
Relevant Documents
    │
    ▼
Response Generation Agent
    │
    ▼
Validation Agent
    │
    ▼
Final Answer
```

---

## 5. Writing Effective Queries

For better retrieval results, provide as much relevant technical information as possible.

### Good Query

```text
What is the troubleshooting procedure for fault code F102 on the X200 controller?
```

This query contains:

* Fault code
* Product information
* Specific task

### Less Specific Query

```text
How do I fix the problem?
```

The second query provides insufficient context and may produce less precise retrieval results.

---

## 6. Query Types

PQ Assistant can be used for different types of Product Queries.

### Troubleshooting

```text
What should I check when fault code F102 appears?
```

### Installation

```text
What are the installation steps for the X200 controller?
```

### Maintenance

```text
What is the recommended maintenance procedure for the X200 system?
```

### Spare Parts

```text
Which replacement part is required for the X200 cooling assembly?
```

### Product Information

```text
What are the operating specifications of the X200 controller?
```

### Historical PQ

```text
Have similar Product Queries been reported for fault code F102?
```

---

## 7. Technical Identifiers

When available, include exact technical identifiers in the query.

Examples include:

* Fault codes
* Part numbers
* Product codes
* Model numbers
* Component names
* Serial-related identifiers where appropriate

Example:

```text
What is the replacement procedure for part number PN-4582?
```

Exact identifiers are particularly useful because the retrieval system combines semantic retrieval with keyword-based BM25 retrieval.

---

## 8. Query Understanding

After submitting a query, the Query Understanding Agent analyzes the request.

It may identify:

```text
Intent:
Troubleshooting

Entities:
Fault Code → F102
Product → X200 Controller

Keywords:
troubleshooting
fault
F102
X200
```

The structured information is then passed to the retrieval stage.

---

## 9. Knowledge Retrieval

The Retrieval Agent searches the available enterprise knowledge.

PQ Assistant uses:

```text
Dense Retrieval
      +
Sparse Retrieval
      │
      ▼
Hybrid Retrieval
      │
      ▼
RRF Ranking
      │
      ▼
Reranking
      │
      ▼
Top-K Context
```

The retrieved context is used by the response-generation agent.

---

## 10. Understanding the Answer

The final response is generated using the retrieved enterprise knowledge.

A typical response may contain:

```text
Answer:
The recommended troubleshooting procedure is to inspect
the specified component and follow the diagnostic sequence
provided in the maintenance documentation.

Source:
Maintenance Manual
Page: 42
```

Where source information is available, users should review the referenced documentation for additional details.

---

## 11. Source-Grounded Responses

PQ Assistant is designed to generate answers based on retrieved enterprise context.

Users should distinguish between:

* Information explicitly supported by retrieved documents
* Reasoning based on the retrieved information
* Information that may require further verification

For safety-critical or operational decisions, users should always verify the answer against the relevant official technical documentation.

---

## 12. Streaming Responses

If Server-Sent Events are enabled, the system can provide progress information while processing a query.

Example:

```text
Understanding query
        │
        ▼
Searching knowledge base
        │
        ▼
Generating response
        │
        ▼
Validating response
        │
        ▼
Final answer
```

This allows the client application to display processing progress instead of waiting for the complete operation.

---

## 13. Providing Feedback

After receiving an answer, users can provide feedback.

Example:

```json
{
    "query_id": 101,
    "rating": 5,
    "feedback": "The answer was accurate and useful."
}
```

A rating can be provided on a scale of:

```text
1 → Very Poor
2 → Poor
3 → Average
4 → Good
5 → Excellent
```

Feedback helps identify areas where the system can be improved.

---

## 14. API Usage

PQ Assistant can also be used directly through its API.

### Submit Query

```http
POST /api/query
```

Request:

```json
{
    "query": "What should I check when fault code F102 occurs?"
}
```

Example response:

```json
{
    "success": true,
    "query": "What should I check when fault code F102 occurs?",
    "answer": "According to the retrieved maintenance documentation, the recommended troubleshooting procedure is...",
    "sources": [
        {
            "document": "maintenance_manual.pdf",
            "page": 42
        }
    ]
}
```

Refer to [`api.md`](api.md) for complete API documentation.

---

## 15. Example End-to-End Query

### User Query

```text
What should I check when fault code F102 occurs on the X200 controller?
```

### Processing

```text
1. Query received
        │
        ▼
2. Intent identified
   → Troubleshooting
        │
        ▼
3. Technical entities extracted
   → F102
   → X200 controller
        │
        ▼
4. Dense retrieval
        │
        ▼
5. BM25 retrieval
        │
        ▼
6. RRF hybrid ranking
        │
        ▼
7. Relevant documents selected
        │
        ▼
8. Response generated
        │
        ▼
9. Response validated
        │
        ▼
10. Final answer returned
```

---

## 16. Handling Unclear Questions

If the query is ambiguous, provide additional context.

Instead of:

```text
Why is it failing?
```

Use:

```text
Why does the X200 controller display fault code F102 during startup?
```

Additional context helps the Query Understanding Agent and retrieval system identify the correct knowledge.

---

## 17. Handling No Relevant Results

If the system cannot find sufficient relevant information, the response should indicate that the available knowledge base does not contain enough information.

Users should then:

1. Verify the Product Query.
2. Add the product/model information.
3. Add relevant fault codes or part numbers.
4. Try alternative terminology.
5. Consult the original technical documentation if necessary.

The system should not be treated as a replacement for authoritative documentation when relevant information cannot be retrieved.

---

## 18. Best Practices

### Use Specific Queries

Include product names, models, fault codes, or part numbers where available.

### Ask One Main Question

Avoid combining many unrelated questions into one query.

### Use Technical Terminology

Use the terminology found in the product documentation.

### Verify Critical Information

For operational or safety-critical decisions, verify the answer against the official documentation.

### Provide Feedback

Submit feedback when an answer is incorrect, incomplete, or particularly useful.

---

## 19. Common Usage Examples

| Use Case            | Example Query                                         |
| ------------------- | ----------------------------------------------------- |
| Troubleshooting     | What should I check for fault code F102?              |
| Installation        | How do I install the X200 controller?                 |
| Maintenance         | What is the maintenance schedule for the X200 system? |
| Spare Parts         | What replacement part is required for PN-4582?        |
| Product Information | What are the specifications of the X200 controller?   |
| Historical PQ       | Are there previous PQs related to fault code F102?    |
| Procedure           | What is the recommended calibration procedure?        |

---

## 20. User Safety and Reliability

PQ Assistant is an AI-assisted knowledge retrieval system.

Generated responses should be treated as assistance rather than an independent authority.

For critical technical operations:

```text
AI Response
    │
    ▼
Review Retrieved Source
    │
    ▼
Verify Official Documentation
    │
    ▼
Perform Authorized Procedure
```

Users should follow their organization's technical, safety, and operational procedures.

---

## 21. Usage Checklist

* [ ] Start the PQ Assistant application.
* [ ] Enter a clear Product Query.
* [ ] Include relevant product/model information.
* [ ] Include fault codes or part numbers when available.
* [ ] Submit the query.
* [ ] Review the generated response.
* [ ] Review available source information.
* [ ] Verify critical technical information.
* [ ] Provide feedback when appropriate.

---

## 22. Related Documentation

* [`README.md`](README.md) — Documentation overview
* [`architecture.md`](architecture.md) — System architecture
* [`api.md`](api.md) — API reference
* [`setup.md`](setup.md) — Installation and configuration
* [`evaluation.md`](evaluation.md) — Evaluation framework
* [`deployment.md`](deployment.md) — Deployment guide
