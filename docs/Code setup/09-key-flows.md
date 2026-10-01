# 09 — Key Flows

**Status:** Approved v2 (reference) | **Last updated:** 2026-10-01

Participants named after modules ("Retrieval", "LLM gateway") are **in-process calls inside the API process**, not network hops.

---

## Master Flow Architecture & Orchestration Map

```mermaid
flowchart TD
    subgraph ADMIN_PATH ["Admin Journey"]
        F1["<b>Flow 1: Document Upload & Ingestion</b><br/>Admin uploads PDF $\rightarrow$ Async Celery worker parses, chunks & embeds"]
    end

    subgraph EMPLOYEE_PATH ["Employee Journey"]
        F2["<b>Flow 2: Streaming Grounded RAG</b><br/>Employee asks query $\rightarrow$ Hybrid search + Reranking $\rightarrow$ Token stream with citations"]
        F3["<b>Flow 3: Contextual Escalation</b><br/>Missing answer or edge case $\rightarrow$ 1-click ticket routed to HR/IT contact"]
        F4["<b>Flow 4: HITL Assistant Action</b><br/>Employee asks for action $\rightarrow$ Agent drafts proposal $\rightarrow$ Explicit confirmation gate"]
    end

    F1 -->|"Documents searchable"| F2
    F2 -->|"Unanswered / Critical"| F3
    F2 -->|"Action requested (ticket/email)"| F4

    style ADMIN_PATH fill:#111827,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style EMPLOYEE_PATH fill:#111827,stroke:#4ade80,stroke-width:2px,color:#ffffff

    style F1 fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style F2 fill:#142918,stroke:#4ade80,stroke-width:2px,color:#ffffff
    style F3 fill:#3f1418,stroke:#f87171,stroke-width:1px,color:#ffffff
    style F4 fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
```

---

## Flow 1: Upload and Ingest a Document (US-020, FR-010, FR-012)

```mermaid
sequenceDiagram
    autonumber
    actor Admin
    participant API as API (documents module)
    participant S3 as Object Storage (MinIO)
    participant DB as PostgreSQL (pgvector)
    participant Q as Redis (Job Queue)
    participant W as Worker (Celery)
    participant E as Embedding Provider

    Admin->>API: POST /documents (file) + Idempotency-Key
    activate API
    API->>API: Validate file format, size, and admin role
    API->>S3: Store raw binary file
    API->>DB: Insert document (status = 'uploaded')
    API->>Q: Enqueue ingestion job (document_id, tenant_id)
    API-->>Admin: 202 Accepted (document_id, status = 'uploaded')
    deactivate API

    Q->>W: Pull ingestion job
    activate W
    W->>DB: Update document & job status = 'processing'
    W->>S3: Read raw file stream
    W->>W: Parse PDF text, clean & generate chunks (~500 tokens)
    
    loop Batch Embedding Generation
        W->>E: Batch embed chunks (retry with backoff on 429)
        E-->>W: Return vector embeddings
    end

    W->>DB: Atomic replace chunks & update status = 'ready'
    deactivate W

    Admin->>API: GET /documents/{id}
    API-->>Admin: Status: Ready (Searchable)
```

Worker writes status directly to the database (same codebase and database), so no callback is needed.

| Failure | Handling |
|---|---|
| Duplicate upload (same `content_hash`) | `409 Conflict`, return existing document |
| File stored but enqueue fails | Document stays `uploaded`; periodic job re-enqueues stale `uploaded` documents |
| Parse error (corrupt or scanned PDF) | Mark `failed` with readable reason; no retry |
| Embedding provider timeout or `429` | Retry with exponential backoff and jitter (max 3), then `failed` |
| Worker crashes mid-job | Job re-delivered; ingestion is **idempotent** (delete existing chunks for the document, then insert) |
| Document deleted while processing | Worker re-checks status before writing; discards result |
| Poison job (always fails) | Max attempts, then `failed`, alert on failure rate |

---

## Flow 2: Ask a Question (US-001..003, FR-020..023)

