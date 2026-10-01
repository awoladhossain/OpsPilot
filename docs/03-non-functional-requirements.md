# 03 — Non-Functional Requirements (NFR)

**Status:** Draft v1 | **Owner:** Awolad | **Last updated:** 2026-09-30

> **How to write:**
> - FR describes **what** the system does; NFR describes **how** it performs: speed, security, cost, reliability.
> - Pattern: `[Quality]: [metric] [target] under [condition].`
> - **All NFRs must include numbers.** Do not just write "Fast", write "p95 < 2s".
> - If exact numbers are unknown, label them as **assumptions** and calibrate them later through benchmarking.
> - In an AI project, most of the real engineering is in NFRs: quality, cost, safety.
>
> **p95 means:** 95 out of 100 requests complete within this time.

> All numbers are **initial targets (assumptions)**.

---

## 1. Performance

| ID | Requirement | Target | How to measure |
|---|---|---|---|
| NFR-001 | Time to first token | p95 < 2 s | Latency histogram (Prometheus) |
| NFR-002 | Full answer time | p95 < 10 s | Same |
| NFR-003 | Document ingestion (10-page PDF) | Ready in < 60 s | Ingestion job duration |

### Latency Budget & Ingestion SLA

```mermaid
flowchart TD
    subgraph LATENCY ["1. Real-Time Chat Latency Budget"]
        REQ["<b>User Hits 'Send'</b><br/>Prompt payload sent over SSE"]
        TTFT["<b>Time to First Token (TTFT)</b><br/>Target: p95 < 2 seconds (NFR-001)"]
        FULL["<b>Full Answer Completion</b><br/>Target: p95 < 10 seconds (NFR-002)"]
        
        REQ -->|"Initial connection & retrieval"| TTFT
        TTFT -->|"Streaming tokens"| FULL
    end

    subgraph ASYNC ["2. Background Ingestion Pipeline"]
        INGEST["<b>10-Page PDF Ingested</b><br/>FR-010 upload triggered"]
        READY["<b>Document Search-Ready</b><br/>Target: < 60 seconds (NFR-003)"]
        
        INGEST -->|"Parse • Chunk • Vectorize"| READY
    end

    style LATENCY fill:#111827,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style ASYNC fill:#111827,stroke:#fbbf24,stroke-width:1px,color:#ffffff

    style REQ fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style TTFT fill:#142918,stroke:#4ade80,stroke-width:2px,color:#ffffff
    style FULL fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style INGEST fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style READY fill:#142918,stroke:#4ade80,stroke-width:2px,color:#ffffff
```

---

## 2. AI Quality

| ID | Requirement | Target | How to measure |
|---|---|---|---|
| NFR-004 | Answers are grounded in sources (faithfulness) | >= 0.85 | Evaluation set (e.g., Ragas) |
| NFR-005 | Correct citation shown | >= 80% | Evaluation set |
| NFR-006 | Out-of-scope questions get "I don't know" | 100% | Evaluation set |
| NFR-007 | Quality does not regress | Evaluation runs on every pull request; PR fails if score drops | CI pipeline |

### RAG Quality Guardrails & Regression CI Gate

