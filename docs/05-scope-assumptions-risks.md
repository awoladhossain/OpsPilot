# 05 — Scope, Assumptions, Constraints, Risks

**Status:** Draft v1 | **Owner:** Awolad | **Last updated:** 2026-09-30

> **How to write:** This file defines the project's **boundaries**: what is included, what is excluded, what we assume, and what could go wrong.
> Include a mitigation (how to reduce it) for every **risk**. This is very useful in interviews.

---

## 1. In Scope (v1)

- Multi-organization (multi-tenant) web application
- Document upload and processing (PDF, DOCX, TXT, MD)
- Question answering with citations
- Escalation to a person
- Assistant actions with user confirmation
- Admin dashboard (usage, cost, knowledge gaps)
- Monitoring, logging, tracing, CI/CD, deployment

## 2. Out of Scope (v1)

- Mobile app, voice
- Billing and payments
- Integrations with Slack / Teams
- Legal or HR decisions made by the system

### Scope Boundary Architecture

```mermaid
flowchart TD
    subgraph IN_SCOPE ["In Scope: OpsPilot v1 Core Capabilities"]
        S1["<b>Multi-Tenant Core:</b> Tenant isolation & RBAC (Admin, Employee)"]
        S2["<b>Document Pipeline:</b> Upload, parse & embed PDF, DOCX, TXT, MD"]
        S3["<b>Grounded RAG:</b> Streaming answers with direct source citations"]
        S4["<b>Safe Fallback:</b> 100% honest 'I don't know' & 1-click human escalation"]
        S5["<b>Assistant Actions:</b> Draft tickets/emails with human confirmation gate"]
        S6["<b>Observability:</b> Metrics, tracing, cost tracking & CI/CD deployment"]
    end

    subgraph OUT_SCOPE ["Out of Scope: Deferred (v2+)"]
        O1["<b>Native Mobile & Voice:</b> iOS/Android apps, speech input/output"]
        O2["<b>Payments & Billing:</b> Stripe integration, paid subscription tiers"]
        O3["<b>Chat Platforms:</b> Slack bot, Microsoft Teams bot"]
        O4["<b>Autonomous Decisions:</b> Binding legal or HR policy determinations"]
    end

    style IN_SCOPE fill:#111827,stroke:#4ade80,stroke-width:2px,color:#ffffff
    style OUT_SCOPE fill:#111827,stroke:#f87171,stroke-width:2px,color:#ffffff

    style S1 fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style S2 fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style S3 fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style S4 fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style S5 fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style S6 fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff

    style O1 fill:#3f1418,stroke:#f87171,stroke-width:1px,color:#ffffff
    style O2 fill:#3f1418,stroke:#f87171,stroke-width:1px,color:#ffffff
    style O3 fill:#3f1418,stroke:#f87171,stroke-width:1px,color:#ffffff
    style O4 fill:#3f1418,stroke:#f87171,stroke-width:1px,color:#ffffff
```

---

## 3. Assumptions

| # | Assumption | How to validate |
|---|---|---|
| A1 | A company has fewer than 500 documents | Test with a large sample |
| A2 | Documents are mostly text (not scanned images) | Test with sample PDFs |
| A3 | Users accept a short answer plus sources | Try with a few real users |
| A4 | An external LLM API is available during development | Check provider limits |

---

## 4. Constraints

- Solo developer, part-time learning project
- Limited budget (low-cost VPS, pay-per-use LLM API)
- Local development laptop has a small GPU (RTX 3050), so only small local models can run
- Learning goal: each technology should be implemented and understood, not only used

### Engineering & Resource Constraints

```mermaid
flowchart TD
    subgraph DEV_ENV ["1. Developer & Capacity Constraints"]
        C1["<b>Solo Engineer:</b> Part-time development with prioritized learning curve"]
        C2["<b>Deep Mastery Focus:</b> Hands-on implementation of each layer (no black-box shortcuts)"]
    end

    subgraph INFRA ["2. Hardware & Budget Boundaries"]
        C3["<b>Host Budget:</b> Low-cost VPS deployment with strict pay-per-use API limits"]
        C4["<b>Local GPU Limit (RTX 3050):</b> Development restricted to small quantized models"]
    end

    style DEV_ENV fill:#111827,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style INFRA fill:#111827,stroke:#fbbf24,stroke-width:1px,color:#ffffff

    style C1 fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style C2 fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style C3 fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style C4 fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
```

---

## 5. Risks

| # | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R1 | Wrong answer (hallucination) | High | High | Answer only from retrieved text, show citations, "I don't know" rule, evaluation in CI |
| R2 | Prompt injection through documents or chat | Medium | High | Treat document text as data, input/output checks, attack test set |
| R3 | One company sees another company's data | Low | Critical | Tenant filter on every query, row-level security, isolation tests |
| R4 | LLM cost grows out of control | Medium | Medium | Usage tracking, per-organization cap, caching, smaller models |
| R5 | LLM provider outage or limit | Medium | Medium | Fallback provider, retry with backoff |
| R6 | Scope grows and project never finishes | High | High | MoSCoW priorities, one phase at a time, demoable milestone per phase |
| R7 | Personal data leaks into logs | Medium | High | Log rules, masking, review |

