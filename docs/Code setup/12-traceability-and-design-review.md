# 12 — Traceability Matrix and Design Review

**Status:** Approved v2 (reference) | **Last updated:** 2026-10-01

Purpose: prove that every requirement is covered by the design and assigned to a phase, and record the review of the design itself.

---

## 1. Functional Requirements Traceability

```mermaid
flowchart TD
    subgraph REQS ["Functional Requirements (User Demands)"]
        FR_AUTH["<b>Identity & Tenancy (FR-001..004)</b><br/>Org registration, RBAC, JWT auth, RLS isolation"]
        FR_DOCS["<b>Knowledge Ingestion (FR-010..014)</b><br/>PDF upload, async parsing, chunking, role filters"]
        FR_RAG["<b>Streaming Grounded RAG (FR-020..024)</b><br/>SSE token streaming, verbatim citations, fallback threshold"]
        FR_ESC["<b>Escalation & Actions (FR-030..042)</b><br/>1-click human tickets, HITL action proposals, MCP tool"]
        FR_OPS["<b>Admin & Observability (FR-050..052)</b><br/>Usage metrics, token accounting, knowledge gaps"]
    end

    subgraph MODULES ["Architectural Modules (In-Process Monolith)"]
        M_ID["<b>identity & core</b><br/>tenants, users, refresh_tokens"]
        M_DOC["<b>documents & ingestion</b><br/>documents, document_chunks, Celery worker"]
        M_CHAT["<b>chat, retrieval & llm</b><br/>conversations, messages, citations, pgvector"]
        M_ESC["<b>escalation & agent</b><br/>escalations, pending_actions, SMTP"]
        M_ADM["<b>admin & usage</b><br/>usage_events, feedback, telemetry"]
    end

    subgraph PHASES ["Implementation Milestones"]
        P1["<b>Phase 1: Foundation</b><br/>Walking skeleton, Auth, SSE stream"]
        P2["<b>Phase 2: Basic RAG</b><br/>Ingestion, pgvector, UI"]
        P3["<b>Phase 3: Eval & Rerank</b><br/>Evaluation set, Cross-encoder, Tuning"]
        P4["<b>Phase 4: Agents & Escalate</b><br/>HITL confirm, Escalation tickets, MCP"]
        P5["<b>Phase 5: Hardening</b><br/>Rate limits, Cache, Admin dashboards"]
    end

    FR_AUTH --> M_ID --> P1
    FR_DOCS --> M_DOC --> P2
    FR_RAG --> M_CHAT --> P2
    M_CHAT -.->|"Quality & Evaluation Gate"| P3
    FR_ESC --> M_ESC --> P4
    FR_OPS --> M_ADM --> P5

    style REQS fill:#111827,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style MODULES fill:#111827,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style PHASES fill:#111827,stroke:#4ade80,stroke-width:1px,color:#ffffff

    style FR_AUTH fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style FR_DOCS fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style FR_RAG fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style FR_ESC fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style FR_OPS fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff

    style M_ID fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style M_DOC fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style M_CHAT fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style M_ESC fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style M_ADM fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff

    style P1 fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style P2 fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style P3 fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style P4 fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style P5 fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
```

| FR | Module(s) | Tables | Endpoint(s) | Phase |
|---|---|---|---|---|
| FR-001 | identity | tenants, users | POST /auth/register-organization | 1 |
| FR-002 | identity | users, invitations | POST /users/invitations, POST /auth/accept-invitation, GET /users | 1 |
| FR-003 | identity | users, refresh_tokens | /auth/login, /refresh, /logout | 1 |
| FR-004 | core, identity | all (RLS) | all | 1 |
| FR-010 | documents | documents | POST /documents | 2 |
| FR-011 | documents, ingestion | documents | POST /documents (url) | 5 (Should) |
| FR-012 | documents, ingestion | documents, ingestion_jobs | GET /documents | 2 |
| FR-013 | documents, ingestion | documents, document_chunks | DELETE /documents/{id} | 2 |
| FR-014 | documents, retrieval | documents, document_chunks | PATCH /documents/{id} | 3 |
| FR-020 | chat, retrieval, llm | conversations, messages | POST /conversations/{id}/messages | 2 |
| FR-021 | chat | none | same (SSE) | 1 |
| FR-022 | chat, retrieval | citations | SSE citation events, GET /citations/{id}/source | 2 |
| FR-023 | chat, retrieval | messages | same | 2, tuned in 3 |
| FR-024 | chat | conversations, messages | GET /conversations, GET .../messages | 1 |
| FR-025 | chat | feedback | POST /messages/{id}/feedback | 5 |
| FR-026 | retrieval, llm | none | same as FR-020 | 7 (Could) |
| FR-030 | escalation | escalations | POST /escalations | 4 |
| FR-031 | escalation | escalation_contacts | /admin/escalation-contacts | 4 |
| FR-032 | escalation | escalations | GET, PATCH /escalations | 4 |
| FR-040 | agent | pending_actions | SSE action_proposed | 4 |
| FR-041 | agent | pending_actions | POST /actions/{id}/confirm, /reject | 4 |
| FR-042 | agent | none (read-only role) | SSE | 4 (Could) |
| FR-050 | usage, admin | usage_events | GET /admin/usage | 5 |
| FR-051 | admin, chat | messages | GET /admin/knowledge-gaps | 5 |
| FR-052 | admin, chat | feedback | GET /admin/feedback | 5 |

