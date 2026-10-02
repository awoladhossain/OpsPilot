# OpsPilot

> **One-line description:** An enterprise AI assistant that answers employees' questions strictly from their company's own documents, provides verified source citations, and escalates to human specialists when answers are missing or critical.

> **How to write:** The README is the repository's "front door". A recruiter or reviewer will spend roughly 30 seconds here. Write this at the end (as the project progresses); if any section is left blank, write "Coming soon".

**Status:** In Development (Phase 1: Foundation)

---

## Why OpsPilot?

Employees waste time searching scattered drives or interrupting colleagues with repeated policy questions. OpsPilot aims to provide quick, source-backed answers, avoid unsupported claims, and make it easy to escalate questions to a person.

### End-to-End User Experience & Value Flow

```mermaid
flowchart TD
    subgraph USER_STEP ["1. Employee Interaction"]
        ASK["<b>Employee asks question</b><br/>'What is our paternity leave policy?'"]
    end

    subgraph SYSTEM_STEP ["2. Grounded OpsPilot Engine"]
        RETRIEVE["<b>Hybrid Retrieval + Rerank</b><br/>Search indexed company documents"]
        EVAL{"<b>Verified match found?</b>"}
        
        RETRIEVE --> EVAL
        
        ANSWER["<b>Streaming Answer with Citations</b><br/>Direct quote + source document & page link"]
        ESCALATE["<b>Zero Hallucination Rejection</b><br/>Honest 'I don't know' + 1-click human escalation"]
        
        EVAL -- "Yes" --> ANSWER
        EVAL -- "No or Critical" --> ESCALATE
    end

    subgraph ADMIN_STEP ["3. Continuous Knowledge Flywheel"]
        DASH["<b>Admin Knowledge Gap Dashboard</b><br/>Unanswered questions surface automatically"]
        UPDATE["<b>Doc Update / Policy Fix</b><br/>Admin uploads revised document"]
        
        ESCALATE --> DASH
        DASH --> UPDATE
    end

    ASK --> RETRIEVE

    style USER_STEP fill:#111827,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style SYSTEM_STEP fill:#111827,stroke:#4ade80,stroke-width:2px,color:#ffffff
    style ADMIN_STEP fill:#111827,stroke:#c084fc,stroke-width:1px,color:#ffffff

    style ASK fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style RETRIEVE fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style EVAL fill:#3b2413,stroke:#fbbf24,stroke-width:2px,color:#ffffff
    style ANSWER fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style ESCALATE fill:#3f1418,stroke:#f87171,stroke-width:1px,color:#ffffff
    style DASH fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style UPDATE fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
```

---

## Features

- [x] Documented requirements and architecture decisions
- [ ] Multi-tenant organization isolation (PostgreSQL RLS)
- [ ] Document upload and background ingestion (PDF, DOCX, TXT, MD)
- [ ] Hybrid retrieval (Dense vector + BM25) with cross-encoder reranking
- [ ] Real-time streaming chat with verified document citations
- [ ] Safe fallback: 100% "I don't know" threshold with 1-click human escalation
- [ ] Assistant actions with Human-in-the-Loop (HITL) confirmation
- [ ] Admin dashboard (usage, token costs, knowledge gap discovery)
- [ ] Full observability (Prometheus, Grafana, OpenTelemetry, Langfuse)

---

## System Architecture

OpsPilot is designed as a modular monolith with a separate worker process. The API and worker share one Python codebase; the worker handles background document ingestion. PostgreSQL with pgvector stores application data and vectors, Redis supports background jobs and caching, and object storage holds uploaded files.

