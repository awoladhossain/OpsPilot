# 01 — Problem Statement

**Status:** Draft v1 | **Owner:** Awolad | **Last updated:** 2026-09-30

> **How to write:** In this file, write only the *problem*, not the solution. Pattern:
> `[Who] cannot [do what] because [why], which causes [impact].`
> The ideas from your draft (hesitation, forgetting follow-ups, reaching out to someone else when critical) were good. They have been organized into sections here.
> Rewrite in your own words; this file is just an example.

---

## 1. Background

Every company has rules, policies, and process information: leave policy, IT rules, expense process, onboarding steps. This information is usually spread across PDFs, shared drives, wikis, and chat messages.

## 2. Problem Statement

Employees cannot quickly and confidently find the right company rule or information, because it is scattered and the only alternative is to ask a colleague, which causes wasted time, repeated questions, wrong decisions, and delayed work.

### Problem Breakdown Flow

```mermaid
flowchart TD
    subgraph S1 ["1. Root Cause: Knowledge Fragmentation"]
        A["<b>Scattered Policies & Documents</b><br/>PDFs in drives, wikis, Slack threads, outdated sheets"]
    end

    subgraph S2 ["2. Access Bottleneck"]
        B["<b>Hesitation & Human Dependency</b><br/>Unclear whom to ask • Fear of asking repeat questions • Colleague busy"]
    end

    subgraph S3 ["3. Immediate Consequences"]
        C1["<b>Delayed Decisions</b><br/>Work blocked waiting for answers"]
        C2["<b>Repeated Interruptions</b><br/>HR & IT answer same FAQs daily"]
        C3["<b>Inaccurate Actions</b><br/>Employees guess or rely on hearsay"]
    end

    subgraph S4 ["4. Business Impact"]
        D["<b>Lost Productivity, Operational Inefficiency & Compliance Risks</b>"]
    end

    A --> B
    B --> C1
    B --> C2
    B --> C3
    C1 --> D
    C2 --> D
    C3 --> D

    style S1 fill:#111827,stroke:#64748b,stroke-width:1px,color:#ffffff
    style S2 fill:#111827,stroke:#64748b,stroke-width:1px,color:#ffffff
    style S3 fill:#111827,stroke:#64748b,stroke-width:1px,color:#ffffff
    style S4 fill:#111827,stroke:#64748b,stroke-width:1px,color:#ffffff
    style A fill:#3f1418,stroke:#f87171,stroke-width:2px,color:#ffffff
    style B fill:#3b2413,stroke:#fbbf24,stroke-width:2px,color:#ffffff
    style C1 fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style C2 fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style C3 fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style D fill:#3f1418,stroke:#ef4444,stroke-width:2px,color:#ffffff
```

---

## 3. Who is Affected

| Who | Pain |
|---|---|
| **Employee** | Does not know whom to ask, hesitates to ask, or finds nobody available |
| **Manager / HR / IT** | Answers the same questions again and again, gets interrupted |
| **Company admin** | Has no idea what employees are confused about |

---

## 4. Pain Points

1. **Hesitation:** Employee feels uncomfortable asking small or repeated questions.
2. **No time / no person:** The right person is busy, absent, or unknown.
3. **Forgotten follow-ups:** A new question comes to mind later, and asking again is awkward.
4. **Scattered information:** Documents exist but nobody knows where.
5. **No path for critical issues:** When a question is important or the answer is missing, there is no clear way to reach the right person with context.

### Stakeholder Pain Point Architecture

```mermaid
flowchart TD
    subgraph EMP ["Employee Experience"]
        E1["<b>Information Blindness</b><br/>Documents are hidden or hard to search"]
        E2["<b>Social Friction & Hesitation</b><br/>Reluctant to ping seniors for small queries"]
        E3["<b>Abandoned Follow-ups</b><br/>New questions arise later; asking again feels awkward"]
    end

    subgraph MGR ["Manager / HR / IT Team"]
        M1["<b>Constant Context Switching</b><br/>Answering basic policy FAQs interrupts deep work"]
        M2["<b>Inconsistent Guidance</b><br/>Different people give conflicting policy answers"]
    end

    subgraph ADM ["Company Leadership & Admin"]
        A1["<b>Zero Visibility</b><br/>No analytics on what policies confuse staff"]
        A2["<b>Knowledge Gaps Unnoticed</b><br/>Missing docs only surface after costly mistakes"]
    end

    style EMP fill:#111827,stroke:#38bdf8,stroke-width:2px,color:#ffffff
    style MGR fill:#111827,stroke:#fbbf24,stroke-width:2px,color:#ffffff
    style ADM fill:#111827,stroke:#c084fc,stroke-width:2px,color:#ffffff

    style E1 fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style E2 fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style E3 fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff

    style M1 fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style M2 fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff

    style A1 fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style A2 fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
```

---

## 5. Current Workarounds and Why They Fail

| Workaround | Why it fails |
|---|---|
| Ask a colleague | Interrupts them, inconsistent answers, depends on availability |
| Search shared drive / Ctrl+F in PDF | Slow, keyword-only, easy to miss the right document |
| Read the full handbook | Nobody does |

### Workaround Failure Modes