```mermaid
sequenceDiagram
    autonumber
    actor Emp as Employee
    participant API as API (chat module)
    participant R as Retrieval Engine
    participant G as LLM Gateway
    participant DB as PostgreSQL (pgvector)
    participant P as LLM Provider

    Emp->>API: POST /conversations/{id}/messages (SSE)
    activate API
    API->>API: Validate JWT auth, check user rate limit & tenant quota
    API->>DB: Save user message & load recent conversation history
    API->>G: Rewrite follow-up into standalone question
    API->>R: Retrieve(question, tenant_id, allowed_roles)
    
    activate R
    R->>G: Embed standalone question
    G-->>R: Query vector
    R->>DB: Hybrid search (Dense vector + BM25 tsvector) with RLS
    DB-->>R: Top 25 candidates
    R->>R: Cross-encoder rerank & apply relevance threshold
    R-->>API: Top 3–5 chunks or "Nothing relevant"
    deactivate R

    alt Relevant Sources Found (Score >= Threshold)
        API->>G: Stream grounded answer
        activate G
        G->>P: Send system prompt + context chunks + user question
        activate P
        P-->>G: Progressive token stream
        G-->>API: Tokens
        API-->>Emp: event: citation + event: token stream
        deactivate P
        deactivate G
    else Nothing Relevant (Out-of-Scope)
        API-->>Emp: Fixed honest "I don't know" answer + Escalation option
    end

    API->>DB: Save assistant response, citations & token usage
    API-->>Emp: event: done
    deactivate API
```

| Failure | Handling |
|---|---|
| Tenant over monthly token cap | `429` with clear message before any LLM call |
| Embedding or LLM timeout | One retry, then fallback model, then `error` event |
| LLM fails mid-stream | `error` event; message saved as `failed`; user can retry |
| User closes connection | Cancel generation, save partial as `cancelled` |
| Nothing relevant retrieved | "I don't know" path (never call LLM without sources) |
| Prompt injection in retrieved text | Sources wrapped as data, instructions ignored, output checked (see [10](10-security-and-tenancy.md)) |
| Database down | `503`, readiness probe fails, alert fires |

---

## Flow 3: Escalate (US-010, FR-030)

```mermaid
sequenceDiagram
    autonumber
    actor Emp as Employee
    participant API as API (escalation module)
    participant DB as PostgreSQL
    participant Q as Redis Queue
    participant W as Worker (Celery)
    participant Mail as Transactional Email
    actor Contact as Escalation Contact

    Emp->>API: POST /escalations (conversation_id) + Idempotency-Key
    activate API
    API->>DB: Find contact for category, create escalation (status='open')
    API->>Q: Enqueue email notification job
    API-->>Emp: 201 Created (escalation_id, status='open')
    deactivate API

    Q->>W: Pull email job
    activate W
    W->>Mail: Send email with Question + Chat Transcript + Sources
    activate Mail
    Mail-->>Contact: Deliver pre-packaged email alert
    Mail-->>W: SMTP Delivery 250 OK
    deactivate Mail
    W->>DB: Update delivery_status = 'sent'
    deactivate W
```

| Failure | Handling |
|---|---|
| Duplicate click | Idempotency key returns the same escalation |
| No contact configured | Use tenant default admin; tell the user |
| Email send fails | Retry with backoff; `delivery_status=failed` visible to admin; alert |

---

## Flow 4: Assistant Action with Confirmation (FR-040, FR-041)

```mermaid
sequenceDiagram
    autonumber
    actor Emp as Employee
    participant API as API (chat and agent modules)
    participant DB as PostgreSQL
    participant Ext as External System (Ticket/Email)

    Emp->>API: "Create a ticket for my laptop issue"
    activate API
    API->>API: LangGraph agent selects tool: create_ticket (Propose-Only)
    API->>DB: Insert pending_action (status='proposed', expires_at=now()+24h)
    API-->>Emp: event: action_proposed (Interactive draft with Confirm & Reject)
    deactivate API

    alt User Confirms
        Emp->>API: POST /actions/{id}/confirm + Idempotency-Key
        activate API
        API->>DB: Validate status=='proposed' & not expired; set status='confirmed'
        API->>Ext: Dispatch action payload (create ticket)
        Ext-->>API: 201 Created (ticket_id: #4810)
        API->>DB: Set status='executed'
        API-->>Emp: Success response with ticket confirmation
        deactivate API
    else User Rejects or Ignores
        Emp->>API: POST /actions/{id}/reject (or action expires)
        activate API
        API->>DB: Set status='rejected' / 'expired'
        API-->>Emp: Action cancelled; zero side-effects executed
        deactivate API
    end
```

| Failure | Handling |
|---|---|
| User never confirms | Action expires, nothing executes |
| Confirm clicked twice | Idempotent; same result returned |
| External system fails | Status `failed`, user sees reason, can retry |
| Agent proposes something the user did not ask for | Only a proposal; nothing runs without confirm |

**Design rule:** the agent **never** performs side effects autonomously. It only proposes. Execution happens after human confirmation, in code that checks tenant, user, status, and expiry.
