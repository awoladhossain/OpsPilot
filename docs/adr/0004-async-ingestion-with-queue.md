# ADR-0004: Asynchronous document ingestion with Celery and Redis

- **Status:** Accepted (mentor recommendation)
- **Date:** 2026-10-01

---

### Asynchronous Ingestion & Queue Architecture

```mermaid
flowchart TD
    subgraph CLIENT_API ["1. Immediate HTTP Response (< 100ms)"]
        ADMIN(["<b>Admin Client</b><br/>Uploads 10-page policy PDF"])
        API["<b>FastAPI Upload Endpoint</b><br/>1. Saves file to disk / S3<br/>2. Inserts 'ingestion_jobs' row (status: 'uploaded')<br/>3. Pushes job to Redis queue"]
        RESP["<b>HTTP 202 Accepted</b><br/>Returns {job_id, status: 'uploaded'} immediately"]

        ADMIN -->|"POST /documents"| API
        API -->|"Instant response"| RESP
    end

    subgraph QUEUE ["2. Redis Message Broker"]
        REDIS[("<b>Redis Job Queue</b><br/>Task payload with document_id & tenant_id")]
        API -->|"Enqueue async task"| REDIS
    end

    subgraph WORKER_PROC ["3. Celery Ingestion Worker"]
        WORKER["<b>Celery Worker Process</b><br/>Consumes job & sets status: 'processing'"]
        PARSE["<b>Extract Text & Metadata</b><br/>pdfplumber / pypdf"]
        CHUNK["<b>Text Chunking</b><br/>~500 token segments with overlap"]
        EMBED["<b>Vector Generation</b><br/>Calls embedding model with retry backoff"]

        REDIS -->|"Pulls task"| WORKER
        WORKER --> PARSE --> CHUNK --> EMBED
    end

    subgraph STORAGE ["4. Persistent Database State"]
        PG[("<b>PostgreSQL (pgvector)</b><br/>• Inserts document chunks & vector embeddings<br/>• Updates 'ingestion_jobs' $\rightarrow$ status: 'ready'")]
        EMBED -->|"Atomic Commit"| PG
    end

    style CLIENT_API fill:#111827,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style QUEUE fill:#111827,stroke:#f87171,stroke-width:1px,color:#ffffff
    style WORKER_PROC fill:#111827,stroke:#fbbf24,stroke-width:2px,color:#ffffff
    style STORAGE fill:#111827,stroke:#4ade80,stroke-width:1px,color:#ffffff

    style ADMIN fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style API fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style RESP fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style REDIS fill:#3f1418,stroke:#f87171,stroke-width:2px,color:#ffffff
    style WORKER fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style PARSE fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style CHUNK fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style EMBED fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style PG fill:#142918,stroke:#4ade80,stroke-width:2px,color:#ffffff
```

---

## Context
Parsing, chunking, and embedding a document can take tens of seconds and depends on an external embedding provider. FR-012 requires visible status; NFR-003 targets 60 s for a 10-page PDF. The worker runs from the same codebase as the API.

## Options considered
1. **Synchronous:** process inside the upload request.
2. **Background task inside the API process.**
3. **Queue with separate worker processes, using Celery with a Redis broker.**
4. **Queue with a lighter library (for example ARQ or Dramatiq).**

## Decision
Use **Celery with Redis**. Job state in `ingestion_jobs`, idempotent tasks, retries with backoff and jitter, acknowledge after completion (at-least-once delivery).

## Why
- Upload returns immediately (`202`); no HTTP timeouts.
- Jobs survive API restarts; workers scale independently.
- Celery is the most widely used Python job system, so the skill transfers to jobs and interviews. Ingestion is mostly sequential I/O and CPU work, so Celery's synchronous model fits.
- The worker writes status straight to the shared database, so no callback API is needed.

## Consequences
- **Good:** resilient, observable (queue depth metric), widely documented.
- **Bad / trade-offs:** heavier than lightweight libraries; async code needs care inside tasks; duplicate delivery must be handled.
- **Follow-up:** periodic job re-enqueues stale `uploaded` documents; revisit if worker complexity outweighs benefits.

## Related
FR-012, NFR-003, [09 Flow 1](../09-key-flows.md)
