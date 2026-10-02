# 13 — Roadmap and Milestones

**Status:** Approved v1 (reference) | **Last updated:** 2026-10-01
**Inputs:** [02 FR](../01-product/02-functional-requirements.md), [06 Architecture](../02-system-design/reference-solution/06-architecture.md), [12 Traceability](../02-system-design/reference-solution/12-traceability-and-design-review.md)

> **Commercial planning update:** Use the [commercial roadmap addendum](../01-product/21-commercial-roadmap-addendum.md) for customer-validation gates and the Phase 8 pilot-readiness sequence. This roadmap describes the engineering phases 0–7; the addendum extends it with the pilot track.

---

## 1. Vision and Final Demo

**Vision:** A company uploads its documents; employees ask questions and get cited answers, and can escalate to a person when the answer is missing.

**Final demo:** live URL with HTTPS, login as admin and employee, upload a policy PDF, ask a question and see citations, see "I don't know" for an out-of-scope question, escalate by email, confirm an agent action, show Grafana dashboards and an evaluation report.

---

## 2. Planning Assumptions

| Assumption | Value | If wrong |
|---|---|---|
| Focused weekly capacity | **10 hours** | Multiply all dates by (10 / your hours) |
| Start | Week 1 begins Sunday 4 Oct 2026 | Shift all dates |
| Estimates include learning time | Yes (1.5–2.0x multiplier already factored into new tech) | Re-calibrate after Phase 0 |
| Contingency | +20% on top of base estimate | Cut scope (section 6), not quality |
| Tools | Python backend (FastAPI), Postgres, Redis, SeaweedFS for local storage, Next.js UI | Changes need an ADR |
| Office work | Can reduce capacity at busy times | Use the buffer; never skip the weekly review |

---

## 3. Phased Delivery Roadmap & Schedule

```mermaid
flowchart TD
    subgraph PHASE_FOUNDATION ["Foundation & Core Architecture (Weeks 1 - 5)"]
        P0["<b>Phase 0: Setup & Infrastructure</b><br/>11h (Weeks 1-2) • Docker Compose, CI skeleton, /health/ready"]
        P1["<b>Phase 1: Multi-Tenant Foundation</b><br/>31h (Weeks 2-5) • Org registration, JWT, RLS spike, SSE streaming"]
        P0 --> P1
    end

    subgraph PHASE_RAG ["Grounded Knowledge & Retrieval (Weeks 5 - 14)"]
        P2["<b>Phase 2: Basic RAG Engine</b><br/>35.5h (Weeks 5-10) • Async PDF ingestion, pgvector HNSW, citations, phone UI"]
        P3["<b>Phase 3: Retrieval Quality & Evaluation</b><br/>34h (Weeks 10-14) • 50-q eval set, hybrid search, rerank, Ragas CI gate"]
        P1 --> P2 --> P3
    end

    subgraph PHASE_FEATURES ["Agents & Hardening (Weeks 14 - 22)"]
        P4["<b>Phase 4: Agents & Human Escalation</b><br/>31h (Weeks 14-18) • HITL propose-confirm, email tickets, MCP tool"]
        P5["<b>Phase 5: Production Hardening</b><br/>33h (Weeks 18-22) • Redis rate limits, caching, fallback chain, admin dashboards"]
        P3 --> P4
        P3 --> P5
        P4 --> P5
    end

    subgraph PHASE_PRODUCTION ["Operations & Advanced Depth (Weeks 22 - 30)"]
        P6["<b>Phase 6: Observability & Production Deploy</b><br/>32h (Weeks 22-25) • Live HTTPS, Grafana stack, alert drills, auto-deploy"]
        P7["<b>Phase 7: Advanced Depth (Stretch)</b><br/>37h (Weeks 25-30) • Model server extraction, routing, fine-tune analysis"]
        P5 --> P6 --> P7
    end

    style PHASE_FOUNDATION fill:#111827,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style PHASE_RAG fill:#111827,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style PHASE_FEATURES fill:#111827,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style PHASE_PRODUCTION fill:#111827,stroke:#c084fc,stroke-width:1px,color:#ffffff

    style P0 fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style P1 fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style P2 fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style P3 fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style P4 fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style P5 fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style P6 fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style P7 fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
```

| Phase | Name | Base hours | Planned weeks | Start (week starts) | Demo |
|---|---|---|---|---|---|
| 0 | Setup | 11 | 1-2 | 4 Oct 2026 | `docker compose up` + green CI |
| 1 | Foundation: tenancy, auth, LLM streaming | 31 | 2-5 | 11 Oct | Login, chat streams, isolation test |
| 2 | Basic RAG | 35.5 | 5-10 | 1 Nov | Upload PDF, cited answer, minimal UI |
| 3 | Better RAG and evaluation | 34 | 10-14 | 6 Dec | Score table comparing variants |
| 4 | Agents and escalation | 31 | 14-18 | 3 Jan 2027 | Escalate, propose and confirm action, MCP tool |
| 5 | Production hardening and admin | 33 | 18-22 | 31 Jan | Rate limits, cache, fallback, dashboard, load test |
| 6 | Observability, CI/CD, deployment | 32 | 22-25 | 28 Feb | Live URL, dashboards, alerts |
| 7 | Advanced (stretch) | 37 | 25-30 | 21 Mar | Model server, routing, fine-tune report, write-up |
| | **Total** | **244.5** | | | |

Base total 244.5 h, with 20% contingency about 293 h, about 29 weeks at 10 h/week. **Phases 0-6 (the complete product) finish around week 25 (late March 2027).** Phase 7 is the advanced stretch and can continue into April. Ramadan and Eid (roughly February to March 2027) and office deadlines may slow you down, which is why the buffer exists.

---

## 4. Phases in Detail

### Phase 0: Setup (11 h)
- **Goal:** Working development environment, repository, and CI skeleton.
- **Demo:** One command starts the stack; a pull request runs lint, type check, tests.
- **Exit criteria:** [ ] Repo with docs imported [ ] `docker compose up` healthy [ ] `/health/ready` tested [ ] CI green and blocking [ ] Board and Phase 1 issues created
- **Learning outcomes:** Containers, compose, project structure, CI basics, Fedora specifics (SELinux labels, Docker vs Podman).

### Phase 1: Foundation (31 h)
- **Goal:** Walking skeleton: secure multi-tenant backend that streams an LLM answer.
- **Demo:** Register organization, log in, chat answer streams token by token, usage recorded.
- **Exit criteria:** [ ] Isolation test passes in CI [ ] Refresh rotation tested [ ] RBAC tested [ ] SSE chat saves messages and usage [ ] Token cap works [ ] ADR-0002 updated with spike result
- **Learning outcomes:** async Python, SQLAlchemy and Alembic, RLS, JWT, SSE, LLM API basics, token accounting.
- **Spike:** RLS with connection pooling (P1-03).

### Phase 2: Basic RAG (35.5 h)
- **Goal:** Upload documents and get grounded, cited answers.
- **Demo:** Upload a leave-policy PDF, ask "How many casual leave days?", see answer with citation; ask something unrelated, see "I don't know".
- **Exit criteria:** [ ] Ingestion runs in worker with status and retries [ ] Retrieval filtered by tenant and role [ ] Citations saved and openable [ ] "I don't know" path works on 10 manual questions [ ] Minimal UI works on a phone width [ ] Phase retro written
- **Learning outcomes:** Parsing, chunking, embeddings, pgvector and HNSW, Celery, idempotency, grounded prompting.

### Phase 3: Better RAG and evaluation (34 h)
- **Goal:** Measure quality, then improve it with evidence.
- **Demo:** Table comparing vector only, hybrid, hybrid + rerank on the same question set.
- **Exit criteria:** [ ] 50-question evaluation set (answerable, multi-document, unanswerable, adversarial) [ ] Metrics reported (retrieval hit rate, MRR, faithfulness, citation correctness) [ ] Hybrid and rerank compared [ ] Threshold tuned [ ] pgvector vs Qdrant benchmark recorded in ADR-0006 [ ] Evaluation runs in CI with a gate [ ] Role-based access (FR-014) tested
- **Learning outcomes:** Evaluation design, retrieval metrics, hybrid search and RRF, rerankers, LLM-as-judge limits, benchmarking.

### Phase 4: Agents and escalation (31 h)
- **Goal:** The assistant can propose actions safely and escalate to a person.
- **Demo:** "Create a ticket for my laptop issue" produces a draft, user confirms; "I don't know" answer offers escalation and the contact gets an email.
- **Exit criteria:** [ ] Escalation with idempotency and email retry [ ] Pending actions with confirm, reject, expiry [ ] LangGraph agent with propose-only tools [ ] MCP server with read-only search tool, tested with a client [ ] Prompt injection test set passes [ ] Agent tool-selection evaluation recorded
- **Learning outcomes:** Tool calling, agent graphs, human-in-the-loop, prompt injection, MCP.

### Phase 5: Production hardening and admin (33 h)
- **Goal:** Make it behave under load and failure; give admins visibility.
- **Demo:** Load test report; kill the LLM provider (fake) and see fallback; admin dashboard with usage, gaps, feedback.
- **Exit criteria:** [ ] Rate limiting [ ] Caching with measured hit rate [ ] Fallback and circuit breaker tested [ ] PII masked in logs [ ] Admin APIs and pages [ ] Feedback endpoint [ ] URL ingestion [ ] Idempotency middleware [ ] k6 baseline and one bottleneck fixed
- **Learning outcomes:** Rate limiting algorithms, caching, resilience patterns, load testing.

### Phase 6: Observability, CI/CD, deployment (32 h)
- **Goal:** Operate it like a real service.
- **Demo:** Live URL; Grafana dashboards; a forced error triggers an alert; a merge to main deploys automatically; restore drill done.
- **Exit criteria:** [ ] OpenTelemetry traces across API, queue, worker [ ] Prometheus metrics and four dashboards [ ] Logs in Loki via Grafana Alloy [ ] Langfuse traces [ ] Alerts to Telegram or Discord [ ] Image scan and dependency scan in CI [ ] Auto deploy with smoke test and rollback [ ] Backup and restore tested
- **Learning outcomes:** Observability pillars, metric cardinality, tracing, SLO thinking, deployment, backups.

### Phase 7: Advanced (stretch, 37 h)
- **Goal:** Depth projects that differentiate you.
- **Demo:** Model server extraction with benchmark; routing results; fine-tuning comparison; blog post and demo video.
- **Exit criteria:** [ ] Model server extracted behind the same interface [ ] Routing evaluated on cost and quality [ ] Small fine-tune compared against baseline (check VRAM first) [ ] Bengali experiment documented [ ] Final load test [ ] Write-up, README, demo video
- **Learning outcomes:** Service extraction, model serving, routing, parameter-efficient fine-tuning, multilingual retrieval, technical writing.

---

## 5. Phase Dependency Graph

```mermaid
flowchart TD
    P0["<b>Phase 0: Setup</b><br/>Docker, CI, base repo"]
    P1["<b>Phase 1: Foundation</b><br/>Tenancy, auth, LLM stream"]
    P2["<b>Phase 2: Basic RAG</b><br/>Ingestion, pgvector, UI"]
    P3["<b>Phase 3: Eval & Rerank</b><br/>Quality benchmarking"]
    P4["<b>Phase 4: Agents</b><br/>HITL & Escalation"]
    P5["<b>Phase 5: Hardening</b><br/>Rate limits, cache, admin"]
    P6["<b>Phase 6: Observability & CD</b><br/>Production live demo"]
    P7["<b>Phase 7: Advanced</b><br/>Stretch models & routing"]

    P0 --> P1
    P1 --> P2
    P2 --> P3
    P3 --> P4
    P3 --> P5
    P4 --> P5
    P5 --> P6
    P6 --> P7

    style P0 fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style P1 fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style P2 fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style P3 fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style P4 fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style P5 fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style P6 fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style P7 fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
```

