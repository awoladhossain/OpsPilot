# [Project Name] — System Design Document

**Status:** Draft | In review | Approved
**Author:** [name] | **Last updated:** YYYY-MM-DD
**Related:** [requirements docs, ADRs]

> **How to write:** Fill out sections in order. If a section is not applicable, write "N/A, because ..." (do not leave it blank). Keep it under 8–12 pages.

---

## 1. Overview
What are we building and why? (3-5 sentences, link to problem statement)

## 2. Goals and Non-Goals
- **Goals:**
- **Non-goals:**

## 3. Architecture Drivers
| Requirement | Impact on design |
|---|---|

## 4. Constraints and Assumptions
- **Constraints (budget, team, time, hardware):**
- **Assumptions (to validate):**

## 5. Capacity Estimation
| Item | Estimate | How computed |
|---|---|---|
| Storage | | |
| Traffic | | |
| Cost | | |
| Latency budget | | |

---

## 6. System Context (C4 Level 1)

```mermaid
flowchart TD
    subgraph ACTORS ["Human Actors"]
        EMP["<b>Employee (User)</b><br/>Queries policies & reviews citations"]
        ADM["<b>Company Admin</b><br/>Uploads documents & monitors usage"]
        ESC["<b>Department Contact</b><br/>Receives escalated edge cases"]
    end

    subgraph SYSTEM ["Core System Boundary"]
        OPS["<b>OpsPilot Platform</b><br/>Grounded Enterprise RAG & Policy Assistant"]
    end

    subgraph EXTERNAL ["External Systems & Services"]
        LLM_EXT["<b>Frontier LLM Providers</b><br/>Anthropic Claude / OpenAI / Local Ollama"]
        MAIL_EXT["<b>Escalation Channels</b><br/>Email SMTP / Internal Ticket Webhooks"]
    end

    EMP -->|"Asks questions (HTTPS / SSE)"| OPS
    ADM -->|"Manages documents & views gaps"| OPS
    OPS -->|"Forwards contextual ticket"| ESC
    OPS -->|"Inference & Embeddings"| LLM_EXT
    OPS -->|"Dispatches notifications"| MAIL_EXT

    style ACTORS fill:#111827,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style SYSTEM fill:#111827,stroke:#4ade80,stroke-width:2px,color:#ffffff
    style EXTERNAL fill:#111827,stroke:#fbbf24,stroke-width:1px,color:#ffffff

    style EMP fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style ADM fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style ESC fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style OPS fill:#142918,stroke:#4ade80,stroke-width:2px,color:#ffffff
    style LLM_EXT fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style MAIL_EXT fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
```

---

## 7. Architecture & Containers (C4 Level 2)

```mermaid
flowchart TD
    subgraph BROWSER ["Client Layer"]
        SPA["<b>Single Page Application (Next.js)</b><br/>Interactive chat UI, SSE stream consumer, admin console"]
    end

    subgraph BACKEND ["Application Backend Layer"]
        API["<b>FastAPI Modular Monolith</b><br/>Auth, Tenancy (RLS), RAG Pipeline, Agent Workflow"]
        WORKER["<b>Celery Background Worker</b><br/>Asynchronous PDF parsing, chunking & vectorization"]
        QUEUE[("<b>Redis Broker & Cache</b><br/>Task distribution & semantic cache")]
    end

    subgraph PERSISTENCE ["Storage & Vector Layer"]
        DB[("<b>PostgreSQL (pgvector)</b><br/>Tenants, Users, Documents, Chunks, Embeddings")]
        VEC[("<b>Qdrant (Optional / Phase 3)</b><br/>Benchmarked vector store")]
    end

    SPA -->|"HTTPS / SSE"| API
    API -->|"Enqueues ingestion job"| QUEUE
    QUEUE -->|"Pulls jobs"| WORKER
    API -->|"CRUD & Vector Queries"| DB
    WORKER -->|"Writes Chunks & Embeddings"| DB
    API -.->|"Benchmark comparison"| VEC

    style BROWSER fill:#111827,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style BACKEND fill:#111827,stroke:#4ade80,stroke-width:2px,color:#ffffff
    style PERSISTENCE fill:#111827,stroke:#fbbf24,stroke-width:1px,color:#ffffff

    style SPA fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style API fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style WORKER fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style QUEUE fill:#3f1418,stroke:#f87171,stroke-width:1px,color:#ffffff
    style DB fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style VEC fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
```

