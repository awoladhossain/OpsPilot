# 06 — Architecture

**Status:** Approved v2 (reference) | **Last updated:** 2026-10-01
**Inputs:** [02 FR](../02-functional-requirements.md), [03 NFR](../03-non-functional-requirements.md), [05 Scope](../05-scope-assumptions-risks.md)
**Style:** Modular monolith with a separate worker process. Not microservices (see [ADR-0003](../adr/0003-modular-monolith-not-microservices.md) and [explainer](../Code%20setup/01-is-opspilot-microservices.md)).

---

## 1. Architecture Drivers

| Requirement | Impact on design |
|---|---|
| NFR-010 Tenant isolation | `tenant_id` on every table, Postgres row-level security, isolation tests |
| NFR-001 First token < 2 s | Streaming (SSE), latency budget, hybrid retrieval with limited rerank |
| NFR-003, FR-012 Background ingestion with status | Queue and worker process, job state, retries |
| NFR-008, NFR-009 Cost | Token accounting per request, per-tenant cap, caching |
| NFR-017, NFR-025 Provider failure and independence | LLM gateway abstraction with fallback |
| NFR-012, FR-041 Prompt injection, confirmation | Agent only proposes actions; retrieved text treated as data |
| NFR-004..007 AI quality | Hybrid retrieval, "I don't know" threshold, evaluation in CI |

---

## 2. Capacity Assumptions

| Item | Estimate |
|---|---|
| Chunks | 10 tenants x 10,000 = 100,000 |
| Vector storage | 100,000 x ~4 KB (1024 dims, float32) = ~400 MB, ~1 GB with index |
| Tokens per question | ~3,000 input, ~300 output |
| Concurrency | 100 concurrent streaming chats |

One modest server is enough for v1 (~8 GB RAM assumption for the lean production stack; measure in Phase 6).

---

## 3. System Context (C4 Level 1)

```mermaid
flowchart TD
    subgraph ACTORS ["Human Actors & Consumers"]
        EMP["<b>Employee</b><br/>Queries policies, reviews citations & escalates"]
        ADM["<b>Company Admin</b><br/>Uploads docs, manages access & tracks usage"]
        ESC["<b>Escalation Contact</b><br/>Receives forwarded edge-case tickets"]
        MCP["<b>MCP Client (Phase 4)</b><br/>External AI agent connecting via MCP protocol"]
    end

    subgraph CORE ["Core Platform Boundary"]
        OP["<b>OpsPilot Platform</b><br/>Grounded enterprise AI assistant"]
    end

    subgraph EXT ["External Services"]
        LLM["<b>LLM & Embedding Providers</b><br/>Claude, OpenAI, Local Ollama"]
        MAIL["<b>Transactional Email Provider</b><br/>SMTP / Resend / SendGrid"]
        TIX["<b>Ticketing System API (Optional)</b><br/>Jira / Linear / ServiceNow"]
    end

    EMP -->|"HTTPS / SSE"| OP
    ADM -->|"Management actions"| OP
    MCP -.->|"MCP Protocol"| OP
    OP -->|"Escalation notification"| MAIL
    MAIL --> ESC
    OP -->|"Inference & Embeddings"| LLM
    OP -.->|"Create ticket"| TIX

    style ACTORS fill:#111827,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style CORE fill:#111827,stroke:#4ade80,stroke-width:2px,color:#ffffff
    style EXT fill:#111827,stroke:#fbbf24,stroke-width:1px,color:#ffffff

    style EMP fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style ADM fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style ESC fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style MCP fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style OP fill:#142918,stroke:#4ade80,stroke-width:2px,color:#ffffff
    style LLM fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style MAIL fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style TIX fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
```

---

## 4. Containers (Deployable Units — C4 Level 2)

