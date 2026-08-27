# PQ Assistant API Documentation

## 1. Overview

PQ Assistant provides a Flask-based API for interacting with the Product Query Assistant.

The API acts as the interface between the client application and the PQ Assistant processing pipeline.

The API is responsible for:

* Receiving Product Queries
* Validating incoming requests
* Sending queries to the processing pipeline
* Returning generated responses
* Streaming responses when SSE is enabled
* Returning structured error responses
* Supporting feedback submission

---

## 2. Base URL

### Local Development

```text
http://localhost:5000
```

### Production

The production base URL depends on the deployment environment.

For example:

```text
https://<your-pq-assistant-domain>
```

---

## 3. API Architecture

```text
Client
  │
  ▼
Flask API
  │
  ├── Request Validation
  │
  ├── Query Service
  │
  └── Query Pipeline
          │
          ├── Query Understanding
          ├── Retrieval
          ├── Response Generation
          └── Validation
                    │
                    ▼
               Final Response
```

---

# 4. Query API

## 4.1 Submit Product Query

### Endpoint

```http
POST /api/query
```

### Description

Submits a Product Query to PQ Assistant and returns an AI-generated response based on the retrieved enterprise knowledge.

### Request Headers

```http
Content-Type: application/json
```

### Request Body

```json
{
    "query": "What is the recommended procedure for fault code F102?"
}
```

### Example Request

```bash
curl -X POST http://localhost:5000/api/query \
-H "Content-Type: application/json" \
-d "{\"query\":\"What is the recommended procedure for fault code F102?\"}"
```

### Successful Response

```json
{
    "success": true,
    "query": "What is the recommended procedure for fault code F102?",
    "answer": "The recommended procedure is to first inspect the specified component and follow the troubleshooting steps provided in the relevant maintenance documentation.",
    "sources": [
        {
            "document": "maintenance_manual.pdf",
            "page": 42
        }
    ]
}
```

### Response Fields

| Field     | Type    | Description                             |
| --------- | ------- | --------------------------------------- |
| `success` | Boolean | Indicates whether the request succeeded |
| `query`   | String  | Original Product Query                  |
| `answer`  | String  | Generated and validated response        |
| `sources` | Array   | Retrieved source information            |

---

# 5. Query Validation

The API should validate the incoming request before processing.

A valid request should contain:

```json
{
    "query": "Product Query text"
}
```

### Invalid Request

```json
{
    "query": ""
}
```

### Example Error Response

```json
{
    "success": false,
    "error": {
        "code": "INVALID_QUERY",
        "message": "Query must not be empty."
    }
}
```

### HTTP Status

```text
400 Bad Request
```

---

# 6. Server-Sent Events API

PQ Assistant can support streaming responses using **Server-Sent Events (SSE)**.

### Endpoint

```http
GET /api/query/stream
```

The endpoint can be used when the application needs to deliver response-generation progress or streamed output to the client.

### Example Request

```text
GET /api/query/stream?query=Explain%20fault%20code%20F102
```

### Example SSE Response

```text
data: {"type":"status","message":"Understanding query"}

data: {"type":"status","message":"Searching knowledge base"}

data: {"type":"status","message":"Generating response"}

data: {"type":"status","message":"Validating response"}

data: {"type":"answer","content":"The recommended procedure is..."}

data: {"type":"complete","success":true}
```

The client should process each SSE event as it arrives.

---

# 7. Feedback API

User feedback can be submitted after receiving a response.

### Endpoint

```http
POST /api/feedback
```

### Request Body

```json
{
    "query_id": 101,
    "rating": 5,
    "feedback": "The answer was accurate and useful."
}
```

### Successful Response

```json
{
    "success": true,
    "message": "Feedback recorded successfully."
}
```

### Possible Rating Range

```text
1 - 5
```

Where:

| Rating | Meaning   |
| -----: | --------- |
|      1 | Very poor |
|      2 | Poor      |
|      3 | Average   |
|      4 | Good      |
|      5 | Excellent |

---

# 8. Health Check API

A health endpoint can be used to determine whether the application is running.

### Endpoint

```http
GET /health
```

### Successful Response

```json
{
    "status": "healthy"
}
```

### HTTP Status

```text
200 OK
```

---

# 9. API Error Handling

PQ Assistant should return consistent error responses.

### Standard Error Format

