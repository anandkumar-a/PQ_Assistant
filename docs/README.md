# PQ Assistant Documentation

## Agentic AI-Based Product Query Assistant using Multi-Agent RAG

PQ Assistant is an intelligent enterprise knowledge retrieval system designed to answer Product Queries (PQs) using **Retrieval-Augmented Generation (RAG)** and a **multi-agent architecture**.

The system retrieves relevant information from enterprise documents and historical Product Queries, generates context-aware responses, validates the generated answer, and stores feedback for continuous evaluation and improvement.

---

## 1. Project Overview

PQ Assistant is designed for manufacturing and industrial enterprise environments where users need quick and reliable answers from large collections of technical and historical documents.

The system can work with knowledge sources such as:

* Product Manuals
* Installation Guides
* Maintenance Manuals
* Fault Code Documents
* Historical Product Queries
* Service Bulletins
* Spare Parts Catalogues
* Technical Documentation

The primary goal is to reduce the time required to find relevant technical information while maintaining answer consistency, traceability, and reliability.

---

## 2. Key Features

* Natural-language Product Query understanding
* Semantic document retrieval
* Sparse keyword-based retrieval
* Hybrid retrieval using Reciprocal Rank Fusion
* Named Entity Recognition for technical entities
* Historical PQ retrieval
* Multi-agent query processing
* Retrieval-Augmented Generation
* Response validation
* Feedback collection
* Evaluation using RAGAS
* Retrieval and response analytics
* REST API support
* Server-Sent Events (SSE) support
* SQLite-based application data storage
* ChromaDB vector storage
* Docker-based deployment

---

## 3. System Architecture

The PQ Assistant follows a multi-stage processing pipeline:

```text
User Query
    │
    ▼
Query Understanding Agent
    │
    ▼
Retrieval Agent
    │
    ├── Dense Retrieval
    │
    ├── Sparse Retrieval
    │
    └── Hybrid Retrieval
    │
    ▼
Relevant Documents / Historical PQs
    │
    ▼
Response Generation Agent
    │
    ▼
Validation Agent
    │
    ▼
Final Answer
    │
    ├── Feedback
    │
    ├── Evaluation
    │
    └── Analytics
```

Detailed architecture documentation is available in [`architecture.md`](architecture.md).

---

## 4. Technology Stack

| Component              | Technology                               |
| ---------------------- | ---------------------------------------- |
| Programming Language   | Python 3.11                              |
| Backend                | Flask                                    |
| LLM                    | Google Gemini 1.5 Flash                  |
| Embedding Model        | `sentence-transformers/all-MiniLM-L6-v2` |
| Vector Database        | ChromaDB                                 |
| Sparse Retrieval       | BM25                                     |
| Hybrid Retrieval       | Reciprocal Rank Fusion (RRF)             |
| NLP / NER              | spaCy                                    |
| Orchestration          | LangChain LCEL                           |
| Database               | SQLite                                   |
| Evaluation             | RAGAS                                    |
| Frontend Communication | REST API / SSE                           |
| Deployment             | Docker / Render                          |

---

## 5. Project Modules

The project is organized into modular components:

```text
pq_assistant/
│
├── agents/
├── analytics/
├── config/
├── data/
├── database/
├── docs/
├── embedding/
├── evaluation/
├── ingestion/
├── pipeline/
├── prompts/
├── repositories/
├── retrieval/
├── services/
├── test/
├── texts/
├── utils/
├── web/
│
├── Dockerfile
├── requirements.txt
└── run.py
```

### Core Modules

**Agents**
Contains the intelligent agents responsible for query understanding, retrieval, response generation, and validation.

**Ingestion**
Handles loading, processing, chunking, and preparing enterprise documents for retrieval.

**Embedding**
Generates vector representations and manages vector storage.

**Retrieval**
Provides dense, sparse, hybrid, and reranking-based retrieval capabilities.

**Database**
Manages application persistence using SQLite and vector-related database components.

**Repositories**
Provides data-access abstractions for documents and queries.