---

## 2. Non-Functional Requirements Verification

```mermaid
flowchart TD
    subgraph PILLARS ["Quality & Architectural Drivers"]
        NFR_PERF["<b>Performance & Responsiveness</b><br/>NFR-001..003: Streaming TTFT &lt; 2s, Async ingestion"]
        NFR_QUAL["<b>RAG Quality & Precision</b><br/>NFR-004..007: Faithfulness, Hit rate &gt; 85%, Zero hallucinations"]
        NFR_SEC["<b>Tenancy & Data Security</b><br/>NFR-010..014: 4-layer RLS, Prompt injection defense, PII masking"]
        NFR_REL["<b>Reliability & Observability</b><br/>NFR-016..026: Provider fallback, OpenTelemetry, Health checks"]
    end

    subgraph CONTROLS ["Architectural Countermeasures"]
        C_STREAM["SSE Progressive Chunks + In-Memory Rerank"]
        C_EVAL["Automated Evaluation Harness + Ragas CI Gate"]
        C_RLS["Postgres RLS Session Variables + Scope Assertions"]
        C_RESIL["Tenacity Retries + Redis Rate Limiter + Circuit Breaker"]
    end

    subgraph PROBES ["Automated Verification Gates"]
        V_LOAD["k6 Load Tests & Latency Histograms"]
        V_CI["GitHub Actions CI Golden Dataset Test"]
        V_ISOL["Multi-Tenant Isolation Integration Tests"]
        V_MON["Prometheus Alerts + Synthetic Error Drills"]
    end

    NFR_PERF --> C_STREAM --> V_LOAD
    NFR_QUAL --> C_EVAL --> V_CI
    NFR_SEC --> C_RLS --> V_ISOL
    NFR_REL --> C_RESIL --> V_MON

    style PILLARS fill:#111827,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style CONTROLS fill:#111827,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style PROBES fill:#111827,stroke:#4ade80,stroke-width:1px,color:#ffffff

    style NFR_PERF fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style NFR_QUAL fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style NFR_SEC fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style NFR_REL fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff

    style C_STREAM fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style C_EVAL fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style C_RLS fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style C_RESIL fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff

    style V_LOAD fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style V_CI fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style V_ISOL fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style V_MON fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
```

| NFR | Design response | Where | Verified by | Phase |
|---|---|---|---|---|
| NFR-001, 002 | Streaming, latency budget, limited rerank | 06, 09 | Latency histogram, load test | 5-6 |
| NFR-003 | Async worker, batch embeddings | 09 Flow 1 | Ingestion duration metric | 2 |
| NFR-004..006 | Hybrid retrieval, threshold, evaluation set | ADR-0005 | Evaluation harness | 3 |
| NFR-007 | Evaluation in CI with gate | 11 | CI | 3 |
| NFR-008, 009 | Usage events, caps, caching | 07, 08 | Usage dashboard | 1, 5 |
| NFR-010 | 4-layer isolation, RLS | 10, ADR-0002 | Isolation tests | 1 |
| NFR-011 | JWT, rotation, RBAC | 10, ADR-0008 | Security tests | 1 |
| NFR-012 | Data-not-instructions, propose-only agent | 10, ADR-0009 | Attack test set | 4 |
| NFR-013 | Redis rate limiting | 08 | Load test | 5 |
| NFR-014 | Log masking, tenant deletion | 10 | Log review, deletion test | 5 |
| NFR-015 | Image, dependency, secret scans | 11 | CI | 6 |
| NFR-016, 017 | Fallback chain, health checks | 09, ADR-0007 | Failure injection | 5 |
| NFR-018 | Single-server sizing | 06 | k6 / Locust | 5, 7 |
| NFR-019..021 | OpenTelemetry, metrics, alerts | 11 | Dashboards, alert test | 6 |
| NFR-022..026 | CI pipeline, compose, deploy, coverage | 11 | CI | 0, 6 |
| NFR-027, 028 | Thin responsive UI, error format | 08 | Manual test | 2, 5 |

---

## 3. Story Walkthrough (Design Review Step 1)

| Story | Path through design | Gap? |
|---|---|---|
| US-001 Ask | chat > retrieval > llm; SSE | None |
| US-002 Sources | citations table, source endpoint | None |
| US-003 I don't know | retrieval threshold, fixed answer, escalation hint | Threshold tuned in Phase 3 |
| US-004 History | conversations, messages | None |
| US-005 Rate | feedback | None |
| US-010 Escalate | escalation module, email job | Email provider choice open |
| US-020 Upload | documents, queue, worker | None |
| US-021 Delete | documents, chunk cleanup | None |
| US-022 Access control | allowed_roles on documents and chunks, RLS | Role change must update chunks (re-sync on PATCH) |
| US-030 Gaps | admin, messages status | Need an explicit "no answer" flag on messages |
| US-031 Usage | usage_events | None |
| US-040 Setup | identity | Login lookup before tenant known (see 07) |