```json
{
    "success": false,
    "error": {
        "code": "ERROR_CODE",
        "message": "Human-readable error message."
    }
}
```

### Common Error Codes

| Error Code         | HTTP Status | Description                      |
| ------------------ | ----------: | -------------------------------- |
| `INVALID_QUERY`    |         400 | Query is missing or invalid      |
| `INVALID_REQUEST`  |         400 | Request body is invalid          |
| `NOT_FOUND`        |         404 | Requested resource was not found |
| `RETRIEVAL_ERROR`  |         500 | Retrieval process failed         |
| `GENERATION_ERROR` |         500 | Response generation failed       |
| `VALIDATION_ERROR` |         500 | Response validation failed       |
| `DATABASE_ERROR`   |         500 | Database operation failed        |
| `INTERNAL_ERROR`   |         500 | Unexpected application error     |

---

# 10. Request Processing

A query request follows this flow:

```text
HTTP Request
     │
     ▼
Request Validation
     │
     ▼
Query Service
     │
     ▼
Query Pipeline
     │
     ▼
Query Understanding Agent
     │
     ▼
Retrieval Agent
     │
     ▼
Response Generation Agent
     │
     ▼
Validation Agent
     │
     ▼
Response Formatting
     │
     ▼
HTTP Response
```

---

# 11. Query Service

The API should delegate Product Query processing to the service layer rather than implementing business logic directly inside Flask routes.

Example architecture:

```text
Flask Route
     │
     ▼
QueryService
     │
     ▼
QueryPipeline
     │
     ▼
Agents + Retrieval
```

This separation improves maintainability and testability.

---

# 12. Authentication

For a production enterprise deployment, authentication should be implemented before exposing sensitive enterprise knowledge.

Possible mechanisms include:

* API keys
* JWT authentication
* Session-based authentication
* Enterprise SSO

Example authenticated request:

```http
Authorization: Bearer <access_token>
```

Authentication implementation should be configured according to the organization's security requirements.

---

# 13. Rate Limiting

Production deployments should consider API rate limiting to prevent excessive requests.

Example conceptual policy:

```text
Maximum Requests:
100 requests / minute / client
```

The actual limit should be configured according to deployment capacity.

---

# 14. Logging

API requests and failures should be logged for monitoring and troubleshooting.

Recommended information includes:

* Request timestamp
* Endpoint
* Request status
* Processing duration
* Error code
* Query identifier

Sensitive information such as API keys, credentials, or confidential enterprise content should not be written to logs.

---

# 15. API Response Lifecycle

A successful request follows:

```text
Client
  │
  ▼
POST /api/query
  │
  ▼
Validate Request
  │
  ▼
Process Query
  │
  ▼
Retrieve Context
  │
  ▼
Generate Answer
  │
  ▼
Validate Answer
  │
  ▼
Store Query Information
  │
  ▼
Return Response
```

---

# 16. Example End-to-End Interaction

### Request

```http
POST /api/query
Content-Type: application/json
```

```json
{
    "query": "What should I check when fault code F102 occurs?"
}
```

### Internal Processing

```text
Query
  │
  ▼
Intent:
Fault Troubleshooting
  │
  ▼
Entities:
F102
  │
  ▼
Dense + BM25 Retrieval
  │
  ▼
Hybrid RRF Ranking
  │
  ▼
Top-K Documents
  │
  ▼
Gemini Response Generation
  │
  ▼
Response Validation
```

### Response

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

---

# 17. API Design Principles

The PQ Assistant API follows these principles:

1. **REST-oriented design** for standard application operations.
2. **JSON-based communication** for structured requests and responses.
3. **Clear HTTP status codes** for successful and failed requests.
4. **Consistent error responses** across endpoints.
5. **Separation of API and business logic** through services.
6. **Streaming support** through Server-Sent Events where required.
7. **Security-first design** for enterprise data.
8. **Observable requests** through structured logging and analytics.
9. **Extensibility** for future endpoints and features.

---

# 18. Future API Extensions

Potential future endpoints include:

```text
GET    /api/documents
GET    /api/documents/<document_id>
POST   /api/documents
DELETE /api/documents/<document_id>

GET    /api/queries
GET    /api/queries/<query_id>

GET    /api/analytics
GET    /api/evaluation/results
POST   /api/evaluation/run
```

These endpoints can be introduced as the application evolves.
