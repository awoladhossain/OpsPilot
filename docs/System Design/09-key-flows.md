# 09 — Key Flows

**Status:** Approved v2 (reference) | **Last updated:** 2026-10-01

Participants named after modules ("Retrieval", "LLM gateway") are **in-process calls inside the API process**, not network hops.

## Flow 1: Upload and ingest a document (US-020, FR-010, FR-012)

```mermaid
sequenceDiagram
  actor Admin
  participant API as API (documents module)
  participant S3 as Object storage
  participant DB as PostgreSQL
  participant Q as Redis (queue)
  participant W as Worker (ingestion)
  participant E as Embedding provider

  Admin->>API: POST /documents (file)
  API->>API: Validate type, size, role
  API->>S3: Store file
  API->>DB: Insert document (status=uploaded)
  API->>Q: Enqueue ingestion job
  API-->>Admin: 202 (document, status=uploaded)
  W->>Q: Take job
  W->>DB: Job and document status = processing
  W->>S3: Read file
  W->>W: Parse, clean, chunk
  W->>E: Embed chunks (batches)
  W->>DB: Replace chunks, document status = ready
  Admin->>API: GET /documents (sees Ready)
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

## Flow 2: Ask a question (US-001..003, FR-020..023)

```mermaid
sequenceDiagram
  actor Emp as Employee
  participant API as API (chat module)
  participant R as Retrieval module
  participant G as LLM gateway
  participant DB as PostgreSQL
  participant P as LLM provider

  Emp->>API: POST /conversations/{id}/messages (SSE)
  API->>API: Auth, rate limit, token cap check
  API->>DB: Save user message, load recent history
  API->>G: Rewrite follow-up into standalone question
  API->>R: Retrieve(question, tenant, role)
  R->>G: Embed question
  R->>DB: Hybrid search (vector + keyword), tenant and role filtered
  R->>R: Merge, rerank, apply relevance threshold
  R-->>API: Ranked chunks or "nothing relevant"
  alt Relevant sources found
    API->>G: Generate answer from sources (stream)
    G->>P: Prompt with sources
    P-->>G: Tokens
    G-->>API: Tokens
    API-->>Emp: token and citation events
  else Nothing relevant
    API-->>Emp: Fixed "I don't know" answer and escalation hint
  end
  API->>DB: Save assistant message, citations, usage event
  API-->>Emp: done
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

## Flow 3: Escalate (US-010, FR-030)

```mermaid
sequenceDiagram
  actor Emp as Employee
  participant API as API (escalation module)
  participant DB as PostgreSQL
  participant Q as Redis (queue)
  participant W as Worker
  participant Mail as Email provider
  actor Contact

  Emp->>API: POST /escalations (conversation_id) + Idempotency-Key
  API->>DB: Find contact for category, insert escalation (open)
  API->>Q: Enqueue email job
  API-->>Emp: 201 (escalation, status=open)
  W->>Q: Take email job
  W->>Mail: Send question, conversation, sources
  Mail-->>Contact: Email
  W->>DB: delivery_status = sent
```

| Failure | Handling |
|---|---|
| Duplicate click | Idempotency key returns the same escalation |
| No contact configured | Use tenant default admin; tell the user |
| Email send fails | Retry with backoff; `delivery_status=failed` visible to admin; alert |

## Flow 4: Assistant action with confirmation (FR-040, FR-041)

```mermaid
sequenceDiagram
  actor Emp as Employee
  participant API as API (chat and agent modules)
  participant DB as PostgreSQL
  participant Ext as Ticket or email system

  Emp->>API: Ask "Create a ticket for my laptop issue"
  API->>API: Agent selects tool create_ticket (propose only)
  API->>DB: Insert pending_action (proposed, expires_at)
  API-->>Emp: Show draft with Confirm and Reject (action_proposed event)
  Emp->>API: POST /actions/{id}/confirm
  API->>DB: Set confirmed (only if proposed and not expired)
  API->>Ext: Execute action
  API->>DB: Set executed or failed
  API-->>Emp: Result
```

| Failure | Handling |
|---|---|
| User never confirms | Action expires, nothing executes |
| Confirm clicked twice | Idempotent; same result returned |
| External system fails | Status `failed`, user sees reason, can retry |
| Agent proposes something the user did not ask for | Only a proposal; nothing runs without confirm |

**Design rule:** the agent **never** performs side effects. It only proposes. Execution happens after human confirmation, in code that checks tenant, user, status, and expiry.
