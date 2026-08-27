# PQ Assistant Architecture

## 1. Overview

PQ Assistant is an **Agentic AI-Based Product Query Assistant using Multi-Agent Retrieval-Augmented Generation (RAG)**.

The architecture combines:

* Multi-agent orchestration
* Dense semantic retrieval
* Sparse keyword retrieval
* Hybrid retrieval
* Reciprocal Rank Fusion (RRF)
* Named Entity Recognition (NER)
* Large Language Model-based response generation
* Response validation
* Evaluation
* Feedback collection
* Analytics

The architecture is designed for enterprise environments where Product Queries (PQs) must be answered using reliable and relevant technical knowledge.

---

## 2. High-Level Architecture

```text
                         ┌─────────────────────┐
                         │       User          │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Flask Web/API     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Query Pipeline    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                    ┌──────────────────────────────┐
                    │ Query Understanding Agent    │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │       Retrieval Agent        │
                    └──────────────┬───────────────┘
                                   │
                 ┌─────────────────┼─────────────────┐
                 │                 │                 │
                 ▼                 ▼                 ▼
        ┌────────────────┐ ┌───────────────┐ ┌───────────────┐
        │ Dense Retrieval│ │ BM25 Retrieval│ │    Reranker   │
        └───────┬────────┘ └───────┬───────┘ └───────┬───────┘
                │                  │                 │
                └──────────────────┼─────────────────┘
                                   ▼
                        ┌─────────────────────┐
                        │   Hybrid Retrieval  │
                        │       (RRF)         │
                        └──────────┬──────────┘
                                   │
                                   ▼
                        ┌─────────────────────┐
                        │ Retrieved Context   │
                        └──────────┬──────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │ Response Generation Agent    │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │      Validation Agent        │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                         ┌─────────────────────┐
                         │    Final Answer     │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┼────────────────┐
                    ▼               ▼                ▼
             ┌───────────┐  ┌──────────────┐  ┌─────────────┐
             │  Feedback │  │  Evaluation  │  │  Analytics  │
             └───────────┘  └──────────────┘  └─────────────┘
```

---

## 3. Architectural Layers

PQ Assistant is organized into logical layers.

```text
┌───────────────────────────────────────────┐
│              Presentation Layer           │
│              Flask / REST / SSE           │
├───────────────────────────────────────────┤
│              Application Layer             │
│             Services / Pipeline            │
├───────────────────────────────────────────┤
│                Agent Layer                 │
│ Query / Retrieval / Response / Validation │
├───────────────────────────────────────────┤
│              Retrieval Layer               │
│ Dense / Sparse / Hybrid / Reranking       │
├───────────────────────────────────────────┤
│             Knowledge Layer                │
│ Documents / PQs / Embeddings / ChromaDB   │
├───────────────────────────────────────────┤
│               Data Layer                   │
│              SQLite / Files                │
└───────────────────────────────────────────┘
```

---

## 4. User Interaction Layer

The user interacts with PQ Assistant through the web application or API.

The frontend sends a Product Query to the Flask backend.

Example:

```text
User:
"What is the recommended procedure for fault code F102?"
```

The request is passed into the query-processing pipeline.

---

## 5. API Layer

The Flask application acts as the entry point for external requests.

Responsibilities include:

* Receiving Product Queries
* Validating requests
* Managing API responses
* Streaming responses using SSE where applicable
* Handling application errors
* Connecting the web layer with the pipeline

The API layer does not perform the complete retrieval or generation process itself. Instead, it delegates processing to the application pipeline.

---

## 6. Query Pipeline

The pipeline coordinates the complete lifecycle of a Product Query.

```text
Input Query
     │
     ▼
Query Understanding
     │
     ▼
Retrieval
     │
     ▼
Context Selection
     │
     ▼
Response Generation
     │
     ▼
Validation
     │
     ▼
Final Response
```

The pipeline acts as the central orchestration layer between the agents and supporting services.

---

## 7. Multi-Agent Architecture

PQ Assistant uses four primary agents.

```text
                 ┌─────────────────────┐
                 │       Query         │
                 │   Understanding     │
                 │       Agent         │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │     Retrieval       │
                 │       Agent         │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │      Response       │
                 │     Generator       │
                 │       Agent         │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │     Validation      │
                 │       Agent         │
                 └─────────────────────┘
```

### 7.1 Query Understanding Agent

The Query Understanding Agent analyzes the user's query.

Responsibilities:

* Identify user intent
* Extract important entities
* Detect technical terminology
* Identify product information
* Extract fault codes
* Extract part numbers
* Prepare a structured retrieval query

