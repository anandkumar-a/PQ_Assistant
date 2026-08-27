# PQ Assistant Deployment Guide

## 1. Overview

This document describes how to deploy **PQ Assistant — Agentic AI-Based Product Query Assistant using Multi-Agent RAG**.

The project is designed to support containerized deployment using **Docker** and can be deployed to a cloud platform such as **Render**.

The deployment architecture is:

```text
Developer
    │
    ▼
GitHub Repository
    │
    ▼
Docker Build
    │
    ▼
Docker Image
    │
    ▼
Cloud Platform
    │
    ▼
PQ Assistant Application
```

---

## 2. Deployment Requirements

Before deployment, ensure the following are available:

| Requirement           | Purpose                        |
| --------------------- | ------------------------------ |
| GitHub repository     | Source-code hosting            |
| Docker                | Application containerization   |
| Google Gemini API key | LLM response generation        |
| ChromaDB storage      | Vector retrieval               |
| SQLite storage        | Structured application data    |
| Cloud hosting         | Production application hosting |

---

## 3. Deployment Architecture

The production architecture can be represented as:

```text
                    ┌──────────────────┐
                    │      User        │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Cloud / Render  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Docker Container │
                    │                  │
                    │ Flask API        │
                    │ Query Pipeline   │
                    │ Agents           │
                    │ Retrieval        │
                    └───────┬──────────┘
                            │
               ┌────────────┼────────────┐
               ▼            ▼            ▼
          ┌─────────┐  ┌──────────┐  ┌──────────┐
          │ SQLite  │  │ ChromaDB │  │ Gemini   │
          │         │  │          │  │ API      │
          └─────────┘  └──────────┘  └──────────┘
```

---

# 4. Production Configuration

Production configuration should be managed through environment variables.

Example:

```env
GOOGLE_API_KEY=your_google_api_key

FLASK_ENV=production
FLASK_DEBUG=False

HOST=0.0.0.0
PORT=5000
```

Additional variables may be required depending on the final application configuration.

**Never commit production credentials to GitHub.**

---

# 5. Dockerfile

The project should contain a `Dockerfile` in the repository root:

```text
pq_assistant/
├── Dockerfile
├── requirements.txt
├── run.py
├── config/
├── agents/
├── retrieval/
├── services/
└── ...
```

A basic Docker configuration can be structured as:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python -m spacy download en_core_web_sm

EXPOSE 5000

CMD ["python", "run.py"]
```

The final Dockerfile should be aligned with the actual project entry point and dependency configuration.

---

# 6. Build Docker Image

From the project root:

```bash
docker build -t pq-assistant .
```

Verify the image:

```bash
docker images
```

The resulting image should appear in the local Docker image list.

---

# 7. Run Docker Container Locally

Create a `.env` file containing the required configuration.

Then run:

```bash
docker run --env-file .env -p 5000:5000 pq-assistant
```

The application should be accessible at:

```text
http://localhost:5000
```

---

# 8. Test the Container

Check the health endpoint:

```bash
curl http://localhost:5000/health
```

Expected response:

```json
{
    "status": "healthy"
}
```

Test the Product Query API:

```bash
curl -X POST http://localhost:5000/api/query ^
-H "Content-Type: application/json" ^
-d "{\"query\":\"What should I check for fault code F102?\"}"
```

---

# 9. Docker Environment Variables

Environment variables should be passed to the container rather than embedded inside the Docker image.

Example:

```bash
docker run \
  --env GOOGLE_API_KEY=your_google_api_key \
  -p 5000:5000 \
  pq-assistant
```

For local development, using `.env` is more convenient:

```bash
docker run --env-file .env -p 5000:5000 pq-assistant
```

---

# 10. Persistent Storage

PQ Assistant uses persistent data stores.

The main storage components are:

```text
SQLite
  │
  ├── Query information
  ├── Feedback
  └── Application data

ChromaDB
  │
  ├── Embeddings
  ├── Document vectors
  └── Vector metadata
```

Container storage is generally ephemeral, so production deployments should use persistent storage where required.

---

# 11. SQLite Deployment Considerations

SQLite is suitable for development and smaller deployments.

For production deployment, consider:

* Persistent disk storage
* Database backup
* File locking
* Concurrent access requirements

If the application grows to multiple instances or requires high concurrent database writes, a server-based relational database may be more appropriate.

---

# 12. ChromaDB Deployment Considerations

ChromaDB stores the vector representations required for semantic retrieval.

Production deployment should ensure that:

* Vector data persists across container restarts.
* The ChromaDB storage path is correctly configured.
* The embedding model configuration remains consistent.
* Document metadata is preserved.
* Backups are available where required.

For larger production deployments, a separately managed vector database can be considered.

---

# 13. Deploying to Render

PQ Assistant can be deployed to Render using the Docker-based deployment approach.

The general workflow is:

```text
GitHub
   │
   ▼
