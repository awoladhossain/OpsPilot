# ADR-0003: Modular monolith with a separate worker, not microservices

- **Status:** Accepted (mentor recommendation). **Supersedes** the earlier two-service proposal (NestJS API service + FastAPI AI service).
- **Date:** 2026-10-01

---

### Monolith vs Microservices Architecture & Boundaries

```mermaid
flowchart TD
    subgraph COMPARE ["1. Architectural Evaluation"]
        DISTR["<b>Rejected: Two-Service Split (NestJS + FastAPI)</b><br/>• Network hop on every streaming token<br/>• Dual CI/CD pipelines, duplicate configs & distributed tracing overhead<br/>• Distributed transaction & network failure points"]
        MONO["<b>Chosen: Modular Monolith + Background Worker</b><br/>• Zero network latency on chat queries (in-process calls)<br/>• Single codebase, single Docker image, single CI pipeline<br/>• Heavy ingestion offloaded to async worker via Redis"]
    end

    subgraph ARCH ["2. Modular Monolith Internal Architecture"]
        CLIENT(["<b>Next.js Frontend Client</b>"])

        subgraph APP ["FastAPI Monolith Process"]
            MOD_AUTH["<b>core / auth / tenancy</b><br/>JWT validation, RLS session context"]
            MOD_CHAT["<b>chat / api</b><br/>SSE streaming controller & session state"]
            MOD_RAG["<b>rag / retrieval</b><br/>Hybrid vector + BM25 search & reranking"]
            MOD_AGENT["<b>agent / engine</b><br/>LangGraph workflow & tool execution"]

            MOD_AUTH --> MOD_CHAT
            MOD_CHAT --> MOD_RAG
            MOD_RAG --> MOD_AGENT
        end

        subgraph ASYNC_WORKER ["Separate Worker Process"]
            WORKER["<b>Ingestion Worker (Celery / ARQ)</b><br/>Document parse, chunk & embed"]
        end

        subgraph CI_GATE ["3. Strict Boundary Enforcement"]
            LINT["<b>import-linter Contracts in CI</b><br/>Prohibits circular dependencies & keeps modules cleanly extractable"]
        end

        CLIENT -->|"HTTPS / SSE"| MOD_CHAT
        MOD_CHAT -->|"Push heavy job via Redis"| WORKER
        APP -.->|"Verified in CI"| LINT
    end

    style COMPARE fill:#111827,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style ARCH fill:#111827,stroke:#38bdf8,stroke-width:2px,color:#ffffff
    style APP fill:#111827,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style ASYNC_WORKER fill:#111827,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style CI_GATE fill:#111827,stroke:#4ade80,stroke-width:1px,color:#ffffff

    style DISTR fill:#3f1418,stroke:#f87171,stroke-width:1px,color:#ffffff
    style MONO fill:#142918,stroke:#4ade80,stroke-width:2px,color:#ffffff

    style CLIENT fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style MOD_AUTH fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style MOD_CHAT fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style MOD_RAG fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style MOD_AGENT fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style WORKER fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style LINT fill:#142918,stroke:#4ade80,stroke-width:2px,color:#ffffff
```

---

## Context
OpsPilot has business concerns (auth, tenants, history, usage, escalation) and AI concerns (ingestion, retrieval, generation, agent). It is built by one developer whose goal is to learn AI engineering in about six months, with a small budget. Every chat request needs both kinds of concerns at once.

## Options considered
1. **Microservices:** many small services with their own data.
2. **Two services:** NestJS for business, FastAPI for AI.
3. **Modular monolith (FastAPI) + worker process:** one codebase, strict module boundaries, background jobs in a separate process, optional model server later.

## Decision
Use option 3. Enforce module boundaries with `import-linter` contracts in CI. Extract a service only when a measured trigger exists. First planned extraction: model server for embeddings and reranking (Phase 7).

## Why
- Matches the learning goal: effort goes to AI and production practices, not to a second codebase.
- The business/AI boundary is not a real boundary; one request needs both, so a network hop adds only failure points.
- One image, one CI pipeline, one logging and tracing setup.
- Clean modules keep later extraction cheap.

## Consequences
- **Good:** simpler to build, test, debug, and deploy; transactions stay in one database.
- **Bad / trade-offs:** discipline needed to keep modules separate; the whole API scales as one unit; less microservices experience (partly covered by the worker and model server).
- **Follow-up:** revisit when a trigger in [06 section 8](../06-architecture.md) occurs.

## Related
[Explainer](../../01-is-opspilot-microservices.md), [06 Architecture](../06-architecture.md)
