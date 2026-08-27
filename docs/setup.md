# PQ Assistant Setup Guide

## 1. Overview

This document explains how to configure and run the **PQ Assistant** project in a local development environment.

PQ Assistant uses Python 3.11 and a modular architecture containing ingestion, embeddings, retrieval, agents, services, evaluation, analytics, and web components.

---

## 2. System Requirements

Before setting up the project, ensure the following are installed.

| Requirement      | Recommended Version     |
| ---------------- | ----------------------- |
| Python           | 3.11                    |
| Git              | Latest stable version   |
| Docker           | Latest stable version   |
| Operating System | Windows / Linux / macOS |
| RAM              | 8 GB or more            |
| Storage          | At least 5 GB free      |

An internet connection is required during initial dependency installation and when using cloud-based LLM services.

---

## 3. Clone the Repository

Clone the PQ Assistant repository from GitHub.

```bash
git clone <your-github-repository-url>
cd pq_assistant
```

Replace `<your-github-repository-url>` with the actual repository URL.

---

## 4. Verify Python

Check the installed Python version:

```bash
python --version
```

The project is designed for:

```text
Python 3.11.x
```

If multiple Python versions are installed, ensure that Python 3.11 is used to create the virtual environment.

---

## 5. Create a Virtual Environment

Create a project-specific virtual environment:

```bash
python -m venv .venv
```

### Windows

Activate the environment:

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

After activation, the terminal should indicate that the virtual environment is active.

---

## 6. Upgrade pip

Upgrade the Python package manager:

```bash
python -m pip install --upgrade pip
```

---

## 7. Install Dependencies

Install the project's Python dependencies:

```bash
pip install -r requirements.txt
```

The requirements file contains the libraries required for:

* Flask
* LangChain
* Google Gemini
* Sentence Transformers
* ChromaDB
* BM25 retrieval
* spaCy
* RAGAS
* Database operations
* Application utilities

---

## 8. Install spaCy Language Model

PQ Assistant uses spaCy for Natural Language Processing and Named Entity Recognition.

Install the English language model:

```bash
python -m spacy download en_core_web_sm
```

Verify the installation:

```bash
python -c "import spacy; spacy.load('en_core_web_sm'); print('spaCy model loaded successfully')"
```

---

## 9. Environment Variables

Create a `.env` file in the project root.

```text
pq_assistant/
├── .env
├── requirements.txt
├── run.py
└── ...
```

The `.env` file should contain the required application configuration.

Example:

```env
GOOGLE_API_KEY=your_google_api_key

FLASK_ENV=development
FLASK_DEBUG=True

HOST=0.0.0.0
PORT=5000
```

Do not commit the `.env` file to GitHub.

Add it to `.gitignore`:

```text
.env
.venv/
__pycache__/
*.pyc
```

---

## 10. Google Gemini Configuration

PQ Assistant uses Google Gemini for response generation.

The application should read the Gemini API key from an environment variable rather than hardcoding it.

Example:

```env
GOOGLE_API_KEY=your_google_api_key
```

The exact configuration should match the project's implementation in the `config/` module.

---

## 11. Project Configuration

The configuration module contains centralized application settings.

```text
config/
├── __init__.py
├── settings.py
├── constants.py
└── logging_config.py
```

### `settings.py`

Contains configurable application settings such as:

* Environment configuration
* Database configuration
* Model configuration
* Retrieval configuration
* API configuration

### `constants.py`

Contains project-level constants.

### `logging_config.py`

Contains application logging configuration.

---

## 12. Required Project Directories

Ensure the major project directories exist:

```text
pq_assistant/
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
└── web/
```

---

## 13. Data Setup

Enterprise documents used by PQ Assistant should be placed in the appropriate data directory according to the ingestion module configuration.

Typical supported knowledge sources include:

```text
data/
├── documents/
├── pqs/
└── processed/
```

The exact directories should follow the paths configured in the project.

Do not place confidential enterprise documents in a public GitHub repository.

---

## 14. Database Initialization

PQ Assistant uses SQLite for structured application data.

The database components are organized under:

```text
database/
├── sqlite/
│   ├── __init__.py
│   ├── connection.py
│   ├── database_manager.py
│   ├── base.py
│   ├── models.py
│   └── sessions.py
└── chromadb/
    ├── __init__.py
    ├── client.py
    ├── collections.py
    ├── embedding_store.py
    └── vector_search.py
```

Before running the complete application, ensure that the database initialization logic is correctly configured.

---

## 15. ChromaDB Setup

ChromaDB is used for vector storage and semantic retrieval.

The application manages ChromaDB through the project's embedding and database modules.

The initial workflow is:

```text
Documents
    │
    ▼
Ingestion
    │
    ▼
Chunking
    │
    ▼
Embedding Generation
    │
    ▼
ChromaDB
```

The vector store should be initialized before attempting semantic retrieval.

---

## 16. Embedding Model Setup

PQ Assistant uses:

```text
sentence-transformers/all-MiniLM-L6-v2
```

The model is used to convert document chunks and queries into vector embeddings.

On first execution, the model may be downloaded automatically by the Sentence Transformers library.

An internet connection may therefore be required during the first embedding operation.

---

## 17. Run the Application

After completing the configuration, start the application using:

```bash
python run.py
```

If the project exposes Flask directly, the development server can also be started using the configured Flask entry point.