```mermaid
flowchart TD
    subgraph CLIENT_TIER ["1. Client Tier"]
        WEB["<b>Web Application (Next.js)</b><br/>Real-time SSE chat & admin UI"]
    end

    subgraph APP_TIER ["2. Application Tier (Same Codebase)"]
        API["<b>API Process (FastAPI Modular Monolith)</b><br/>Auth, business logic, RAG, agent workflows"]
        WK["<b>Worker Process (Celery Worker)</b><br/>Background parsing, chunking & vectorization"]
    end

    subgraph DATA_TIER ["3. Persistence & Storage Layer"]
        PG[("<b>PostgreSQL + pgvector</b><br/>App data, relational tenancy & vector store")]
        RD[("<b>Redis</b><br/>Celery broker, semantic cache & rate limiter")]
        S3[("<b>MinIO Object Storage</b><br/>Raw uploaded files")]
    end

    subgraph OBS_TIER ["4. Observability Stack"]
        PR["<b>Prometheus</b><br/>Metrics aggregation"]
        GR["<b>Grafana</b><br/>Unified dashboards"]
        LK["<b>Loki + Alloy</b><br/>Structured log shipping"]
        TP["<b>Tempo</b><br/>Distributed tracing"]
        LF["<b>Langfuse</b><br/>LLM tracing & eval"]
    end

    subgraph EXT_SVCS ["5. External & Optional Inference"]
        LLM["<b>LLM & Embedding Provider</b><br/>Cloud frontier APIs"]
        MS["<b>Dedicated Model Server (Phase 7)</b><br/>Local GPU embeddings & reranking"]
    end

    WEB -->|"HTTPS REST + SSE"| API
    API -->|"Relational & vector queries"| PG
    API -->|"Cache & sessions"| RD
    API -->|"Store raw files"| S3
    API -->|"Token generation"| LLM
    API -.->|"Inference offload"| MS
    API -->|"Enqueue background job"| RD
    RD -->|"Pulls jobs"| WK
    WK -->|"Write chunks & vectors"| PG
    WK -->|"Read raw files"| S3
    WK -->|"Batch embeddings"| LLM

    API -.->|"Emits metrics"| PR
    WK -.->|"Emits metrics"| PR
    API -.->|"Traces"| LF
    API -.->|"OpenTelemetry"| TP
    PR --> GR
    LK --> GR
    TP --> GR

    style CLIENT_TIER fill:#111827,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style APP_TIER fill:#111827,stroke:#4ade80,stroke-width:2px,color:#ffffff
    style DATA_TIER fill:#111827,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style OBS_TIER fill:#111827,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style EXT_SVCS fill:#111827,stroke:#64748b,stroke-width:1px,color:#ffffff

    style WEB fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style API fill:#142918,stroke:#4ade80,stroke-width:2px,color:#ffffff
    style WK fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style PG fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style RD fill:#3f1418,stroke:#f87171,stroke-width:1px,color:#ffffff
    style S3 fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style PR fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style GR fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style LK fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style TP fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style LF fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style LLM fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style MS fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
```

---

## 5. Modules Inside the API Process (Modular Monolith)