```mermaid
flowchart TD
    subgraph W1 ["Workaround 1: Ask a Colleague"]
        A1["<b>Attempt:</b> Ping teammate or HR via Slack/Teams"]
        A2["<b>Breakdown:</b> Distracts colleague, answers are delayed or inconsistent"]
        A1 --> A2
    end

    subgraph W2 ["Workaround 2: Search Shared Drive / Ctrl+F"]
        B1["<b>Attempt:</b> Search keywords in nested drive folders"]
        B2["<b>Breakdown:</b> Keyword mismatch, outdated versions found"]
        B1 --> B2
    end

    subgraph W3 ["Workaround 3: Read Full Handbook"]
        C1["<b>Attempt:</b> Skim 80-page company manual"]
        C2["<b>Breakdown:</b> High cognitive load, ignored by almost everyone"]
        C1 --> C2
    end

    style W1 fill:#111827,stroke:#f87171,stroke-width:1px,color:#ffffff
    style W2 fill:#111827,stroke:#f87171,stroke-width:1px,color:#ffffff
    style W3 fill:#111827,stroke:#f87171,stroke-width:1px,color:#ffffff

    style A1 fill:#1e293b,stroke:#94a3b8,stroke-width:1px,color:#ffffff
    style A2 fill:#3f1418,stroke:#f87171,stroke-width:1px,color:#ffffff
    style B1 fill:#1e293b,stroke:#94a3b8,stroke-width:1px,color:#ffffff
    style B2 fill:#3f1418,stroke:#f87171,stroke-width:1px,color:#ffffff
    style C1 fill:#1e293b,stroke:#94a3b8,stroke-width:1px,color:#ffffff
    style C2 fill:#3f1418,stroke:#f87171,stroke-width:1px,color:#ffffff
```

---

## 6. Proposed Solution (High-Level Conceptual Flow)

OpsPilot is a SaaS application where a company uploads its rules and documents, and employees ask questions in natural language. The system answers **only from the company's documents**, shows **where the answer came from**, and if the answer is missing or the issue is critical, lets the employee **escalate to a responsible person** with the full context.

### Proposed User Journey & Resolution Logic

```mermaid
flowchart TD
    USER(["<b>Employee</b><br/>Asks question in plain natural language"])

    subgraph OPS ["OpsPilot Internal Workflow"]
        SYS["<b>Document Retrieval & Grounded QA</b><br/>Search indexed & verified company documentation only"]
        CHECK{"<b>Answer found in verified docs?</b>"}
        
        SYS --> CHECK
        
        RES_OK["<b>Verified Answer with Citations</b><br/>• Direct policy excerpt<br/>• Source doc name & page link"]
        RES_FAIL["<b>Safe Rejection & Contextual Escalation</b><br/>• Honest 'I don't know' (No hallucinations)<br/>• 1-Click Ticket with conversation context"]
        
        CHECK -- "Yes" --> RES_OK
        CHECK -- "No or Critical" --> RES_FAIL
    end

    subgraph OUTCOMES ["Resolution Paths"]
        RESOLVED["<b>Instant Resolution</b><br/>Employee proceeds with work in seconds"]
        HANDOFF["<b>Targeted Escalation</b><br/>HR/IT receives pre-packaged context"]
    end

    USER --> SYS
    RES_OK --> RESOLVED
    RES_FAIL --> HANDOFF

    style USER fill:#271b3d,stroke:#c084fc,stroke-width:2px,color:#ffffff
    style OPS fill:#111827,stroke:#38bdf8,stroke-width:2px,color:#ffffff
    style OUTCOMES fill:#111827,stroke:#64748b,stroke-width:1px,color:#ffffff

    style SYS fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style CHECK fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style RES_OK fill:#142918,stroke:#4ade80,stroke-width:2px,color:#ffffff
    style RES_FAIL fill:#3f1418,stroke:#f87171,stroke-width:2px,color:#ffffff
    style RESOLVED fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style HANDOFF fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
```

---

## 7. Goals

- Employees get correct, sourced answers in seconds without asking a person.
- Employees can escalate critical or unanswered questions with one action.
- Admins can see what employees are asking and which questions have no answer.

## 8. Non-Goals (v1)

- Not a general-purpose chatbot (does not answer outside company documents).
- Not a replacement for HR or legal decisions.
- No mobile app, no voice.

---

## 9. Success Metrics

> Numbers below are **initial targets (assumptions)**. Revise after testing.

| Metric | Target | How to measure |
|---|---|---|
| Answer correctness on test questions | >= 85% | Evaluation dataset |
| Answers with correct citation | >= 80% | Evaluation dataset |
| Time to first response | < 2 s (p95) | Metrics dashboard |
| "I don't know" instead of a wrong answer | 100% on out-of-scope test questions | Evaluation dataset |
| Escalation delivered with context | 100% | Automated test |

### Success Metrics & Target Thresholds

```mermaid
flowchart TD
    subgraph M1 ["1. Retrieval & Quality"]
        Q1["<b>Answer Correctness</b><br/>Target: >= 85%<br/>Evaluation dataset testing"]
        Q2["<b>Source Citation Accuracy</b><br/>Target: >= 80%<br/>Verified link to source doc"]
    end

    subgraph M2 ["2. Performance"]
        P1["<b>Response Latency</b><br/>Target: < 2s (p95)<br/>Fast streaming response"]
    end

    subgraph M3 ["3. Trust & Reliability"]
        S1["<b>Zero Hallucination Tolerance</b><br/>Target: 100% on out-of-scope queries<br/>Explicit 'I don't know' reply"]
        S2["<b>Escalation Delivery</b><br/>Target: 100% with full context<br/>Pre-packaged ticket handoff"]
    end

    style M1 fill:#111827,stroke:#38bdf8,stroke-width:2px,color:#ffffff
    style M2 fill:#111827,stroke:#fbbf24,stroke-width:2px,color:#ffffff
    style M3 fill:#111827,stroke:#4ade80,stroke-width:2px,color:#ffffff

    style Q1 fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style Q2 fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style P1 fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style S1 fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style S2 fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
```

---

## 10. Open Questions

- Which document types are needed first (PDF only, or DOCX and web pages too)?
- Who receives an escalation: one contact per company or per category (HR, IT, Finance)?
- Should employees be allowed to see every document, or only some?