Render
   │
   ▼
Build Docker Image
   │
   ▼
Start Container
   │
   ▼
Expose Web Service
```

---

# 14. Prepare the GitHub Repository

Before deployment, ensure that the repository contains the required files:

```text
pq_assistant/
├── Dockerfile
├── requirements.txt
├── run.py
├── .gitignore
├── agents/
├── analytics/
├── config/
├── database/
├── embedding/
├── evaluation/
├── ingestion/
├── pipeline/
├── prompts/
├── repositories/
├── retrieval/
├── services/
├── utils/
└── web/
```

Do not include:

```text
.env
.venv/
__pycache__/
```

in the repository.

---

# 15. Create a Render Web Service

In Render:

1. Create a new Web Service.
2. Connect the GitHub repository.
3. Select the PQ Assistant repository.
4. Configure the service to use the Dockerfile.
5. Add the required environment variables.
6. Configure the application port.
7. Deploy the service.

The exact Render interface and available configuration options may change over time.

---

# 16. Render Environment Variables

Configure production secrets through the Render environment-variable settings.

For example:

```text
GOOGLE_API_KEY
FLASK_ENV
FLASK_DEBUG
HOST
PORT
```

The actual variables must match those used by the application's `config/settings.py`.

Do not store production API keys inside source code.

---

# 17. Port Configuration

Cloud platforms typically provide a port through an environment variable.

The Flask application should listen on the configured host and port.

Conceptually:

```python
app.run(
    host="0.0.0.0",
    port=PORT
)
```

The application should not bind only to:

```text
127.0.0.1
```

inside a production container because external traffic needs to reach the service.

---

# 18. Production Start Command

The production container should start the application using the project's configured entry point.

For the current project structure:

```bash
python run.py
```

The Dockerfile should define the corresponding startup command.

---

# 19. Health Checks

A health endpoint should be available:

```http
GET /health
```

Example:

```json
{
    "status": "healthy"
}
```

The endpoint can be used to verify that the application is running.

A production health check can monitor:

```text
Application
     │
     ▼
/health
     │
     ▼
Healthy / Unhealthy
```

---

# 20. Deployment Verification

After deployment, verify the following:

### Application

```text
Application starts successfully
```

### Health Endpoint

```text
GET /health
```

### Query API

```text
POST /api/query
```

### Database

Verify that SQLite operations work correctly.

### Vector Store

Verify that ChromaDB can retrieve indexed documents.

### LLM

Verify that Gemini API access works.

### Embeddings

Verify that the embedding model is available.

---

# 21. Production Testing

Run a basic Product Query after deployment:

```json
{
    "query": "What is the recommended troubleshooting procedure for fault code F102?"
}
```

Verify that:

1. The request reaches the API.
2. Query understanding executes.
3. Retrieval executes.
4. Relevant context is returned.
5. Response generation succeeds.
6. Validation succeeds.
7. The final answer is returned.
8. Feedback can be recorded.

---

# 22. Logging and Monitoring

Production logs should monitor:

* Application startup
* API requests
* Response status
* Query-processing duration
* Retrieval duration
* Generation duration
* Errors
* Database failures
* Vector-store failures

Example:

```text
2026-08-27 20:00:01 INFO Application started
2026-08-27 20:00:15 INFO Query received
2026-08-27 20:00:16 INFO Retrieval completed
2026-08-27 20:00:18 INFO Response generated
2026-08-27 20:00:18 INFO Validation completed
```

Sensitive information should not be unnecessarily written to logs.

---

# 23. Security Checklist

Before exposing PQ Assistant publicly:

* [ ] Disable Flask debug mode.
* [ ] Store secrets as environment variables.
* [ ] Enable HTTPS.
* [ ] Implement authentication where required.
* [ ] Validate API requests.
* [ ] Protect enterprise documents.
* [ ] Restrict database access.
* [ ] Avoid exposing internal error details.
* [ ] Secure vector-store data.
* [ ] Configure appropriate rate limiting.
* [ ] Review application dependencies for vulnerabilities.

---

# 24. Backup Strategy

Important application data should be backed up.

Potential backup targets include:

```text
SQLite Database
       │
       ▼