```mermaid
flowchart TD
    subgraph METRICS ["1. Core RAG Quality Thresholds"]
        M1["<b>Faithfulness & Groundedness</b><br/>Target: >= 0.85 (NFR-004)<br/>Answers derived solely from docs"]
        M2["<b>Citation Accuracy</b><br/>Target: >= 80% (NFR-005)<br/>Direct links to source pages"]
        M3["<b>Out-of-Scope Rejection</b><br/>Target: 100% (NFR-006)<br/>Answers 'I don't know' without guessing"]
    end

    subgraph CI_GATE ["2. Pull Request Quality Gate (NFR-007)"]
        PR["<b>Developer Opens Pull Request</b><br/>Changes prompt, chunking, or model"]
        EVAL["<b>Automated RAG Evaluation Suite</b><br/>Executes benchmark test questions via Ragas"]
        CHECK{"<b>Eval Score >= Baseline?</b>"}
        PASS["<b>PR Approved & Mergeable</b><br/>No quality regression detected"]
        FAIL["<b>PR Blocked Automatically</b><br/>Regression alert: review prompt/retrieval"]

        PR --> EVAL
        EVAL --> CHECK
        CHECK -- "Yes" --> PASS
        CHECK -- "No" --> FAIL
    end

    METRICS -.->|"Enforced in CI"| EVAL

    style METRICS fill:#111827,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style CI_GATE fill:#111827,stroke:#c084fc,stroke-width:1px,color:#ffffff

    style M1 fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style M2 fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style M3 fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style PR fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style EVAL fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style CHECK fill:#3b2413,stroke:#fbbf24,stroke-width:2px,color:#ffffff
    style PASS fill:#142918,stroke:#4ade80,stroke-width:2px,color:#ffffff
    style FAIL fill:#3f1418,stroke:#ef4444,stroke-width:2px,color:#ffffff
```

---

## 3. Cost

| ID | Requirement | Target | How to measure |
|---|---|---|---|
| NFR-008 | Average LLM cost per question | <= $0.01 (assumption) | Token usage tracking |
| NFR-009 | Monthly spending cap per organization | Configurable; requests stop at cap | Usage table |

### Token Budgeting & Spending Cap Circuit Breaker

```mermaid
flowchart TD
    subgraph PER_REQ ["1. Per-Query Cost Control"]
        Q["<b>User Query Execution</b><br/>Embedding retrieval + Prompt construction"]
        TOK["<b>Token Efficiency Optimization</b><br/>Target: <= $0.01 average per query (NFR-008)"]
        Q --> TOK
    end

    subgraph QUOTA ["2. Monthly Tenant Spending Cap (NFR-009)"]
        LEDGER["<b>Organization Usage Tracker</b><br/>Tracks monthly aggregated token spend"]
        LIMIT{"<b>Monthly Spend >= Org Cap?</b>"}
        
        LEDGER --> LIMIT
        
        ALLOW["<b>Process Query</b><br/>Normal routing to LLM"]
        BLOCK["<b>Circuit Breaker Triggered</b><br/>Friendly quota exceeded notification"]
        
        LIMIT -- "Under Cap" --> ALLOW
        LIMIT -- "Cap Exceeded" --> BLOCK
    end

    TOK --> LEDGER

    style PER_REQ fill:#111827,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style QUOTA fill:#111827,stroke:#fbbf24,stroke-width:1px,color:#ffffff

    style Q fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style TOK fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style LEDGER fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style LIMIT fill:#3b2413,stroke:#fbbf24,stroke-width:2px,color:#ffffff
    style ALLOW fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style BLOCK fill:#3f1418,stroke:#ef4444,stroke-width:2px,color:#ffffff
```

---

## 4. Security and Privacy

| ID | Requirement | Target | How to measure |
|---|---|---|---|
| NFR-010 | Tenant isolation | No cross-organization data access, ever | Automated isolation tests |
| NFR-011 | Authentication and authorization | Hashed passwords, short-lived tokens, role-based access | Security tests |
| NFR-012 | Prompt injection resistance | Text inside documents is never treated as instructions | Attack test set in CI |
| NFR-013 | Rate limiting | Per user and per organization limits | Load test |
| NFR-014 | Privacy | No document content or personal data in logs; organization data can be deleted on request | Log review, deletion test |
| NFR-015 | Dependencies and images | No known critical vulnerabilities | Image and dependency scan in CI |

### Defense-in-Depth Security Framework

```mermaid
flowchart TD
    subgraph L1 ["Layer 1: Perimeter & Access Control"]
        RL["<b>Rate Limiting (NFR-013)</b><br/>Per-user & per-tenant burst protection"]
        AUTH["<b>Auth & JWT (NFR-011)</b><br/>Hashed credentials & short-lived tokens"]
        RL --> AUTH
    end

    subgraph L2 ["Layer 2: AI Safety & Injection Defense"]
        INJ["<b>Prompt Injection Shield (NFR-012)</b><br/>Doc content treated strictly as data, never executable instructions"]
        AUTH --> INJ
    end

    subgraph L3 ["Layer 3: Data Isolation & Privacy"]
        ISO["<b>Tenant Isolation (NFR-010)</b><br/>Zero cross-tenant data leakage via RLS"]
        PRIV["<b>Log Sanitization & Right to Delete (NFR-014)</b><br/>No PII/document text in logs • 1-click full org purge"]
        INJ --> ISO
        ISO --> PRIV
    end

    subgraph L4 ["Layer 4: Supply Chain & Infrastructure"]
        VULN["<b>Vulnerability Scanning (NFR-015)</b><br/>Zero critical CVEs in Docker images & dependencies"]
        PRIV --> VULN
    end

    style L1 fill:#111827,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style L2 fill:#111827,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style L3 fill:#111827,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style L4 fill:#111827,stroke:#c084fc,stroke-width:1px,color:#ffffff

    style RL fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style AUTH fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style INJ fill:#3b2413,stroke:#fbbf24,stroke-width:2px,color:#ffffff
    style ISO fill:#142918,stroke:#4ade80,stroke-width:2px,color:#ffffff
    style PRIV fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style VULN fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
```

---

## 5. Reliability and Scalability

| ID | Requirement | Target | How to measure |
|---|---|---|---|
| NFR-016 | Availability (v1, single server) | 99% monthly | Uptime monitor |
| NFR-017 | LLM provider failure | Fallback model, or clear error message | Failure injection test |
| NFR-018 | v1 load | 10 organizations, 100 concurrent chats, 10,000 chunks per organization | Load test (k6 / Locust) |

### High Availability & Multi-Model Fallback Circuit

```mermaid
flowchart TD
    subgraph RESIL ["1. High Availability & Scalability Targets"]
        UP["<b>System Availability</b><br/>Target: 99% monthly uptime (NFR-016)"]
        LOAD["<b>Concurrency Target (NFR-018)</b><br/>10 organizations • 100 concurrent chats • 10k chunks/org"]
    end

    subgraph FAILOVER ["2. Model Provider Resilience Circuit (NFR-017)"]
        CALL["<b>Dispatch Query to Primary LLM</b>"]
        STATUS{"<b>Provider Response Status?</b>"}
        
        CALL --> STATUS
        
        SUCC["<b>Stream Tokens to Client</b><br/>Successful generation"]
        FALL["<b>Fallback Model Invoked</b><br/>Secondary provider or local Ollama instance"]
        ERR["<b>Graceful Degradation Notice</b><br/>Friendly plain-text error; no system crash"]
        
        STATUS -- "Healthy" --> SUCC
        STATUS -- "Timeout or 5xx" --> FALL
        FALL -->|"If fallback fails"| ERR
    end

    style RESIL fill:#111827,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style FAILOVER fill:#111827,stroke:#fbbf24,stroke-width:1px,color:#ffffff

    style UP fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style LOAD fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style CALL fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style STATUS fill:#3b2413,stroke:#fbbf24,stroke-width:2px,color:#ffffff
    style SUCC fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style FALL fill:#3b2413,stroke:#fbbf24,stroke-width:2px,color:#ffffff
    style ERR fill:#3f1418,stroke:#ef4444,stroke-width:1px,color:#ffffff
```

---

## 6. Observability

| ID | Requirement | Target | How to measure |
|---|---|---|---|
| NFR-019 | Every request traceable | Request ID across all services | Trace view |
| NFR-020 | Metrics and dashboards | Latency, errors, tokens, cost, retrieval quality | Grafana dashboard |
| NFR-021 | Alerts | Alert if error rate > 5% for 5 minutes | Alert rule fires in test |

### Unified Observability & Alerting Pipeline

