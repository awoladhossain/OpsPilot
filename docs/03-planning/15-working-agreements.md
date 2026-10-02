# 15 — Working Agreements

**Status:** Approved v1 (reference) | **Last updated:** 2026-10-01

> An agreement with yourself. Establish these operating principles before beginning development so you never have to deliberate on routine process decisions.

---

## 1. Repository Structure

```
opspilot/
├── backend/
│   ├── app/
│   │   ├── core/              # config, db session, security context, logging, telemetry
│   │   └── modules/
│   │       ├── identity/
│   │       ├── documents/
│   │       ├── ingestion/
│   │       ├── retrieval/
│   │       ├── llm/
│   │       ├── chat/
│   │       ├── agent/
│   │       ├── escalation/
│   │       ├── usage/
│   │       └── admin/
│   ├── alembic/
│   ├── tests/
│   └── pyproject.toml
├── frontend/
├── eval/                      # datasets, evaluation scripts, reports
├── infra/                     # compose files, prometheus, grafana, loki, alloy, proxy config
├── docs/                      # requirements, design, ADRs, notes, retros
│   ├── adr/
│   ├── notes/                 # your own concept notes
│   └── retros/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   ├── workflows/
│   └── pull_request_template.md
├── docker-compose.yml
├── Makefile
└── README.md
```

Each module folder contains: `service.py` (public interface), private `models`, `repository`, `schemas`, `tests`.

---

## 2. Git Workflow (Trunk-Based, Short Branches)

```mermaid
flowchart TD
    subgraph MAIN_TRUNK ["Protected Trunk (main Branch)"]
        M1["<b>main (Deployable State)</b><br/>Always green • Direct commits blocked"]
    end

    subgraph FEATURE_BRANCH ["Short-Lived Feature Branch (&lt; 400 LOC)"]
        F1["<b>Branch Out:</b> feat/P2-06-ingestion-worker<br/>Created from latest main"]
        F2["<b>Local Dev:</b> TDD cycle + pre-commit hooks<br/>Ruff format, type checks"]
        F3["<b>Self-Review:</b> Read own git diff<br/>Verify zero secrets, zero debug logs"]
        
        F1 --> F2 --> F3
    end

    subgraph CI_PR_GATES ["Automated CI & Merge Gates"]
        PR["<b>Open Pull Request</b><br/>PR template filled, closes #issue"]
        CI["<b>CI Quality Gates</b><br/>ruff $\rightarrow$ mypy $\rightarrow$ import-linter $\rightarrow$ pytest"]
        MERGE["<b>Squash & Merge to main</b><br/>Clean conventional commit message"]
        TAG["<b>Semantic Tagging (Post-Phase)</b><br/>git tag v0.2.0"]

        PR --> CI --> MERGE --> TAG
    end

    M1 --> F1
    F3 --> PR
    MERGE --> M1

    style MAIN_TRUNK fill:#111827,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style FEATURE_BRANCH fill:#111827,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style CI_PR_GATES fill:#111827,stroke:#4ade80,stroke-width:1px,color:#ffffff

    style M1 fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style F1 fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style F2 fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style F3 fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style PR fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style CI fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style MERGE fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style TAG fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
```

| Rule | Detail |
|---|---|
| `main` | Always deployable; protected; changes only by pull request; CI must pass |
| Branch name | `<type>/<task-id>-<short-name>`, for example `feat/P2-06-ingestion-worker` |
| Branch life | Short: merge within 1-3 days, never weeks |
| PR size | Aim for under about 400 changed lines; split bigger work |
| Merge | Squash merge with a clean title |
| Self-review | Read your own diff before asking CI to pass |
| Tags | Tag each finished phase (`v0.1.0` after Phase 1 and so on) |

### Commit Messages (Conventional Commits)

Format: `<type>(<scope>): <summary>`

| Type | Use |
|---|---|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation |
| `test` | Tests |
| `refactor` | Code change without behavior change |
| `chore` | Tooling, dependencies |
| `ci` | Pipeline changes |
| `perf` | Performance |

---

## 3. Definition of Done (DoD)