**Gaps found and fixed in design:**
1. PATCH of allowed roles must update chunk roles in the same transaction.
2. Add `answered boolean` (or reason code) to `messages` so knowledge gaps are queryable.
3. Login lookup exception for RLS.

---

## 4. Failure Scenarios and Resilience Matrix

```mermaid
flowchart TD
    subgraph FAILURES ["Fault Injections & Disruption Scenarios"]
        FL_LLM["<b>LLM Provider Outage / Rate Limit</b><br/>Primary model API returns 429/500/timeout"]
        FL_WRK["<b>Celery Worker Node Crash</b><br/>Process killed mid-document embedding"]
        FL_RDS["<b>Redis Broker Restart / Eviction</b><br/>In-flight queue state lost or rate limits reset"]
        FL_DB["<b>DB Connection Pool Exhaustion</b><br/>Sudden burst saturates available pool connections"]
        FL_INJ["<b>Prompt Injection Payload in PDF</b><br/>Adversarial instructions embedded in uploaded doc"]
    end

    subgraph RESILIENCE ["Architectural Countermeasures & Recovery"]
        R_LLM["<b>Automated Fallback Chain</b><br/>Retry with backoff $\rightarrow$ switch to backup model $\rightarrow$ graceful error event"]
        R_WRK["<b>Idempotent Chunk Processing</b><br/>Message redelivered via Redis visibility timeout; chunk upsert prevents duplicates"]
        R_RDS["<b>Periodic Reconciliation Sweep</b><br/>Scheduled background task re-enqueues orphaned 'uploaded' documents"]
        R_DB["<b>Fast-Fail & Circuit Breaker</b><br/>Queue connection timeouts return HTTP 503 Service Unavailable + Prometheus alert"]
        R_INJ["<b>Strict Data Demarcation</b><br/>Parser strips executable scripts; RAG prompt encloses chunks in data tags"]
    end

    FL_LLM --> R_LLM
    FL_WRK --> R_WRK
    FL_RDS --> R_RDS
    FL_DB --> R_DB
    FL_INJ --> R_INJ

    style FAILURES fill:#111827,stroke:#f87171,stroke-width:1px,color:#ffffff
    style RESILIENCE fill:#111827,stroke:#4ade80,stroke-width:1px,color:#ffffff

    style FL_LLM fill:#3f1418,stroke:#f87171,stroke-width:1px,color:#ffffff
    style FL_WRK fill:#3f1418,stroke:#f87171,stroke-width:1px,color:#ffffff
    style FL_RDS fill:#3f1418,stroke:#f87171,stroke-width:1px,color:#ffffff
    style FL_DB fill:#3f1418,stroke:#f87171,stroke-width:1px,color:#ffffff
    style FL_INJ fill:#3f1418,stroke:#f87171,stroke-width:1px,color:#ffffff

    style R_LLM fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style R_WRK fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style R_RDS fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style R_DB fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style R_INJ fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
```

| Scenario | Result & System Behavior |
|---|---|
| LLM provider down | Retry once, fallback model, then clear error; chat for cached or "I don't know" paths unaffected |
| Worker crashes mid-ingestion | Job re-delivered, idempotent; document chunk cleanup on retry |
| Redis restarts | Queue jobs may be lost; periodic job re-enqueues stale `uploaded` documents; rate limits reset |
| Database connection pool full | Request timeout, `503`, alert; pool size and timeouts configured |
| One tenant floods requests | Per-tenant rate limit and cap in Redis protects shared infrastructure |
| Malicious PDF with instructions | Treated as data inside XML tags; attack test set run in CI |
| Embedding model changed | Re-index job using `embedding_model` version column |
| Object storage unavailable | Upload fails fast with error; existing retrieval answers unaffected |

---

## 5. Open Decisions (Resolved at Named Phase)

| Decision | Phase |
|---|---|
| Primary LLM and embedding provider | 1 and 2 |
| Chunk size and overlap | 3 |
| Email provider | 4 |
| Hosting provider and size | 6 |
| Bengali keyword search approach | 7 |

---

## 6. Review Checklist Result

- [x] Every Must FR maps to a module, table, endpoint, and phase
- [x] Every architecture driver has a design response
- [x] Tenant isolation designed at four layers with tests
- [x] Async operations have status, retry, and failure handling
- [x] Every module has a one-line responsibility
- [x] No box without a reason (services reduced to API process, worker, optional model server)
- [x] Security, logging, and rate limits considered
- [x] Major decisions recorded as ADRs (0002-0009)
- [ ] Spike results (RLS with pooling, hybrid search with filters) recorded, done in Phase 1 and 3