**Services**
Contains business logic used by the application.

**Pipeline**
Coordinates the complete query-processing workflow.

**Analytics**
Tracks query, retrieval, response, feedback, and system performance metrics.

**Evaluation**
Provides repeatable evaluation of PQ Assistant responses using predefined datasets and evaluation metrics.

---

## 6. Documentation Guide

| Documentation                   | Description                                              |
| ------------------------------- | -------------------------------------------------------- |
| [Architecture](architecture.md) | System architecture, agents, RAG pipeline, and data flow |
| [API](api.md)                   | REST API endpoints and request/response formats          |
| [Setup](setup.md)               | Local installation and environment configuration         |
| [Usage](usage.md)               | Instructions for using the PQ Assistant                  |
| [Evaluation](evaluation.md)     | Evaluation datasets, metrics, and RAGAS                  |
| [Deployment](deployment.md)     | Docker and production deployment instructions            |

---

## 7. Query Processing Flow

A typical Product Query follows these stages:

### Step 1 — Query Understanding

The Query Understanding Agent analyzes the user's question and identifies important information such as:

* Query intent
* Product information
* Fault codes
* Part numbers
* Technical entities
* Relevant keywords

### Step 2 — Retrieval

The Retrieval Agent searches the enterprise knowledge base using multiple retrieval strategies.

Dense retrieval provides semantic matching, while BM25 provides keyword-based matching.

The results are combined using **Reciprocal Rank Fusion (RRF)**.

### Step 3 — Response Generation

The Response Generation Agent receives the retrieved context and generates a response grounded in the available enterprise knowledge.

### Step 4 — Validation

The Validation Agent checks the generated response for relevance, consistency, and grounding against the retrieved information.

### Step 5 — Final Response

The validated response is returned to the user.

Query and feedback information can subsequently be used for evaluation and analytics.

---

## 8. Evaluation

The evaluation module supports repeatable testing using predefined Product Query datasets.

Evaluation can measure areas such as:

* Answer correctness
* Context relevance
* Faithfulness
* Retrieval quality
* Response quality
* Overall system performance

RAGAS is used as part of the evaluation framework.

See [`evaluation.md`](evaluation.md) for details.

---

## 9. Analytics

The analytics module provides monitoring capabilities across different stages of the system.

Current analytics components include:

* Query Analytics
* Retrieval Analytics
* Response Analytics
* Feedback Analytics
* Performance Analytics
* Analytics Manager

These components help identify retrieval problems, response-quality issues, user feedback trends, and system performance bottlenecks.

---

## 10. Development

For local development, configure the required environment variables and install the project's dependencies before starting the Flask application.

Detailed instructions are provided in [`setup.md`](setup.md).

---

## 11. Deployment

PQ Assistant is designed to support containerized deployment using Docker.

The intended deployment workflow is:

```text
Source Code
     │
     ▼
Docker Image
     │
     ▼
Container
     │
     ▼
Production Environment
```

See [`deployment.md`](deployment.md) for deployment configuration and instructions.

---

## 12. Project Objectives

The major objectives of PQ Assistant are to:

1. Reduce Product Query response time.
2. Improve consistency of technical responses.
3. Retrieve relevant enterprise knowledge efficiently.
4. Preserve historical PQ knowledge.
5. Combine semantic and keyword-based retrieval.
6. Use agents for intelligent query processing and validation.
7. Provide explainable and grounded responses.
8. Evaluate system performance systematically.
9. Capture user feedback for continuous improvement.
10. Provide analytics for monitoring and optimization.

---

## 13. Future Improvements

Potential future enhancements include:

* Advanced reranking models
* Improved entity extraction
* Conversational memory
* Source citation and document traceability
* Human-in-the-loop validation
* Advanced agent planning
* Automated evaluation pipelines
* Continuous retrieval optimization
* Production monitoring dashboards
* Role-based enterprise access control

---

## 14. License

This project is developed as an academic and research-oriented project.

Refer to the repository license for the applicable usage and distribution terms.