### Risk Matrix & Mitigation Architecture

```mermaid
flowchart TD
    subgraph SEC_RISKS ["Security & Data Risks"]
        R2["<b>R2: Prompt Injection</b><br/>Documents or chat contain instructions"]
        M2["<b>Mitigation:</b> Treat doc content strictly as data • Sanitize outputs • Attack test suite"]
        R2 --> M2

        R3["<b>R3: Cross-Tenant Data Leak</b><br/>Org A accesses Org B policy data"]
        M3["<b>Mitigation:</b> Postgres Row-Level Security (RLS) • Strict tenant query filters"]
        R3 --> M3

        R7["<b>R7: PII Leak in Logs</b><br/>Sensitive personal data exposed in traces"]
        M7["<b>Mitigation:</b> Structlog masking • Zero document text in logging streams"]
        R7 --> M7
    end

    subgraph AI_RISKS ["AI Quality & Operational Risks"]
        R1["<b>R1: Hallucinations</b><br/>Model invents nonexistent policy"]
        M1["<b>Mitigation:</b> Answer strictly from citations • 'I don't know' rule • Ragas PR gates"]
        R1 --> M1

        R4["<b>R4: Runaway LLM Spend</b><br/>Token consumption explodes"]
        M4["<b>Mitigation:</b> Organization spending caps • Semantic caching • Smaller router models"]
        R4 --> M4

        R5["<b>R5: Provider Outage</b><br/>Upstream API rate limits or down"]
        M5["<b>Mitigation:</b> Exponential retry backoff • Secondary fallback model"]
        R5 --> M5

        R6["<b>R6: Scope Creep</b><br/>Project becomes overwhelmed"]
        M6["<b>Mitigation:</b> Strict MoSCoW prioritization • Demoable phase-by-phase delivery"]
        R6 --> M6
    end

    style SEC_RISKS fill:#111827,stroke:#f87171,stroke-width:1px,color:#ffffff
    style AI_RISKS fill:#111827,stroke:#fbbf24,stroke-width:1px,color:#ffffff

    style R2 fill:#3f1418,stroke:#f87171,stroke-width:1px,color:#ffffff
    style M2 fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style R3 fill:#3f1418,stroke:#ef4444,stroke-width:2px,color:#ffffff
    style M3 fill:#142918,stroke:#4ade80,stroke-width:2px,color:#ffffff
    style R7 fill:#3f1418,stroke:#f87171,stroke-width:1px,color:#ffffff
    style M7 fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff

    style R1 fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style M1 fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style R4 fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style M4 fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style R5 fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style M5 fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style R6 fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style M6 fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
```

---

## 6. Open Questions

- [ ] Which LLM provider(s) for v1?
- [ ] Hosting: which VPS and region?
- [ ] Which evaluation dataset will be used (write our own questions from sample policy documents)?

---

## 7. Project Glossary

| Term | Meaning |
|---|---|
| **Tenant / Organization** | One customer company and its data |
| **Document** | A file or web page uploaded by an admin |
| **Chunk** | A small piece of a document used for searching |
| **Embedding** | Numbers that represent the meaning of a text |
| **RAG** | Retrieval-Augmented Generation: find relevant text first, then let the LLM answer from it |
| **Citation** | Link from an answer to its source |
| **Escalation** | Sending a question to a human with context |

### Conceptual Relationships & Information Pipeline

```mermaid
flowchart TD
    TENANT["<b>1. Tenant / Organization</b><br/>Customer boundary: Org users & data"]
    DOC["<b>2. Document</b><br/>Policy PDF, DOCX, TXT or Markdown file"]
    CHUNK["<b>3. Chunks</b><br/>Segmented snippets (~500 tokens) with metadata"]
    EMBED["<b>4. Embeddings</b><br/>Vector representations stored in pgvector / Qdrant"]
    RAG["<b>5. RAG Pipeline</b><br/>Retrieves top chunks + constructs grounded context for LLM"]
    ANS["<b>6. Answer & Citation</b><br/>Grounded response with verified page source link"]
    ESC["<b>7. Escalation</b><br/>Human handoff if query is out-of-scope or critical"]

    TENANT --> DOC
    DOC --> CHUNK
    CHUNK --> EMBED
    EMBED --> RAG
    RAG --> ANS
    RAG -->|"No document match"| ESC

    style TENANT fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style DOC fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style CHUNK fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style EMBED fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style RAG fill:#142918,stroke:#4ade80,stroke-width:2px,color:#ffffff
    style ANS fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style ESC fill:#3f1418,stroke:#f87171,stroke-width:1px,color:#ffffff
```