The agent may use NLP and NER capabilities to improve query interpretation.

---

### 7.2 Retrieval Agent

The Retrieval Agent is responsible for finding relevant enterprise knowledge.

It coordinates:

* Dense retrieval
* Sparse retrieval
* Hybrid retrieval
* Reranking
* Historical PQ retrieval

The goal is to provide the response-generation agent with the most relevant context.

---

### 7.3 Response Generation Agent

The Response Generation Agent uses the retrieved context to construct the answer.

Responsibilities include:

* Understanding retrieved context
* Generating a natural-language response
* Grounding the response in retrieved information
* Avoiding unsupported claims
* Producing a clear technical answer

The primary LLM used by the system is Google Gemini 1.5 Flash.

---

### 7.4 Validation Agent

The Validation Agent evaluates the generated response before it is returned to the user.

Validation can consider:

* Relevance
* Context consistency
* Grounding
* Completeness
* Unsupported information
* Response quality

If the generated answer does not satisfy the validation requirements, the pipeline can apply the appropriate correction or handling strategy.

---

## 8. Retrieval Architecture

PQ Assistant uses a hybrid retrieval strategy.

```text
                       Query
                         │
              ┌──────────┴──────────┐
              │                     │
              ▼                     ▼
       Dense Retrieval        Sparse Retrieval
              │                     │
              ▼                     ▼
       Vector Similarity           BM25
              │                     │
              └──────────┬──────────┘
                         ▼
                Reciprocal Rank
                    Fusion
                       │
                       ▼
                  Reranking
                       │
                       ▼
                Top-K Context
```

---

## 9. Dense Retrieval

Dense retrieval converts the query into an embedding vector and searches for semantically similar document chunks.

The project uses:

```text
sentence-transformers/all-MiniLM-L6-v2
```

The embeddings are stored in ChromaDB.

Dense retrieval is useful when the query and document use different words but express similar meanings.

---

## 10. Sparse Retrieval

Sparse retrieval uses keyword-based matching.

The project uses **BM25** through the `rank_bm25` implementation.

Sparse retrieval is particularly useful for technical identifiers such as:

* Fault codes
* Part numbers
* Product codes
* Model numbers
* Exact technical terminology

Example:

```text
Query:
"Fault code F102"

Sparse retrieval can prioritize documents containing:
"F102"
```

---

## 11. Hybrid Retrieval

Dense and sparse retrieval are combined to improve retrieval robustness.

The system uses **Reciprocal Rank Fusion (RRF)** to combine rankings.

Conceptually:

```text
Dense Results
     │
     ├─────────────┐
     │             │
     ▼             ▼
Semantic Rank   Keyword Rank
     │             │
     └──────┬──────┘
            ▼
           RRF
            │
            ▼
      Combined Ranking
```

RRF helps the system benefit from both semantic similarity and exact keyword matching.

---

## 12. Reranking

After hybrid retrieval, candidate documents can be reranked to improve the ordering of the most relevant results.

```text
Initial Candidates
       │
       ▼
Hybrid Retrieval
       │
       ▼
Candidate Documents
       │
       ▼
Reranker
       │
       ▼
Top-K Relevant Context
```

The final context is passed to the response-generation stage.

---

## 13. Knowledge and Data Flow

Enterprise documents first pass through the ingestion process.

```text
Enterprise Documents
        │
        ▼
Document Ingestion
        │
        ▼
Text Extraction
        │
        ▼
Document Chunking
        │
        ▼
Embedding Generation
        │
        ▼
ChromaDB
        │
        ▼
Retrieval
        │
        ▼
Relevant Context
```

Historical Product Queries can also be stored and retrieved as part of the enterprise knowledge base.

---

## 14. Storage Architecture

PQ Assistant uses different storage mechanisms according to the type of information.

### ChromaDB

Used for:

* Document embeddings
* Vector similarity search
* Semantic retrieval

### SQLite

Used for application-level structured information such as:

* Queries
* Documents metadata
* Feedback
* Evaluation-related records
* Application state

---

## 15. Application Service Layer

The service layer contains application business logic.

Major services include:

```text
services/
├── base_service.py
├── document_service.py
└── query_service.py
```

The service layer separates business operations from API and database implementation details.

---

## 16. Repository Layer

The repository layer provides data-access abstractions.

```text
repositories/
├── base_repository.py
├── document_repository.py
└── query_repository.py
```

Repositories are responsible for interacting with persistent data without exposing database implementation details to higher-level components.

---

## 17. Ingestion Architecture

The ingestion pipeline prepares enterprise documents for retrieval.

```text
Input Documents
      │
      ▼
Document Loader
      │
      ▼
Text Processing
      │
      ▼
Chunking
      │
      ▼
Metadata Creation
      │
      ▼
Embedding Generation
      │
      ▼
Vector Storage
```

Metadata can include information such as:

* Document name
* Document type
* Product
* Section
* Source
* Page
* Technical identifiers

---

## 18. Feedback Architecture

User feedback is collected after the response is generated.

```text
Final Answer
     │
     ▼
User Feedback
     │
     ▼
Feedback Storage
     │
     ▼
Feedback Analytics
     │
     ▼
System Improvement
```

Feedback can be used to identify problematic queries and improve retrieval or response generation.

---

## 19. Evaluation Architecture

The evaluation module provides repeatable assessment of the PQ Assistant.

```text
Evaluation Dataset
       │
       ▼
PQ Questions
       │
       ▼
PQ Assistant
       │
       ▼
Generated Answers
       │
       ▼
Evaluation Metrics
       │
       ▼
RAGAS Evaluation
       │
       ▼
Evaluation Report
```

The evaluation framework can measure response and retrieval quality using predefined questions, expected answers, and relevant documents.

---

## 20. Analytics Architecture

Analytics are collected across the system.

```text
                    PQ Assistant
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
      Query          Retrieval         Response
     Analytics       Analytics        Analytics
        │                │                │
        └────────────────┼────────────────┘
                         │
               ┌─────────┴─────────┐
               ▼                   ▼
          Feedback             Performance
          Analytics             Analytics
               │                   │
               └─────────┬─────────┘
                         ▼
                  Analytics Manager
```

This allows the project to monitor system behavior and identify performance bottlenecks.

---

## 21. Error Handling

Errors should be handled at appropriate architectural boundaries.

```text
User Request
     │
     ▼
API Validation
     │
     ▼
Pipeline
     │
     ├── Query Error
     ├── Retrieval Error
     ├── Generation Error
     ├── Validation Error
     └── Storage Error
     │
     ▼
Error Handler
     │
     ▼
Structured Response
```

The system should avoid exposing internal implementation details to end users.

---

## 22. Security Considerations

Because PQ Assistant is intended for enterprise knowledge retrieval, security should be considered across all layers.

Important considerations include:

* Environment-variable-based secret management
* API input validation
* Authentication and authorization
* Protection of enterprise documents
* Safe handling of uploaded files
* Database access controls
* Secure API communication
* Logging without exposing sensitive information

API keys and other secrets should never be hardcoded into the source code.

---

## 23. Deployment Architecture

The application is designed for containerized deployment.

```text
GitHub Repository
       │
       ▼
Docker Build
       │
       ▼
Docker Image
       │
       ▼
Deployment Platform
       │
       ▼
PQ Assistant API
       │
       ├── SQLite
       └── ChromaDB
```

Docker provides a consistent runtime environment for development and deployment.

---

## 24. Complete End-to-End Flow

The complete PQ Assistant workflow can be summarized as:

```text
User Product Query
        │
        ▼
      Flask
        │
        ▼
Query Understanding Agent
        │
        ├── Intent Detection
        ├── Entity Extraction
        └── Query Processing
        │
        ▼
Retrieval Agent
        │
        ├── Dense Retrieval
        ├── BM25 Retrieval
        ├── Hybrid RRF
        └── Reranking
        │
        ▼
Top-K Relevant Context
        │
        ▼
Response Generation Agent
        │
        ▼
Generated Answer
        │
        ▼
Validation Agent
        │
        ▼
Validated Final Answer
        │
        ├───────────────┐
        ▼               ▼
     Feedback       Analytics
        │               │
        └───────┬───────┘
                ▼
            Evaluation
                │
                ▼
       Continuous Improvement
```

---

## 25. Architectural Principles

The PQ Assistant architecture follows these principles:

1. **Modularity** — Each major responsibility is separated into its own module.
2. **Separation of Concerns** — API, services, agents, retrieval, and storage have distinct responsibilities.
3. **Hybrid Retrieval** — Semantic and keyword retrieval complement each other.
4. **Grounded Generation** — Responses should be based on retrieved enterprise context.
5. **Validation** — Generated responses should be checked before delivery.
6. **Observability** — Analytics and feedback provide visibility into system behavior.
7. **Evaluability** — The system supports repeatable evaluation.
8. **Scalability** — Components can be improved or replaced independently.
9. **Maintainability** — Repository and service abstractions reduce coupling.
10. **Security** — Enterprise data and credentials must be protected throughout the architecture.