| Component | Responsibility | Owns (data) | Technology | Scales by |
|---|---|---|---|---|

Evolution path: v0 / v1 / v2

---

## 8. Data Design

```mermaid
erDiagram
    ORGANIZATIONS ||--o{ USERS : "has members"
    ORGANIZATIONS ||--o{ DOCUMENTS : "owns"
    ORGANIZATIONS ||--o{ CHAT_SESSIONS : "owns"
    DOCUMENTS ||--o{ DOCUMENT_CHUNKS : "chunked into"
    USERS ||--o{ CHAT_SESSIONS : "participates in"
    CHAT_SESSIONS ||--o{ CHAT_MESSAGES : "contains"
    CHAT_MESSAGES ||--o{ MESSAGE_CITATIONS : "cites"
    DOCUMENT_CHUNKS ||--o{ MESSAGE_CITATIONS : "sourced by"

    ORGANIZATIONS {
        uuid id PK
        string name
        string plan_tier
        timestamp created_at
    }
    USERS {
        uuid id PK
        uuid organization_id FK
        string email
        string role
    }
    DOCUMENTS {
        uuid id PK
        uuid organization_id FK
        string title
        string status
    }
    DOCUMENT_CHUNKS {
        uuid id PK
        uuid document_id FK
        text content
        vector embedding
    }
    CHAT_SESSIONS {
        uuid id PK
        uuid organization_id FK
        uuid user_id FK
        string title
    }
    CHAT_MESSAGES {
        uuid id PK
        uuid session_id FK
        string role
        text content
    }
```

---

## 9. Key Flows & Sequence

```mermaid
sequenceDiagram
    autonumber
    actor Employee as Employee (Client)
    participant API as FastAPI Monolith
    participant DB as Postgres (pgvector)
    participant Model as LLM Provider
    actor Contact as Escalation Contact

    Employee->>API: POST /api/chat (Query: "Leave policy?")
    activate API
    API->>DB: Set tenant session (RLS) & Query hybrid search
    activate DB
    DB-->>API: Return Top Candidates (BM25 + pgvector)
    deactivate DB
    
    alt Relevance Score >= Threshold
        API->>Model: Stream prompt with chunk context & citations
        activate Model
        Model-->>API: Token chunks (SSE)
        API-->>Employee: SSE Stream tokens + Sourced Citations
        deactivate Model
    else Out-of-Scope / No Document Match
        API-->>Employee: "I don't know" + Escalation Action Button
        opt Employee clicks Escalate
            Employee->>API: POST /api/escalate
            API->>Contact: Send Ticket (Query + History + Context)
            API-->>Employee: Ticket created & assigned
        end
    end
    deactivate API
```

| Flow | Failure | Handling |
|---|---|---|

---

## 10. API Design
(Conventions, endpoint table, error format, auth)

## 11. Security and Privacy
(Threats and controls)

## 12. Observability
(Metrics, logs, traces, alerts, dashboards)

## 13. Deployment and Operations
(Environments, CI/CD, backup, rollback)

## 14. Technology Choices
| Area | Choice | Alternatives | ADR |
|---|---|---|---|

## 15. Risks and Open Questions
| Risk / question | Mitigation / owner |
|---|---|

---

## 16. Review Checklist
- [ ] Every must-have requirement maps to design
- [ ] Every driver has a design response
- [ ] Failure scenarios walked through
- [ ] Every major decision has an ADR