```mermaid
flowchart TD
    subgraph FOUNDATION ["Shared Core Foundation"]
        CORE["<b>core</b><br/>Config, DB Session, Security Context, Logging, Telemetry"]
        ID["<b>identity</b><br/>Tenants, Users, Auth, Roles, Invitations"]
        CORE --> ID
    end

    subgraph DOMAINS ["Internal Domain Modules (API Process)"]
        ADM["<b>admin</b><br/>Read-only dashboard metrics"]
        CHAT["<b>chat</b><br/>Conversations, SSE streaming, Citations"]
        AGENT["<b>agent</b><br/>LangGraph state machine, HITL tools"]
        RET["<b>retrieval</b><br/>Hybrid vector + BM25, Reranker"]
        LLMG["<b>llm</b><br/>Gateway abstraction, Fallback, Token accounting"]
        DOCS["<b>documents</b><br/>Upload, Metadata, Categories, Deletion"]
        ESC["<b>escalation</b><br/>Contacts & Email dispatch"]
        USE["<b>usage</b><br/>Quota counters & Cost events"]
    end

    subgraph ASYNC_MOD ["Worker Module"]
        ING["<b>ingestion (runs in Celery worker)</b><br/>Parse, Chunk, Embed & Commit chunks"]
    end

    CHAT --> RET
    CHAT --> LLMG
    CHAT --> AGENT
    CHAT --> USE
    AGENT --> RET
    AGENT --> LLMG
    AGENT --> ESC
    RET --> LLMG
    ADM --> USE
    ADM --> DOCS
    DOCS --> ING
    ING --> LLMG

    style FOUNDATION fill:#111827,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style DOMAINS fill:#111827,stroke:#4ade80,stroke-width:2px,color:#ffffff
    style ASYNC_MOD fill:#111827,stroke:#fbbf24,stroke-width:1px,color:#ffffff

    style CORE fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style ID fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style ADM fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style CHAT fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style AGENT fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style RET fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style LLMG fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style DOCS fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style ESC fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style USE fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style ING fill:#3b2413,stroke:#fbbf24,stroke-width:2px,color:#ffffff
```

All modules depend on a small `core` package (configuration, database session, security context, logging, telemetry) and on `identity` for the current tenant and user.

### Module Responsibilities