Periodic Backup

ChromaDB
       │
       ▼
Persistent Storage / Backup

Evaluation Results
       │
       ▼
Versioned Storage
```

Backups should be tested periodically to ensure that data can actually be restored.

---

# 25. Deployment Pipeline

A recommended CI/CD workflow is:

```text
Developer
    │
    ▼
Git Commit
    │
    ▼
GitHub
    │
    ▼
Automated Tests
    │
    ▼
Docker Build
    │
    ▼
Deployment
    │
    ▼
Health Check
    │
    ▼
Production
```

Future CI/CD automation can use GitHub Actions or another CI platform.

---

# 26. Rollback Strategy

If a new deployment introduces a critical problem:

```text
New Version
     │
     ▼
Production Failure
     │
     ▼
Identify Previous Stable Version
     │
     ▼
Rollback
     │
     ▼
Health Check
     │
     ▼
Stable Production
```

Git tags or release versions should be used to identify stable application versions.

---

# 27. Performance Considerations

Production performance depends on:

* Query volume
* LLM response latency
* Embedding generation
* Retrieval latency
* Reranking time
* Database performance
* Available CPU and memory
* Vector-store size

Analytics should be used to identify bottlenecks.

Important measurements include:

```text
Query Latency
Retrieval Latency
Generation Latency
Validation Latency
Total Response Time
```

---

# 28. Scaling Considerations

For larger workloads, the following components can be scaled independently:

```text
             PQ Assistant
                   │
       ┌───────────┼───────────┐
       ▼           ▼           ▼
      API       Retrieval    Storage
       │           │           │
       ▼           ▼           ▼
    Multiple    Vector DB    Managed DB
    Workers
```

Potential future improvements include:

* Production-grade relational database
* Managed vector database
* Distributed task processing
* Caching
* Multiple application instances
* Load balancing
* Dedicated observability infrastructure

---

# 29. Production Deployment Checklist

* [ ] Repository is ready.
* [ ] `Dockerfile` is present.
* [ ] `requirements.txt` is up to date.
* [ ] Production environment variables are configured.
* [ ] Secrets are not committed.
* [ ] Docker image builds successfully.
* [ ] Container starts successfully.
* [ ] Application listens on `0.0.0.0`.
* [ ] Production port is configured.
* [ ] Health endpoint works.
* [ ] Query endpoint works.
* [ ] Gemini API access works.
* [ ] Embedding model works.
* [ ] ChromaDB works.
* [ ] SQLite persistence is configured.
* [ ] Logs are available.
* [ ] Backups are configured where required.
* [ ] Security configuration is reviewed.
* [ ] Production query has been tested.

---

# 30. Recommended Deployment Sequence

The complete deployment sequence is:

```text
1. Complete Development
        │
        ▼
2. Run Unit Tests
        │
        ▼
3. Run Evaluation
        │
        ▼
4. Review Analytics
        │
        ▼
5. Build Docker Image
        │
        ▼
6. Test Container Locally
        │
        ▼
7. Push Code to GitHub
        │
        ▼
8. Configure Cloud Service
        │
        ▼
9. Configure Environment Variables
        │
        ▼
10. Deploy
        │
        ▼
11. Run Health Check
        │
        ▼
12. Run Production Query
        │
        ▼
13. Monitor Logs and Performance
```

---

# 31. Final Deployment Architecture

```text
                           USER
                             │
                             ▼
                    ┌─────────────────┐
                    │  Cloud Platform │
                    │     / Render    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Docker Container│
                    │                 │
                    │ Flask API       │
                    │ Services        │
                    │ Pipeline        │
                    │ Agents          │
                    │ Retrieval       │
                    └───────┬─────────┘
                            │
            ┌───────────────┼────────────────┐
            │               │                │
            ▼               ▼                ▼
       ┌─────────┐     ┌──────────┐    ┌────────────┐
       │ SQLite  │     │ ChromaDB │    │ Gemini API │
       └─────────┘     └──────────┘    └────────────┘
                            │
                            ▼
                    Enterprise Knowledge
```

---

# 32. Related Documentation

* [`README.md`](README.md) — Documentation overview
* [`architecture.md`](architecture.md) — System architecture
* [`api.md`](api.md) — API reference
* [`setup.md`](setup.md) — Local setup
* [`usage.md`](usage.md) — Usage guide
* [`evaluation.md`](evaluation.md) — Evaluation framework