```mermaid
flowchart TD
    subgraph CLIENT ["1. Client Tier"]
        UI["<b>Web Application (Next.js / React)</b><br/>• Real-time SSE chat interface<br/>• Source citation viewer<br/>• Admin management & analytics dashboard"]
    end

    subgraph APPLICATION ["2. Application (FastAPI Modular Monolith)"]
        API["<b>API Process</b><br/>Authentication • Tenant isolation • Chat • Retrieval • Admin"]
        WORKER["<b>Worker Process (same codebase)</b><br/>Document parsing • Chunking • Embeddings"]
        MODULES["<b>Internal modules</b><br/>Identity • Documents • Chat • Retrieval • Agent • Usage • Escalation"]
        API --> MODULES
    end

    subgraph DATA ["3. Data & State Tier"]
        PG["<b>PostgreSQL + pgvector</b><br/>App data, tenant configs, chat sessions & vectors"]
        REDIS["<b>Redis</b><br/>Task queues & semantic cache"]
        STORAGE["<b>S3-Compatible Object Storage</b><br/>SeaweedFS locally • Production provider TBD"]
    end

    subgraph OBS ["4. Observability & Quality Tier"]
        MON["<b>Prometheus & Grafana</b><br/>Latency, error rates & operational health"]
        TRACE["<b>Langfuse & OpenTelemetry</b><br/>LLM tracing, token cost & Ragas evaluation"]
    end

    UI -->|"HTTPS / SSE"| API
    API -->|"Enqueue jobs"| REDIS
    REDIS --> WORKER
    API --> PG
    WORKER --> PG
    WORKER --> STORAGE
    API -->|"LLM and embedding requests"| PROVIDERS["External AI providers"]
    API -.->|"Telemetry"| OBS
    WORKER -.->|"Telemetry"| OBS

    style CLIENT fill:#111827,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style APPLICATION fill:#111827,stroke:#4ade80,stroke-width:2px,color:#ffffff
    style DATA fill:#111827,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style OBS fill:#111827,stroke:#64748b,stroke-width:1px,color:#ffffff

    style UI fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style API fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style WORKER fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style MODULES fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style PG fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style REDIS fill:#3f1418,stroke:#f87171,stroke-width:1px,color:#ffffff
    style STORAGE fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style MON fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style TRACE fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
```

---

## Tech Stack

| Domain | Technology | Rationale |
|---|---|---|
| **Frontend** | Next.js / React, Tailwind CSS | Progressive streaming (SSE), modern component architecture |
| **Backend** | FastAPI (Python), modular monolith | API and domain modules in one codebase |
| **Background jobs** | Celery + Redis | Asynchronous document processing in a separate worker process |
| **Databases** | PostgreSQL + pgvector | Relational tenancy, chat history, and embedded vector retrieval |
| **Object storage** | SeaweedFS locally, S3 API | Production provider to be selected in Phase 6 |
| **Cache & Message Broker** | Redis | Job queue broker and cache |
| **RAG & Search** | Hybrid (BM25 + Dense) + BGE Reranker | High precision retrieval grounded strictly in company documentation |
| **Agent Framework** | LangGraph | State machine workflows, tool calling, and human-in-the-loop approvals |
| **LLM Router** | Claude / OpenAI / Local Ollama | Flexibility between cloud frontier models and local private inference |
| **AI Evaluation** | Ragas | Continuous automated regression testing on every PR |
| **Observability** | Prometheus, Grafana, OpenTelemetry, Langfuse | End-to-end tracing, latency profiling, and token cost accounting |
| **DevOps & Containers** | Docker, Docker Compose, GitHub Actions | Containerized API and worker with automated CI/CD |

---

## Getting Started

```bash
git clone <repo-url>
cd opspilot
cp .env.example .env
docker compose up
```

---

## Documentation

- [00 — How to Write Docs](../01-product/00-writing-documentation.md)
- [01 — Problem Statement](../01-product/01-problem-statement.md)
- [02 — Functional Requirements](../01-product/02-functional-requirements.md)
- [03 — Non-Functional Requirements](../01-product/03-non-functional-requirements.md)
- [04 — User Stories](../01-product/04-user-stories.md)
- [05 — Scope, Assumptions, Risks](../01-product/05-scope-assumptions-risks.md)
- [Architecture Decision Records (ADRs)](../02-system-design/decisions)

---

## Roadmap

See phases and milestones in the project board.

## License

TBD
