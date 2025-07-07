# GenKubeGuard

GenKubeGuard is a Kubernetes YAML security analyzer and DevSecOps assistant that integrates static analysis with a local LLM for secure, intelligent feedback. It provides patch suggestions, contextual recommendations for various developer roles, and a GraphQL API for enhanced interaction.

---

## Table of Contents

* [Features](#features)
* [Project Structure](#project-structure)
* [How to Run the Application](#how-to-run-the-application)
* [Endpoints](#endpoints)
* [Testing](#testing)
* [Technical Stack](#technical-stack)
* [Why This Project Matters](#why-this-project-matters)
* [Author](#author)
* [License](#license)

---

## Features

* Static analysis of Kubernetes YAML files using kube-linter.
* AI-generated explanations for each issue using a local LLM (Mistral via Ollama).
* Automatic patching of insecure or incomplete YAML configurations.
* Contextual suggestions tailored to the role of the user (junior, senior, or SRE).
* Lightweight retrieval-augmented memory using FAISS to log and recall prompt-response pairs.
* REST API and GraphQL endpoints for flexibility and extensibility.
* Pytest-based test suite covering core functionality and endpoints.
* Dockerized for local deployment with Ollama integration.

---

## Project Structure

```
genkubeguard/
├── src/
│   ├── llm_handler.py         # Handles explain, patch, and suggest logic using Ollama
│   ├── rag_memory.py          # In-memory RAG using FAISS
│   ├── yaml_patcher.py        # Delegates patch generation
│   ├── prompts/               # Prompt templates for explain, fix, suggest, and personas
│   └── schema.py              # GraphQL schema definition
│
├── tests/
│   ├── test_api_endpoints.py  # Tests for /analyze, /patch, /suggest, /suggest-persona, /memory
│   ├── test_llm_handler.py    # Unit tests for LLM logic
│   └── test_yaml_patcher.py   # Test for patching logic
│
├── k8s/                       # Sample Kubernetes YAML files
├── main.py                   # FastAPI application entry point
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .gitignore
└── README.md
```


## How to Run the Application

### Prerequisites

* Python 3.10+ or Docker
* Ollama with `mistral` model installed

### Install Mistral

ollama run mistral

### Set Environment Variables (Windows PowerShell)

[Environment]::SetEnvironmentVariable("OLLAMA_HOST", "localhost", "User")
[Environment]::SetEnvironmentVariable("OLLAMA_PORT", "11434", "User")

### Run with Docker Compose

docker-compose up

Access after startup:

* FastAPI Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
* GraphQL Playground: [http://localhost:8000/graphql](http://localhost:8000/graphql)

### Run Manually (Without Docker)

pip install -r requirements.txt
uvicorn main:app --reload

---

## Endpoints

### REST

POST /analyze – Uploads a YAML file, returns linter issues and LLM explanations.
POST /patch – Uploads a YAML file and returns a patched version.
POST /suggest – Uploads a YAML file and returns best-practice suggestions.
POST /suggest-persona?persona= – Returns suggestions based on developer role (junior, senior, sre).
GET /memory?q=search_term – Searches stored prompt-response memory.

### GraphQL

Visit: [http://localhost:8000/graphql](http://localhost:8000/graphql)

Queries:
analyze(yamlStr: String!): AnalysisResult
patch(yamlStr: String!): PatchResult
suggest(yamlStr: String!): SuggestionResult
suggestWithPersona(yamlStr: String!, persona: String!): SuggestionResult

---

## Testing

### Run all tests

python -m pytest

### Detailed report

pytest -v

### Test coverage

pip install pytest-cov
pytest --cov=src --cov-report=term-missing

### Tests include:

* All REST endpoints
* Patch logic
* LLM outputs
* Memory retrieval

---

## Technical Stack

* Python 3.10
* FastAPI
* Strawberry GraphQL
* Ollama (with Mistral model)
* FAISS (for vector search)
* Kube-linter (static analysis)
* Docker & Docker Compose
* Pytest

---

## Why This Project Matters

This project shows how to combine DevSecOps tooling with generative AI to automate YAML validation, generate role-specific guidance, and streamline secure Kubernetes deployment workflows. It is designed to be practical, testable, and immediately deployable  ideal for backend and GenAI developer roles.

---

## Author

**Aswathi Vipin**
[LinkedIn](https://www.linkedin.com/in/aswathivk)

---

## License

MIT License
See the [LICENSE](LICENSE) file for details.
