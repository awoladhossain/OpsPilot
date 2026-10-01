# ADR-XXXX: [Short title of the decision]

- **Status:** Proposed | Accepted | Superseded by ADR-YYYY
- **Date:** YYYY-MM-DD
- **Deciders:** [names]

> **How to write:** An ADR (Architecture Decision Record) is a concise document capturing "why we made this decision". One decision = one file.
> Keep it under 1 page. In technical interviews, this is your strongest evidence of sound engineering judgment.
> When to write: Whenever you choose one option from 2+ alternatives (database, framework, vector DB, message queue, etc.).

---

### ADR Decision Framework & Lifecycle

```mermaid
flowchart TD
    subgraph STAGE_1 ["1. Context & Architectural Challenge"]
        PROB["<b>Engineering Problem & Constraints</b><br/>Why does a decision need to be made now?<br/>Linked to FRs and NFRs"]
    end

    subgraph STAGE_2 ["2. Evaluation of Alternatives"]
        OP_A["<b>Option A: Candidate 1</b><br/>Pros, cons, operational complexity"]
        OP_B["<b>Option B: Candidate 2</b><br/>Performance, cost, developer velocity"]
        OP_C["<b>Option C: Candidate 3</b><br/>Ecosystem maturity, maintenance"]
    end

    subgraph STAGE_3 ["3. Decision & Trade-off Analysis"]
        DEC["<b>Chosen Solution ('The Decision')</b><br/>Selected based on concrete technical criteria"]
        WHY["<b>Technical Rationale ('Why')</b><br/>Justified against project requirements"]
        DEC --> WHY
    end

    subgraph STAGE_4 ["4. Impact & Consequences"]
        GOOD["<b>Positive Gains (+)</b><br/>Immediate benefits & capabilities enabled"]
        BAD["<b>Accepted Trade-offs (-)</b><br/>Known friction or complexity accepted"]
        NEXT["<b>Actionable Follow-ups</b><br/>Benchmarking triggers, migration spikes"]
    end

    subgraph LIFECYCLE ["5. ADR Status Lifecycle"]
        ST_PROP["<b>Status: Proposed</b><br/>Under team / PR review"]
        ST_ACC["<b>Status: Accepted</b><br/>Active architecture standard"]
        ST_SUP["<b>Status: Superseded</b><br/>Replaced by future ADR-YYYY"]

        ST_PROP -->|"Consensus reached"| ST_ACC
        ST_ACC -->|"Architecture evolves"| ST_SUP
    end

    PROB --> OP_A & OP_B & OP_C
    OP_A & OP_B & OP_C --> DEC
    WHY --> GOOD & BAD & NEXT

    style STAGE_1 fill:#111827,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style STAGE_2 fill:#111827,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style STAGE_3 fill:#111827,stroke:#4ade80,stroke-width:2px,color:#ffffff
    style STAGE_4 fill:#111827,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style LIFECYCLE fill:#111827,stroke:#64748b,stroke-width:1px,color:#ffffff

    style PROB fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style OP_A fill:#1e293b,stroke:#94a3b8,stroke-width:1px,color:#ffffff
    style OP_B fill:#1e293b,stroke:#94a3b8,stroke-width:1px,color:#ffffff
    style OP_C fill:#1e293b,stroke:#94a3b8,stroke-width:1px,color:#ffffff
    style DEC fill:#142918,stroke:#4ade80,stroke-width:2px,color:#ffffff
    style WHY fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style GOOD fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style BAD fill:#3f1418,stroke:#f87171,stroke-width:1px,color:#ffffff
    style NEXT fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style ST_PROP fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style ST_ACC fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style ST_SUP fill:#3f1418,stroke:#f87171,stroke-width:1px,color:#ffffff
```

---

## Context
What is the problem? What are the constraints? Why does this decision need to be made now? (2-5 lines)

## Options considered
1. **Option A**: short description
2. **Option B**: short description
3. **Option C**: short description

## Decision
We will use **[option]**.

## Why
- Reason 1 (you can link to project requirements, e.g., NFR-010)
- Reason 2

## Consequences
- **Good:**
- **Bad / trade-offs:**
- **Follow-up:** (any required action, e.g., "benchmark at 100k chunks, revisit if slow")

## Related
- Requirements: FR-xxx, NFR-xxx
- Other ADRs:
