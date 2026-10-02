# ADR-0001: Vector storage for document search (EXAMPLE)

- **Status:** Example only. You will make the real decision in Step 2, after learning and testing.
- **Date:** YYYY-MM-DD
- **Deciders:** Awolad

> This is only an **example to demonstrate the format**. Write the actual decision after conducting your own research and testing; do not copy this content directly.

---

### Decision & Evaluation Architecture

```mermaid
flowchart TD
    subgraph CHALLENGE ["1. Problem & Architectural Drivers"]
        REQ["<b>Core Need:</b> Store embeddings & perform semantic search<br/>• Strict tenant isolation (NFR-010)<br/>• Minimal operational overhead & low VPS budget"]
    end

    subgraph OPTIONS ["2. Options Evaluated"]
        O_PG["<b>Option 1: PostgreSQL + pgvector (CHOSEN)</b><br/>• Single database for app data, users & vectors<br/>• Native ACID transactions & Row-Level Security (RLS)<br/>• Zero additional infrastructure or memory overhead"]
        O_QD["<b>Option 2: Dedicated Vector DB (Qdrant)</b><br/>• Ultra-fast HNSW indexing & filtering<br/>• Extra container to deploy, back up & synchronize with DB"]
        O_CLOUD["<b>Option 3: Managed Cloud Vector Service</b><br/>• Fully managed (e.g., Pinecone)<br/>• Violates budget constraint; vendor lock-in & data residency risk"]
    end

    subgraph STRATEGY ["3. Two-Phase Evolutionary Strategy"]
        P1["<b>Phase 1 & 2 (v1 Launch):</b><br/>Run on <b>PostgreSQL + pgvector</b><br/>Unified backups, RLS isolation, simple DevOps"]
        P2["<b>Phase 3 (Empirical Benchmarking):</b><br/>Deploy <b>Qdrant side-by-side</b> to benchmark<br/>Measure p95 latency & recall at 10k-100k chunks"]

        P1 -->|"Benchmark threshold met?"| P2
    end

    REQ --> OPTIONS
    O_PG --> P1
    O_QD -.-> P2

    style CHALLENGE fill:#111827,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style OPTIONS fill:#111827,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style STRATEGY fill:#111827,stroke:#4ade80,stroke-width:2px,color:#ffffff

    style REQ fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style O_PG fill:#142918,stroke:#4ade80,stroke-width:2px,color:#ffffff
    style O_QD fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style O_CLOUD fill:#3f1418,stroke:#f87171,stroke-width:1px,color:#ffffff
    style P1 fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style P2 fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
```

---

## Context
OpsPilot needs to store text embeddings and find the most similar chunks for a question. Data of each organization must stay isolated (NFR-010). The system already needs a relational database for users, organizations, and chat history.

## Options considered
1. **PostgreSQL with pgvector**: vectors stored next to application data.
2. **Dedicated vector database (e.g., Qdrant)**: separate service built for vector search.
3. **Managed cloud vector service**: hosted, less to operate.

## Decision
Start with **PostgreSQL + pgvector** (example).

## Why
- One database to run and back up, fits the low-budget constraint.
- Tenant filter and vector search can use the same query and row-level security.
- Enough for v1 load (NFR-018: 10,000 chunks per organization).

## Consequences
- **Good:** simpler operations, transactional consistency between documents and vectors.
- **Bad / trade-offs:** may be slower than a dedicated vector database at large scale.
- **Follow-up:** benchmark pgvector vs Qdrant in Phase 3; write a new ADR if results justify a change.

## Related
- Requirements: FR-004, NFR-010, NFR-018
