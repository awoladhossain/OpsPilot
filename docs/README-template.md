# OpsPilot

> **One-line description:** An enterprise AI assistant that answers employees' questions strictly from their company's own documents, provides verified source citations, and escalates to human specialists when answers are missing or critical.

> **How to write:** The README is the repository's "front door". A recruiter or reviewer will spend roughly 30 seconds here. Write this at the end (as the project progresses); if any section is left blank, write "Coming soon".

**Status:** In Development (Phase 1: Foundation)

---

## Why OpsPilot?

Employees waste hours searching through scattered drives or interrupting colleagues with repetitive policy questions. OpsPilot provides instant, source-backed answers with strict zero-hallucination guardrails and seamless human escalation.

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

OpsPilot is engineered as a decoupled, multi-tier system with an API Gateway managing multi-tenant security and a dedicated Python AI microservice orchestrating background ingestion, hybrid RAG, and agent execution.

```mermaid
flowchart TD
    subgraph CLIENT ["1. Client Tier"]
        UI["<b>Web Application (Next.js / React)</b><br/>• Real-time SSE chat interface<br/>• Source citation viewer<br/>• Admin management & analytics dashboard"]
    end

    subgraph GATEWAY ["2. API Gateway Tier (NestJS)"]
        GW["<b>API Gateway & Security Layer</b><br/>• JWT Authentication & Session management<br/>• Multi-tenant isolation & Row-Level Security<br/>• Rate limiting & Organization usage quotas"]
    end

    subgraph AI_SERVICE ["3. AI Service Tier (FastAPI)"]
        INGEST["<b>Async Ingestion Worker</b><br/>Parse • Chunk • Vectorize"]
        RAG["<b>Hybrid RAG Engine</b><br/>Dense vector + BM25 + Cross-Encoder Reranker"]
        AGENT["<b>Agent Runtime (LangGraph)</b><br/>Tools • Memory • Human-in-the-Loop Gate"]
        ROUTER["<b>LLM Gateway & Router</b><br/>Claude • OpenAI • Local Ollama (RTX 3050)"]

        INGEST --> RAG
        RAG --> AGENT
        AGENT --> ROUTER
    end

    subgraph DATA ["4. Data & State Tier"]
        PG["<b>PostgreSQL + pgvector</b><br/>App data, tenant configs, chat sessions & vectors"]
        REDIS["<b>Redis</b><br/>Task queues & semantic cache"]
        QDRANT["<b>Qdrant Vector DB</b><br/>High-performance vector benchmarking"]
    end

    subgraph OBS ["5. Observability & Quality Tier"]
        MON["<b>Prometheus & Grafana</b><br/>Latency, error rates & operational health"]
        TRACE["<b>Langfuse & OpenTelemetry</b><br/>LLM tracing, token cost & Ragas evaluation"]
    end

    UI -->|"HTTPS / SSE"| GW
    GW -->|"Internal gRPC / REST"| AI_SERVICE
    AI_SERVICE --> DATA
    GW -.->|"Telemetry"| OBS
    AI_SERVICE -.->|"Telemetry"| OBS

    style CLIENT fill:#111827,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style GATEWAY fill:#111827,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style AI_SERVICE fill:#111827,stroke:#4ade80,stroke-width:2px,color:#ffffff
    style DATA fill:#111827,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style OBS fill:#111827,stroke:#64748b,stroke-width:1px,color:#ffffff

    style UI fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style GW fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style INGEST fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style RAG fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style AGENT fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style ROUTER fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style PG fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style REDIS fill:#3f1418,stroke:#f87171,stroke-width:1px,color:#ffffff
    style QDRANT fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style MON fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style TRACE fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
```

---

## Tech Stack

| Domain | Technology | Rationale |
|---|---|---|
| **Frontend** | Next.js / React, Tailwind CSS | Progressive streaming (SSE), modern component architecture |
| **API Gateway** | NestJS (TypeScript) | Enterprise-grade auth, rate limiting, and multi-tenant isolation |
| **AI Service** | FastAPI (Python) | Async endpoints, LangGraph agent workflows, high-throughput RAG |
| **Databases** | PostgreSQL + pgvector | Relational tenancy, chat history, and embedded vector retrieval |
| **Specialized Vector DB** | Qdrant | Benchmarking vector indexing and search latency against pgvector |
| **Cache & Message Broker** | Redis + Celery / ARQ | Asynchronous document processing and semantic response caching |
| **RAG & Search** | Hybrid (BM25 + Dense) + BGE Reranker | High precision retrieval grounded strictly in company documentation |
| **Agent Framework** | LangGraph | State machine workflows, tool calling, and human-in-the-loop approvals |
| **LLM Router** | Claude / OpenAI / Local Ollama | Flexibility between cloud frontier models and local private inference |
| **AI Evaluation** | Ragas | Continuous automated regression testing on every PR |
| **Observability** | Prometheus, Grafana, OpenTelemetry, Langfuse | End-to-end tracing, latency profiling, and token cost accounting |
| **DevOps & Containers** | Docker, Docker Compose, GitHub Actions | Containerized microservices with automated CI/CD pipeline |

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

- [00 — How to Write Docs](00-how-to-write-docs.md)
- [01 — Problem Statement](01-problem-statement.md)
- [02 — Functional Requirements](02-functional-requirements.md)
- [03 — Non-Functional Requirements](03-non-functional-requirements.md)
- [04 — User Stories](04-user-stories.md)
- [05 — Scope, Assumptions, Risks](05-scope-assumptions-risks.md)
- [Architecture Decision Records (ADRs)](adr/)

---

## Roadmap

See phases and milestones in the project board.

## License

TBD
