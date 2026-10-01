# ADR-0005: Hybrid retrieval (vector + keyword) with reranking

- **Status:** Proposed (reference); validate with the evaluation set in Phase 3
- **Date:** 2026-10-01

---

### Hybrid Retrieval & Reranker Pipeline

```mermaid
flowchart TD
    Q_IN(["<b>User Query</b><br/>e.g., 'What is the policy code for casual leave CL-04?'"])

    subgraph DUAL_RETRIEVAL ["1. Parallel Dual-Track Retrieval"]
        VEC["<b>Dense Semantic Vector Search</b><br/>• pgvector cosine distance<br/>• Captures semantic meaning & intent<br/>• Returns Top 20 candidates"]
        KEY["<b>Sparse Keyword Search (BM25 / FTS)</b><br/>• Postgres tsvector / BM25 match<br/>• Captures exact codes, IDs & numbers<br/>• Returns Top 20 candidates"]
    end

    subgraph FUSION ["2. Reciprocal Rank Fusion (RRF)"]
        RRF["<b>Score Fusion & Deduplication</b><br/>Combines rank positions into unified score<br/>Produces Top 25 candidates"]
    end

    subgraph RERANK ["3. Cross-Encoder Reranker (~300ms)"]
        CROSS["<b>BGE-Reranker Inference</b><br/>Jointly scores (Query, Chunk) pairs<br/>Filters down to Top 3–5 highest signal chunks"]
    end

    subgraph GATE ["4. Relevance Confidence Threshold"]
        SCORE{"<b>Top Score >= Threshold?</b>"}
        
        PASS["<b>Context Passed to LLM</b><br/>Highly relevant citations • Low token waste • Grounded answer"]
        REJECT["<b>Safe Rejection Triggered</b><br/>Honest 'I don't know' • No hallucination • 1-Click escalation"]

        SCORE -- "Yes" --> PASS
        SCORE -- "No" --> REJECT
    end

    Q_IN --> VEC
    Q_IN --> KEY
    VEC --> RRF
    KEY --> RRF
    RRF --> CROSS
    CROSS --> SCORE

    style DUAL_RETRIEVAL fill:#111827,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style FUSION fill:#111827,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style RERANK fill:#111827,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style GATE fill:#111827,stroke:#4ade80,stroke-width:2px,color:#ffffff

    style Q_IN fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style VEC fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style KEY fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style RRF fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style CROSS fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style SCORE fill:#3b2413,stroke:#fbbf24,stroke-width:2px,color:#ffffff
    style PASS fill:#142918,stroke:#4ade80,stroke-width:2px,color:#ffffff
    style REJECT fill:#3f1418,stroke:#ef4444,stroke-width:2px,color:#ffffff
```

---

## Context
Policy documents contain exact terms (policy names, codes, numbers) and paraphrased concepts. Pure vector search misses exact terms; pure keyword search misses meaning. Quality targets: NFR-004..006.

## Options considered
1. **Vector search only.**
2. **Keyword search only.**
3. **Hybrid:** vector and keyword results merged (for example Reciprocal Rank Fusion), then a reranker model on the top candidates.

## Decision
Start with **hybrid retrieval and reranking**, keep a relevance threshold for the "I don't know" path.

## Why
- Covers both exact and semantic matching.
- Reranker improves precision of the few chunks sent to the LLM, reducing tokens and cost.

## Consequences
- **Good:** better citations and fewer wrong answers.
- **Bad / trade-offs:** extra latency (reranking, budget ~300 ms) and complexity.
- **Follow-up:** measure each variant (vector only, hybrid, hybrid + rerank) on the evaluation set; keep the simplest one that meets targets.

## Related
NFR-001, NFR-004, NFR-005, NFR-006, [07 Data model](../07-data-model.md)