The application should then be accessible at:

```text
http://localhost:5000
```

---

## 18. Verify the Application

Check the health endpoint if it is implemented:

```bash
curl http://localhost:5000/health
```

Expected response:

```json
{
    "status": "healthy"
}
```

You can then test the Product Query API.

Example:

```bash
curl -X POST http://localhost:5000/api/query ^
-H "Content-Type: application/json" ^
-d "{\"query\":\"What is the recommended procedure for fault code F102?\"}"
```

---

## 19. Development Workflow

A recommended development workflow is:

```text
1. Activate virtual environment
          │
          ▼
2. Pull latest source code
          │
          ▼
3. Install/update dependencies
          │
          ▼
4. Configure .env
          │
          ▼
5. Initialize database/vector store
          │
          ▼
6. Run ingestion if required
          │
          ▼
7. Start application
          │
          ▼
8. Test API
          │
          ▼
9. Run evaluation/tests
```

---

## 20. Running Tests

Activate the virtual environment first:

```bash
.venv\Scripts\activate
```

Then run the test suite:

```bash
pytest
```

For verbose output:

```bash
pytest -v
```

Tests should cover important components such as:

* Query processing
* Retrieval
* Services
* Agents
* API behavior
* Evaluation
* Database operations

---

## 21. Running Evaluation

The evaluation module contains repeatable evaluation resources.

```text
evaluation/
├── datasets/
├── metrics.py
├── evaluator.py
├── ragas_evaluator.py
└── report_generator.py
```

The evaluation dataset contains predefined Product Query questions, expected answers, and relevant documents.

Evaluation can be executed according to the project's evaluation runner or application entry point.

---

## 22. Troubleshooting

### Python Version Error

Check:

```bash
python --version
```

Ensure Python 3.11 is being used.

---

### Dependency Error

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Then reinstall:

```bash
pip install -r requirements.txt
```

---

### spaCy Model Error

If the model cannot be loaded:

```bash
python -m spacy download en_core_web_sm
```

Then verify:

```bash
python -c "import spacy; spacy.load('en_core_web_sm')"
```

---

### Environment Variable Error

Verify that `.env` exists in the project root and contains the required variables.

Do not expose API keys in source code.

---

### ChromaDB Error

Check that:

* The vector store path is valid.
* The embedding model is available.
* Required directories exist.
* The application has permission to access the storage location.

---

### Import Errors

Run the application from the project root:

```bash
cd pq_assistant
python run.py
```

Avoid executing package files directly when they rely on relative imports.

For example, prefer:

```bash
python run.py
```

instead of:

```bash
python database/sqlite/connection.py
```

---

## 23. Windows Development Notes

On Windows, activate the virtual environment with:

```bash
.venv\Scripts\activate
```

If PowerShell prevents activation because of execution policies, configure the environment according to your system's PowerShell policy or use Command Prompt.

Use Windows-compatible paths when configuring local storage.

---

## 24. Docker Setup

PQ Assistant can also be executed using Docker.

Build the image:

```bash
docker build -t pq-assistant .
```

Run the container:

```bash
docker run --env-file .env -p 5000:5000 pq-assistant
```

The application should then be available at:

```text
http://localhost:5000
```

---

## 25. Security Checklist

Before running PQ Assistant in a production environment:

* [ ] Do not commit `.env` files.
* [ ] Do not hardcode API keys.
* [ ] Do not upload confidential enterprise documents to public repositories.
* [ ] Configure authentication.
* [ ] Validate API input.
* [ ] Protect database access.
* [ ] Configure appropriate logging.
* [ ] Avoid logging sensitive query content where unnecessary.
* [ ] Use HTTPS in production.
* [ ] Configure appropriate access controls.

---

## 26. Recommended First-Time Setup

For a new developer, the recommended sequence is:

```text
Clone Repository
      │
      ▼
Install Python 3.11
      │
      ▼
Create Virtual Environment
      │
      ▼
Install requirements.txt
      │
      ▼
Install spaCy Model
      │
      ▼
Configure .env
      │
      ▼
Initialize Database
      │
      ▼
Initialize Vector Store
      │
      ▼
Load Knowledge Documents
      │
      ▼
Run Application
      │
      ▼
Test API
      │
      ▼
Run Tests / Evaluation
```

---

## 27. Setup Completion Checklist

* [ ] Python 3.11 installed
* [ ] Repository cloned
* [ ] Virtual environment created
* [ ] Virtual environment activated
* [ ] pip upgraded
* [ ] Dependencies installed
* [ ] spaCy model installed
* [ ] `.env` configured
* [ ] API credentials configured
* [ ] SQLite configured
* [ ] ChromaDB configured
* [ ] Embedding model available
* [ ] Enterprise documents prepared
* [ ] Application started successfully
* [ ] Health endpoint verified
* [ ] Query API tested
* [ ] Tests executed successfully

---

## 28. Next Steps

After completing the setup:

1. Review [`architecture.md`](architecture.md).
2. Review [`api.md`](api.md).
3. Load the required enterprise knowledge documents.
4. Run the ingestion pipeline.
5. Initialize embeddings and vector storage.
6. Start the PQ Assistant application.
7. Test Product Query processing.
8. Run the evaluation suite.
9. Review analytics and feedback data.
10. Prepare the application for deployment.