Observability basics (structured logs, request IDs) start in Phase 1, so Phase 6 builds on existing signals.

---

## 6. Scope Management: Critical Path vs. De-scoping Hierarchy

```mermaid
flowchart TD
    subgraph NEVER_CUT ["Non-Negotiable Core (Never Compromise)"]
        NC1["<b>Multi-Tenant Isolation Tests</b> (NFR-010, RLS)"]
        NC2["<b>Retrieval Evaluation Suite</b> (NFR-007, Golden set)"]
        NC3["<b>'I Don't Know' Fallback Behavior</b> (Hallucination defense)"]
        NC4["<b>Propose-Only Agent Tooling</b> (Human-in-the-loop safety)"]
        NC5["<b>Automated CI Gates</b> (Lint, Type check, Tests)"]
    end

    subgraph DE_SCOPE ["De-scoping Hierarchy (Cut in this Order if Behind)"]
        DS1["<b>1. Phase 7 Items:</b> Model server, Fine-tune, Multilingual"]
        DS2["<b>2. Semantic Caching:</b> Keep exact Redis cache only"]
        DS3["<b>3. Admin UI Polish:</b> Keep pure REST APIs"]
        DS4["<b>4. URL Ingestion:</b> Focus exclusively on PDF upload"]
        DS5["<b>5. Structured Data Tool:</b> Drop non-document querying"]
        DS6["<b>6. Langfuse Tracing:</b> Keep Prometheus metrics & Loki logs"]
        DS7["<b>7. Bengali Keyword Search:</b> Rely on multilingual embeddings"]
        
        DS1 --> DS2 --> DS3 --> DS4 --> DS5 --> DS6 --> DS7
    end

    style NEVER_CUT fill:#111827,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style DE_SCOPE fill:#111827,stroke:#f87171,stroke-width:1px,color:#ffffff

    style NC1 fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style NC2 fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style NC3 fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style NC4 fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style NC5 fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff

    style DS1 fill:#3f1418,stroke:#f87171,stroke-width:1px,color:#ffffff
    style DS2 fill:#3f1418,stroke:#f87171,stroke-width:1px,color:#ffffff
    style DS3 fill:#3f1418,stroke:#f87171,stroke-width:1px,color:#ffffff
    style DS4 fill:#3f1418,stroke:#f87171,stroke-width:1px,color:#ffffff
    style DS5 fill:#3f1418,stroke:#f87171,stroke-width:1px,color:#ffffff
    style DS6 fill:#3f1418,stroke:#f87171,stroke-width:1px,color:#ffffff
    style DS7 fill:#3f1418,stroke:#f87171,stroke-width:1px,color:#ffffff
```

**Never cut:** tenant isolation tests, evaluation set, "I don't know" behavior, propose-only agent, CI.

---

## 7. Re-Plan Triggers

- Phase takes more than 1.5x its estimate: stop, find out why, update remaining estimates.
- A spike shows a design assumption is wrong: write a new ADR, update affected docs.
- Two weeks without progress: reduce scope of the current phase, do not extend it.

---

## 8. Phase Done Checklist (Every Phase)

- [ ] Demo works and is recorded (2-3 minutes)
- [ ] Exit criteria all checked
- [ ] Docs and ADRs updated
- [ ] Concept check done (`16-learning-checkpoints.md`)
- [ ] Retro written (what worked, what did not, what to change)
- [ ] Git tag created (for example `v0.2.0`)
- [ ] Next phase tasks broken down and estimated
