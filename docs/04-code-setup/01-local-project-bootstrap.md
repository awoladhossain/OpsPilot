# Local Project Bootstrap

This guide records the commands used to create the initial OpsPilot application scaffolds. It assumes the repository and its `docs/` folder already exist. Run the project commands from the repository root unless a command changes directories.

## Planned stack

- **Frontend:** Next.js, React, TypeScript, and Tailwind CSS
- **Backend:** FastAPI on Python 3.12
- **Database and vector search:** PostgreSQL with pgvector
- **Background jobs and cache:** Celery and Redis
- **File storage:** SeaweedFS locally through its S3-compatible API

NestJS was an earlier proposal. The current backend plan is FastAPI.

## 1. Check the development tools

```bash
cd /home/username/Projects/OpsPilot

git --version
docker --version
docker compose version
uv --version
node --version
npm --version
```

Next.js requires Node.js 20.9 or newer. If `uv` is missing on Linux, install it with the official installer and open a new terminal:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install Docker for your operating system using the [official Docker instructions](https://docs.docker.com/engine/install/).

## 2. Create the backend scaffold

From the repository root:

```bash
mkdir -p backend frontend infra/postgres/init docs/notes
uv init --app --python 3.12 backend

cd backend
uv add fastapi "uvicorn[standard]" pydantic-settings sqlalchemy asyncpg alembic pgvector redis celery boto3
uv add --dev pytest pytest-asyncio httpx ruff mypy import-linter pre-commit
uv sync
cd ..
```

`uv init` creates the Python project and virtual environment configuration. `uv add` records runtime and development dependencies in `pyproject.toml`; `uv.lock` pins the resolved versions. Use `uv run` to run Python tools in this project environment.

Verify that Alembic is installed in the project environment:

```bash
cd backend
uv sync
uv run python -c "import alembic; print(alembic.__version__)"
cd ..
```

## 3. Create the frontend scaffold

From the repository root:

```bash
npx create-next-app@latest frontend --yes
```

The default setup includes TypeScript, Tailwind CSS, ESLint, and the Next.js App Router. Start the development server with:

```bash
cd frontend
npm run dev
```

Open <http://localhost:3000>. Stop the server with `Ctrl+C`.

## 4. Review the generated files

From the repository root:

```bash
git status --short
find backend frontend infra docs/notes -maxdepth 2 -type f | sort
```

Keep both dependency lockfiles (`backend/uv.lock` and `frontend/package-lock.json`) in version control. Do not commit `backend/.venv`, `frontend/node_modules`, or local secret files such as `.env`.

## 5. Select the backend Python interpreter in the editor

The backend virtual environment is:

```text
/home/awolad/Projects/OpsPilot/backend/.venv/bin/python
```

In VS Code or Cursor:

1. Open the Command Palette with `Ctrl+Shift+P`.
2. Choose **Python: Select Interpreter**.
3. Select the interpreter above. If it is not listed, choose **Enter interpreter path** and paste it.
4. Reload the editor window if import warnings remain.

Running that Python path directly in a terminal only opens the Python prompt; it does not change the editor's selected interpreter. Exit the prompt with `exit()`.

## Current setup boundary

These commands create the frontend and backend scaffolds and install their dependencies. The backend is still the generated starter package until a FastAPI application and health endpoint are added. The `infra/` folders are placeholders; PostgreSQL, Redis, and object storage are not running until a Compose file is created.