| Module | Responsibility (one line) | Owns tables |
|---|---|---|
| identity | Tenants, users, login, roles, invitations | tenants, users |
| documents | Upload, metadata, status, categories, delete | documents, document_categories |
| ingestion | Parse, chunk, embed, store chunks (worker tasks) | document_chunks, ingestion_jobs |
| retrieval | Hybrid search, rerank, relevance threshold, role filter | none (reads chunks via ingestion's public interface) |
| llm | Provider interface, fallback, token and cost accounting | none |
| chat | Conversations, messages, SSE streaming, citations | conversations, messages, citations, feedback |
| agent | Tools, agent graph, pending actions | pending_actions |
| escalation | Contacts, escalations, email sending | escalation_contacts, escalations |
| usage | Usage events, caps, reports | usage_events |
| admin | Dashboard queries across modules (read-only through public interfaces) | none |

### Boundary Rules (Enforced in CI)

1. Each module exposes a public `service` interface; everything else is private.
2. A module never imports another module's `models` or `repository`.
3. A module reads or writes another module's data only through that module's service.
4. Dependencies point one way (see diagram); no cycles.
5. Rules are written as contracts in `import-linter` and checked on every pull request.

---

## 6. Components

| Component | Responsibility | Tech | Scales by |
|---|---|---|---|
| Web app | Chat UI, admin UI (kept thin, time-boxed) | Next.js | Static hosting / more instances |
| API process | HTTP API, auth, business rules, chat, retrieval, agent | FastAPI | More instances (stateless) |
| Worker process | Ingestion, email, cleanup, scheduled jobs | Celery, Redis broker | More workers |
| PostgreSQL | System of record, vector and keyword search | PostgreSQL + pgvector | Vertical first, read replicas later |
| Redis | Queue broker, cache, rate-limit counters | Redis | Vertical |
| Object storage | Original uploaded files | MinIO (S3 API) | Disks / cloud S3 |
| Observability | Metrics, logs, traces, LLM traces | Prometheus, Grafana, Loki, Alloy, Tempo, Langfuse | Separate host later |
| Model server (optional) | Embeddings and reranker models | Local model server container | GPU host |

---

## 7. Evolution Path (Build in Slices)

```mermaid
flowchart TD
    subgraph PHASE_A ["Foundation & Core RAG"]
        P01["<b>Phase 0-1: Foundation</b><br/>FastAPI API, Postgres RLS, JWT Auth, Streaming chat"]
        P02["<b>Phase 2: Ingestion & Storage</b><br/>Redis + Celery worker, MinIO S3, PDF Ingestion, Citation UI"]
        P03["<b>Phase 3: Retrieval Quality</b><br/>Hybrid search (BM25 + pgvector), Reranker, Ragas CI eval"]
        P01 --> P02 --> P03
    end

    subgraph PHASE_B ["Agents, Governance & Production"]
        P04["<b>Phase 4: Agent & Tools</b><br/>LangGraph agent, Propose-only tools, Human escalation, MCP server"]
        P05["<b>Phase 5: Reliability & Quotas</b><br/>Tenant spending caps, Semantic cache, LLM fallback circuit"]
        P06["<b>Phase 6: Production Observability</b><br/>Prometheus, Grafana, OpenTelemetry, Langfuse, Live VPS deploy"]
        P03 --> P04 --> P05 --> P06
    end

    subgraph PHASE_C ["Scale & Specialization"]
        P07["<b>Phase 7: Model Server Extraction</b><br/>Dedicated GPU model server for embeddings & reranking"]
        P06 --> P07
    end

    style PHASE_A fill:#111827,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style PHASE_B fill:#111827,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style PHASE_C fill:#111827,stroke:#c084fc,stroke-width:1px,color:#ffffff

    style P01 fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style P02 fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style P03 fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style P04 fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style P05 fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style P06 fill:#142918,stroke:#4ade80,stroke-width:2px,color:#ffffff
    style P07 fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
```

| Phase | What exists | Demo |
|---|---|---|
| 0-1 | API process, Postgres, tenancy, auth, LLM streaming | Login and chat streams, isolation test passes |
| 2 | + Redis, MinIO, worker, ingestion, retrieval, minimal UI | Upload policy PDF, ask, get cited answer |
| 3 | + evaluation harness, hybrid search, reranker | Score table comparing variants |
| 4 | + agent, escalation, MCP server | Propose action, confirm, escalate |
| 5 | + rate limits, caching, fallback, admin dashboard | Load test report |
| 6 | + full observability, CI/CD, deployment | Live URL with dashboards and alerts |
| 7 | + model server, routing, fine-tuning experiment | Extraction and benchmark write-up |

---

## 8. When We Would Extract a Service

| Trigger | Action |
|---|---|
| Model inference needs GPU or a different scaling profile | Extract model server (Phase 7) |
| A module has a different team or release cycle | Extract it |
| Measured bottleneck in one module | Scale or extract it |

---

## 9. Technology Choices

| Area | Choice | Main alternative | ADR |
|---|---|---|---|
| Architecture style | Modular monolith + worker | Microservices | [ADR-0003](../adr/0003-modular-monolith-not-microservices.md) |
| Tenancy | Shared tables + RLS | Schema or database per tenant | [ADR-0002](../adr/0002-tenant-isolation-shared-tables-rls.md) |
| Background jobs | Celery + Redis | ARQ, Dramatiq | [ADR-0004](../adr/0004-async-ingestion-with-queue.md) |
| Retrieval | Hybrid + rerank | Vector only | [ADR-0005](../adr/0005-hybrid-retrieval-with-rerank.md) |
| Vector store | pgvector first | Qdrant | ADR-0006 |
| LLM access | Thin internal gateway, fallback chain | Direct SDK calls | ADR-0007 |
| Authentication | Own JWT and refresh tokens using proven libraries | External identity provider | ADR-0008 |
| Agent | LangGraph, propose-only tools | Hand-written loop | ADR-0009 |

---

## 10. Risks Specific to This Architecture

| Risk | Mitigation |
|---|---|
| Modules slowly couple together | import-linter contracts in CI, module tests |
| Worker and API share code and drift | One codebase, one image, different entry command |
| Embedding model change forces re-embedding | Store `embedding_model` per chunk, re-index job |
| Too many observability components for a small server | Lean production profile; tracing and LLM tracing optional or local (see [11](11-deployment-and-observability.md)) |
