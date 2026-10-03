# OpsPilot Backend

FastAPI-based modular monolith backend for OpsPilot.

## Tech Stack
- **Framework:** FastAPI (Python 3.12+)
- **ASGI Server:** Uvicorn
- **Database & Vector Search:** PostgreSQL + SQLAlchemy + asyncpg + pgvector
- **Migrations:** Alembic
- **Task Queue & Cache:** Celery + Redis
- **Storage:** S3-compatible (SeaweedFS / AWS S3) via boto3
- **Package Manager:** [uv](https://astral.sh/uv)
- **Quality & Testing:** pytest, ruff, mypy

## Quick Start

### 1. Install Dependencies
```bash
uv sync
```

### 2. Run Development Server
```bash
uv run uvicorn app.main:app --reload --port 8000
```
- Health Check: http://localhost:8000/health/live
- Swagger API Docs: http://localhost:8000/docs

### 3. Run Quality Tools
```bash
# Format code
uv run ruff format .

# Lint code
uv run ruff check --fix .

# Type checking
uv run mypy app

# Run tests
uv run pytest
```