```mermaid
flowchart TD
    subgraph TASK_DOD ["Task-Level DoD (Every Pull Request)"]
        T1["<b>1. Functionality & Tests:</b> Code works, unit/integration tests cover edges"]
        T2["<b>2. Acceptance Criteria:</b> 'Done when' checklist fully met"]
        T3["<b>3. Static Analysis:</b> ruff, mypy strict, import-linter pass locally & CI"]
        T4["<b>4. Hygiene & Security:</b> Zero secrets, no print statements, PII masked"]
        T5["<b>5. Documentation:</b> Design docs and ADRs updated in the same PR"]
        T6["<b>6. Concept Notes:</b> 5-line explanation logged in docs/notes/"]

        T1 --> T2 --> T3 --> T4 --> T5 --> T6
    end

    subgraph PHASE_DOD ["Phase-Level DoD (Milestone Exit Gate)"]
        P_DEMO["Live Recorded Demo (2-3 min)"]
        P_CRIT["All Phase Exit Criteria Checked"]
        P_RETRO["Written Retrospective in docs/retros/"]
        P_TAG["Release Tag Created (e.g. v0.2.0)"]

        T6 --> P_DEMO --> P_CRIT --> P_RETRO --> P_TAG
    end

    style TASK_DOD fill:#111827,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style PHASE_DOD fill:#111827,stroke:#4ade80,stroke-width:1px,color:#ffffff

    style T1 fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style T2 fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style T3 fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style T4 fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style T5 fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style T6 fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff

    style P_DEMO fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style P_CRIT fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style P_RETRO fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style P_TAG fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
```

### Per Task Checklist
- [ ] Code works and **is tested** (unit or integration)
- [ ] "Done when" criterion of the task is met
- [ ] Lint, type check, module boundary check pass
- [ ] CI is green
- [ ] No secrets, no `print` debugging, no commented-out code
- [ ] Docs updated if behavior, API, or design changed (and ADR if a decision changed)
- [ ] You can explain it in 5 lines (note added to `docs/notes/` for new concepts)

### Per Phase Checklist
See [13 section 8](13-roadmap-and-milestones.md).

---

## 4. Code Standards

| Area | Rule |
|---|---|
| Style | Formatter and linter run by pre-commit and CI; no style debates |
| Types | Type hints everywhere; type checker in CI |
| Naming | Clear names over comments; English everywhere in code |
| Modules | Respect boundaries (import contracts in CI) |
| Errors | Domain errors mapped to the standard error format |
| Config | Environment variables only; no constants for secrets |
| Logging | Structured, no secrets or document content |
| Async | Do not block the event loop; database and HTTP calls are async |
| Dependencies | Add deliberately; pin versions; review before adding |

---

## 5. Testing Strategy & Hierarchy

```mermaid
flowchart TD
    subgraph TEST_SUITE ["Multi-Layered Testing Hierarchy"]
        L5["<b>Load & Resilience (k6 / Locust):</b> Throughput, p95 latency, circuit breaking"]
        L4["<b>AI Evaluation (eval/ harness):</b> Faithfulness, hit rate, citation accuracy"]
        L3["<b>Contract & Security:</b> 4-layer tenant isolation, prompt injection attacks"]
        L2["<b>Integration Tests (pytest + Testcontainers):</b> Real PostgreSQL + pgvector, Redis"]
        L1["<b>Unit Tests (pytest):</b> Pure logic, chunkers, parsers, scoring calculations"]

        L1 --> L2 --> L3 --> L4 --> L5
    end

    style TEST_SUITE fill:#111827,stroke:#fbbf24,stroke-width:1px,color:#ffffff

    style L1 fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style L2 fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style L3 fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style L4 fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style L5 fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
```

| Level | What | Tools (examples) |
|---|---|---|
| Unit | Pure logic: chunking, scoring, parsers | pytest |
| Integration | API with real Postgres and Redis | pytest with service containers |
| Contract | Isolation, injection, API snapshot | Dedicated test suites |
| Evaluation | RAG quality on dataset | `eval/` harness |
| Load | Throughput and latency | k6 or Locust |

Rule: bug found, then write a failing test first, then fix.

---

## 6. Documentation Rules

- Code change that changes design: update the doc in the same pull request.
- Major decision: ADR before or with the code.
- Every phase: retro file in `docs/retros/`.
- Concept notes in your own words in `docs/notes/` (these are for you, and prove understanding).

---

## 7. Time and Focus

- WIP limit 2.
- Weekly review every Sunday (template in the planning guide).
- One rest day per week, no exceptions.
- If stuck more than 45 minutes on one problem, write the question down in 5 lines (rubber-duck) and then ask for help.
- Time-box experiments: stop when time is over and write down what you learned.

---

## 8. Security Hygiene

- `.env` never committed; `.env.example` only names.
- Secret scanning in CI.
- Do not paste real company or personal documents into test data; use made-up sample policies.
- Keep API keys with spending limits set at the provider.