```mermaid
flowchart TD
    subgraph TRACE ["1. Distributed Tracing (NFR-019)"]
        REQ["<b>Incoming Request</b><br/>Injected with unique Request-ID"]
        GW["<b>API Gateway (NestJS)</b>"]
        AI["<b>AI Service (FastAPI)</b>"]
        DB["<b>Postgres & Vector Store</b>"]
        LLM["<b>LLM Generation</b>"]

        REQ --> GW --> AI --> DB
        AI --> LLM
    end

    subgraph TELEM ["2. Unified Observability & Alerting (NFR-020 & NFR-021)"]
        METRICS["<b>Prometheus Metrics Collector</b><br/>Latency, token consumption, error counts"]
        DASH["<b>Grafana & Langfuse Dashboard</b><br/>Real-time system health & retrieval quality"]
        ALERT{"<b>Error Rate > 5% for 5 mins?</b>"}
        PAGER["<b>Alertmanager Notification</b><br/>Immediate alert to Discord / Slack / Pager"]

        METRICS --> DASH
        METRICS --> ALERT
        ALERT -- "Triggered" --> PAGER
    end

    GW -.->|"Emits metrics"| METRICS
    AI -.->|"Emits metrics"| METRICS

    style TRACE fill:#111827,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style TELEM fill:#111827,stroke:#c084fc,stroke-width:1px,color:#ffffff

    style REQ fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style GW fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style AI fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style DB fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style LLM fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style METRICS fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style DASH fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style ALERT fill:#3b2413,stroke:#fbbf24,stroke-width:2px,color:#ffffff
    style PAGER fill:#3f1418,stroke:#ef4444,stroke-width:2px,color:#ffffff
```

---

## 7. Maintainability and Delivery

| ID | Requirement | Target | How to measure |
|---|---|---|---|
| NFR-022 | CI on every pull request | Lint, type check, tests, evaluation | CI status |
| NFR-023 | Local setup | One command starts the full system | Fresh-machine test |
| NFR-024 | Automated deployment | Merge to main deploys to server | Deployment pipeline |
| NFR-025 | Provider independence | LLM and embedding provider changeable by configuration | Swap test |
| NFR-026 | Test coverage | >= 70% of backend code | Coverage report |

### CI/CD Quality Gates & Automated Delivery

```mermaid
flowchart TD
    subgraph CI ["1. Automated CI Pipeline on Every PR (NFR-022, NFR-026)"]
        CODE["<b>Git Push / Pull Request</b>"]
        LINT["<b>Lint & Format</b><br/>ruff & biome checks"]
        TYPE["<b>Static Analysis</b><br/>mypy strict type validation"]
        TEST["<b>Automated Test Suite</b><br/>Unit & integration tests (>= 70% coverage)"]
        EVAL["<b>AI Regression Suite</b><br/>Ragas evaluation validation"]

        CODE --> LINT --> TYPE --> TEST --> EVAL
    end

    subgraph CD ["2. Automated Continuous Deployment (NFR-024)"]
        MERGE["<b>Merge to 'main' Branch</b>"]
        BUILD["<b>Docker Container Build</b><br/>Trivy security scan"]
        DEPLOY["<b>Deploy to Production Server</b><br/>Zero-downtime container rollout"]

        EVAL -->|"All checks pass"| MERGE
        MERGE --> BUILD --> DEPLOY
    end

    style CI fill:#111827,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style CD fill:#111827,stroke:#4ade80,stroke-width:1px,color:#ffffff

    style CODE fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style LINT fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style TYPE fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style TEST fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style EVAL fill:#271b3d,stroke:#c084fc,stroke-width:2px,color:#ffffff
    style MERGE fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style BUILD fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style DEPLOY fill:#142918,stroke:#4ade80,stroke-width:2px,color:#ffffff
```

---

## 8. Usability

| ID | Requirement | Target | How to measure |
|---|---|---|---|
| NFR-027 | Works on mobile browser | Usable at 360 px width | Manual test |
| NFR-028 | Error messages | Plain language, no stack traces | Manual test |
