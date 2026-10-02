# 02 — Functional Requirements

**Status:** Draft v1 | **Owner:** Awolad | **Last updated:** 2026-09-30
**Priority scale (MoSCoW):** Must / Should / Could / Won't (v1)

> **How to write:**
> - In this file, write **what the system can do**. Do not mention technology names (`client -> backend -> db -> ai agent` is design, which belongs in Step 2).
> - Pattern: `The user can [action] [object] [condition].`
> - Each row must have an ID, priority, and acceptance criteria (how to verify).
> - Writing `04-user-stories.md` first makes writing this file much easier.

---

## 1. Authentication and Organizations

| ID | Requirement | Priority | Acceptance criteria |
|---|---|---|---|
| FR-001 | A company admin can register a new organization. | Must | New organization exists and admin can log in |
| FR-002 | An admin can invite users by email and assign a role (Admin, Employee). | Must | Invited user can join with the given role |
| FR-003 | A user can log in and log out; sessions expire after inactivity. | Must | Expired session requires login again |
| FR-004 | A user can only see data of their own organization. | Must | Test: user of Org A gets nothing from Org B |

### Architecture & Boundary Flow

```mermaid
flowchart TD
    subgraph ORG_MGMT ["1. Multi-Tenant Organization Boundary"]
        ADMIN["<b>Company Admin</b><br/>Registers new organization"]
        ORG["<b>Tenant Organization Entity</b><br/>Isolated database workspace"]
        ADMIN -->|"FR-001: Register"| ORG
    end

    subgraph RBAC ["2. Role-Based Access Control"]
        INVITE["<b>Email Invitation</b><br/>FR-002: Admin invites team"]
        ROLE_A["<b>Admin Role</b><br/>Manage docs, view analytics, invite users"]
        ROLE_E["<b>Employee Role</b><br/>Ask questions, view citations, escalate"]
        
        INVITE --> ROLE_A
        INVITE --> ROLE_E
    end

    subgraph ISOLATION ["3. Strict Tenant Isolation (FR-004)"]
        TENANT_A["<b>Org A Workspace</b><br/>Users, docs, chat history"]
        BARRIER{{"<b>Tenant Security Boundary</b><br/>Zero cross-tenant data access"}}
        TENANT_B["<b>Org B Workspace</b><br/>Users, docs, chat history"]
        
        TENANT_A -.->|"Access Blocked"| BARRIER
        TENANT_B -.->|"Access Blocked"| BARRIER
    end

    ORG --> INVITE

    style ORG_MGMT fill:#111827,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style RBAC fill:#111827,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style ISOLATION fill:#111827,stroke:#f87171,stroke-width:1px,color:#ffffff

    style ADMIN fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style ORG fill:#271b3d,stroke:#c084fc,stroke-width:2px,color:#ffffff
    style INVITE fill:#1e293b,stroke:#94a3b8,stroke-width:1px,color:#ffffff
    style ROLE_A fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style ROLE_E fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style TENANT_A fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style BARRIER fill:#3f1418,stroke:#ef4444,stroke-width:2px,color:#ffffff
    style TENANT_B fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
```

---

## 2. Document Management

| ID | Requirement | Priority | Acceptance criteria |
|---|---|---|---|
| FR-010 | An admin can upload PDF, DOCX, TXT, and Markdown files. | Must | Uploaded file appears in the document list |
| FR-011 | An admin can add a web page by URL. | Should | Page content becomes searchable |
| FR-012 | The system processes each document in the background and shows its status (Uploaded, Processing, Ready, Failed). | Must | Status changes; failure shows a reason |
| FR-013 | An admin can delete or replace a document; deleted content is no longer used in answers. | Must | Question about deleted content returns "I don't know" |
| FR-014 | An admin can assign a category (HR, IT, Finance) and restrict access by role. | Should | Employee cannot get answers from restricted documents |

### Ingestion Lifecycle & Governance Flow

```mermaid
flowchart TD
    subgraph INGEST ["1. Source Ingestion"]
        DOCS["<b>Uploaded Files</b><br/>PDF, DOCX, TXT, Markdown (FR-010)"]
        URL["<b>Web Resource</b><br/>Page added by URL (FR-011)"]
    end

    subgraph PIPELINE ["2. Processing State Machine (FR-012)"]
        S_UP["<b>Uploaded</b><br/>File received & stored"]
        S_PROC["<b>Processing</b><br/>Parsing, chunking & vector embedding"]
        S_READY["<b>Ready</b><br/>Searchable in knowledge base"]
        S_FAIL["<b>Failed</b><br/>Error reason displayed to admin"]

        S_UP --> S_PROC
        S_PROC -->|"Success"| S_READY
        S_PROC -->|"Parsing/Embed error"| S_FAIL
    end

    subgraph GOV ["3. Governance & Lifecycle (FR-013 & FR-014)"]
        CAT["<b>Category & Access Restriction</b><br/>Assigned to HR, IT, Finance with role limits"]
        DEL["<b>Deletion / Replacement</b><br/>Immediately purged from active search indices"]
    end

    DOCS --> S_UP
    URL --> S_UP
    S_READY --> CAT
    S_READY --> DEL

    style INGEST fill:#111827,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style PIPELINE fill:#111827,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style GOV fill:#111827,stroke:#c084fc,stroke-width:1px,color:#ffffff

    style DOCS fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style URL fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style S_UP fill:#1e293b,stroke:#94a3b8,stroke-width:1px,color:#ffffff
    style S_PROC fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style S_READY fill:#142918,stroke:#4ade80,stroke-width:2px,color:#ffffff
    style S_FAIL fill:#3f1418,stroke:#f87171,stroke-width:2px,color:#ffffff
    style CAT fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style DEL fill:#3f1418,stroke:#f87171,stroke-width:1px,color:#ffffff
```

---

## 3. Chat and Answers

| ID | Requirement | Priority | Acceptance criteria |
|---|---|---|---|
| FR-020 | An employee can ask a question in natural language. | Must | Answer returned for a question covered by documents |
| FR-021 | The answer appears progressively (streaming). | Should | First words appear before the full answer is ready |
| FR-022 | Every answer shows its sources (document name and page or section). | Must | Each answer has at least one citation that opens the source |
| FR-023 | If no relevant information exists, the system says it does not know and does not guess. | Must | Out-of-scope test questions get "I don't know" |
| FR-024 | Conversations are saved; a user can reopen past conversations and continue. | Must | Past chat is listed and can be continued |
| FR-025 | A user can rate an answer (thumbs up/down) with an optional comment. | Should | Rating is stored and visible to admin |
| FR-026 | A user can ask questions in Bengali. | Could | Bengali question returns a correct answer |

### Conversational Retrieval & Streaming Flow

```mermaid
flowchart TD
    Q_IN(["<b>Employee Question</b><br/>Natural language or Bengali (FR-020, FR-026)"])

    subgraph ENGINE ["Response Engine & Grounding"]
        STREAM["<b>Progressive SSE Streaming</b><br/>First words stream in real-time (FR-021)"]
        KNOW{"<b>Document Match Found?</b>"}
        
        STREAM --> KNOW
        
        ANS_OK["<b>Grounded Answer with Sources</b><br/>Exact document name, section & link (FR-022)"]
        ANS_NO["<b>Strict Safe Rejection</b><br/>'I don't know' — No guessing (FR-023)"]
        
        KNOW -- "Yes" --> ANS_OK
        KNOW -- "No" --> ANS_NO
    end

    subgraph POST ["Session Persistence & Feedback"]
        SESS["<b>Session History</b><br/>Conversation saved & resumed (FR-024)"]
        FB["<b>User Feedback</b><br/>Thumbs up/down + comment (FR-025)"]
    end

    Q_IN --> STREAM
    ANS_OK --> SESS
    ANS_NO --> SESS
    ANS_OK --> FB
    ANS_NO --> FB

    style ENGINE fill:#111827,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style POST fill:#111827,stroke:#4ade80,stroke-width:1px,color:#ffffff

    style Q_IN fill:#271b3d,stroke:#c084fc,stroke-width:2px,color:#ffffff
    style STREAM fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style KNOW fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style ANS_OK fill:#142918,stroke:#4ade80,stroke-width:2px,color:#ffffff
    style ANS_NO fill:#3f1418,stroke:#f87171,stroke-width:2px,color:#ffffff
    style SESS fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style FB fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
```

---

## 4. Escalation

| ID | Requirement | Priority | Acceptance criteria |
|---|---|---|---|
| FR-030 | A user can escalate a question to a responsible person; the message includes the question, the conversation, and the sources found. | Must | Contact receives all three |
| FR-031 | An admin can set escalation contacts per category. | Should | Escalation goes to the matching contact |
| FR-032 | Escalations have a status (Open, Resolved) and the user can see it. | Could | Status visible to the user |

### Contextual Escalation Pipeline

```mermaid
flowchart TD
    TRIG(["<b>Trigger Escalation</b><br/>Unanswered question or critical matter (FR-030)"])

    subgraph PAYLOAD ["1. Escalation Context Package"]
        P1["<b>User Query:</b> Original question"]
        P2["<b>Chat History:</b> Full multi-turn context"]
        P3["<b>Retrieved Sources:</b> Chunks/docs referenced"]
    end

    subgraph ROUTER ["2. Category-Based Routing (FR-031)"]
        ROUT{"<b>Category Match</b>"}
        C_HR["<b>HR Contact</b><br/>Leave, benefits, policy"]
        C_IT["<b>IT Helpdesk</b><br/>Access, hardware, VPN"]
        C_FIN["<b>Finance Desk</b><br/>Payroll, expense claims"]
        
        ROUT -->|"HR"| C_HR
        ROUT -->|"IT"| C_IT
        ROUT -->|"Finance"| C_FIN
    end

    subgraph TRACK ["3. Ticket Lifecycle (FR-032)"]
        ST_OPEN["<b>Status: Open</b><br/>Visible in employee dashboard"]
        ST_RES["<b>Status: Resolved</b><br/>Feedback & answer documented"]
        ST_OPEN --> ST_RES
    end

    TRIG --> PAYLOAD
    PAYLOAD --> ROUT
    C_HR --> ST_OPEN
    C_IT --> ST_OPEN
    C_FIN --> ST_OPEN

    style PAYLOAD fill:#111827,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style ROUTER fill:#111827,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style TRACK fill:#111827,stroke:#4ade80,stroke-width:1px,color:#ffffff

    style TRIG fill:#3f1418,stroke:#f87171,stroke-width:2px,color:#ffffff
    style P1 fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style P2 fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style P3 fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style ROUT fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style C_HR fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style C_IT fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style C_FIN fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style ST_OPEN fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style ST_RES fill:#142918,stroke:#4ade80,stroke-width:2px,color:#ffffff
```

---

## 5. Assistant Actions

| ID | Requirement | Priority | Acceptance criteria |
|---|---|---|---|
| FR-040 | The assistant can prepare actions such as creating a ticket or drafting an email. | Should | Draft is shown to the user |
| FR-041 | Any action with side effects needs explicit user confirmation before it runs. | Must (if FR-040) | No action runs without a click on "Confirm" |
| FR-042 | The assistant can answer questions from structured company data (read-only). | Could | Read-only query returns correct result |

### Human-In-The-Loop (HITL) Execution Gate

```mermaid
flowchart TD
    subgraph DRAFT ["1. Action Preparation (FR-040)"]
        ACT["<b>Assistant Action Triggered</b><br/>e.g., Draft support ticket or draft email"]
        PREV["<b>Interactive Preview</b><br/>Title, recipient, body, and payload shown to user"]
        ACT --> PREV
    end

    subgraph GATE ["2. Human-In-The-Loop Approval Gate (FR-041)"]
        CONFIRM{"<b>User Decision</b><br/>Explicit confirmation required"}
        PREV --> CONFIRM
        
        BTN_OK["<b>User Clicks 'Confirm'</b><br/>Explicit authorization given"]
        BTN_NO["<b>User Clicks 'Cancel / Edit'</b><br/>Abort or revise parameters"]
        
        CONFIRM -- "Approved" --> BTN_OK
        CONFIRM -- "Rejected" --> BTN_NO
    end

    subgraph EXEC ["3. Safe Side-Effect Execution"]
        RUN["<b>Action Dispatched</b><br/>Ticket created or email sent via external API"]
        ABORT["<b>Execution Blocked</b><br/>No side effects performed"]
        
        BTN_OK --> RUN
        BTN_NO --> ABORT
    end

    style DRAFT fill:#111827,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style GATE fill:#111827,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style EXEC fill:#111827,stroke:#64748b,stroke-width:1px,color:#ffffff

    style ACT fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style PREV fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style CONFIRM fill:#3b2413,stroke:#fbbf24,stroke-width:2px,color:#ffffff
    style BTN_OK fill:#142918,stroke:#4ade80,stroke-width:2px,color:#ffffff
    style BTN_NO fill:#3f1418,stroke:#f87171,stroke-width:2px,color:#ffffff
    style RUN fill:#142918,stroke:#4ade80,stroke-width:2px,color:#ffffff
    style ABORT fill:#3f1418,stroke:#ef4444,stroke-width:1px,color:#ffffff
```

---

## 6. Admin Dashboard

| ID | Requirement | Priority | Acceptance criteria |
|---|---|---|---|
| FR-050 | An admin can see usage: number of questions, tokens, and cost per day. | Should | Numbers match stored usage |
| FR-051 | An admin can see questions that had no answer (knowledge gaps). | Should | "I don't know" questions listed |
| FR-052 | An admin can see answer ratings and comments. | Could | Ratings listed |

### Admin Observability & Knowledge Feedback Loop

```mermaid
flowchart TD
    subgraph TELEM ["1. Incoming Operational Telemetry"]
        T_USAGE["<b>Usage Telemetry</b><br/>Question count, token usage, daily cost (FR-050)"]
        T_GAPS["<b>Knowledge Gap Log</b><br/>Unanswered questions & 'I don't know' count (FR-051)"]
        T_RATING["<b>Feedback Telemetry</b><br/>User thumbs up/down & commentary (FR-052)"]
    end

    subgraph DASH ["2. Admin Oversight Dashboard"]
        VIEW["<b>Unified Analytics Console</b><br/>Cost trends, top queries, weak documentation areas"]
    end

    subgraph LOOP ["3. Continuous Knowledge Improvement Loop"]
        DOC_UPDATE["<b>Doc Authoring / Update</b><br/>Admin uploads or revises missing policy docs"]
        BETTER["<b>Higher Answer Rate</b><br/>Reduced escalations & improved user satisfaction"]
        
        DOC_UPDATE --> BETTER
    end

    T_USAGE --> VIEW
    T_GAPS --> VIEW
    T_RATING --> VIEW
    VIEW -->|"Identifies missing topics"| DOC_UPDATE

    style TELEM fill:#111827,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style DASH fill:#111827,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style LOOP fill:#111827,stroke:#4ade80,stroke-width:1px,color:#ffffff

    style T_USAGE fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style T_GAPS fill:#3f1418,stroke:#f87171,stroke-width:1px,color:#ffffff
    style T_RATING fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style VIEW fill:#271b3d,stroke:#c084fc,stroke-width:2px,color:#ffffff
    style DOC_UPDATE fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style BETTER fill:#142918,stroke:#4ade80,stroke-width:2px,color:#ffffff
```

---

## 7. Not in v1 (Won't)

- Mobile app
- Voice input/output
- Slack / Teams integration (revisit later)
- Billing and payments

## 8. Plans, onboarding, and data control

| ID | Requirement | Priority | Acceptance criteria |
|---|---|---|---|
| FR-060 | An admin can view the organization's plan, limits, and current usage. | Should | The usage page shows questions used compared with the plan limit. |
| FR-061 | The system enforces plan limits for employees, documents, and questions, warns at 80%, and blocks usage at 100%. | Must (for paid plans) | Requests beyond a limit receive a clear message; warnings appear at 80%. |
| FR-062 | A new admin receives a guided first-run checklist to upload a document, ask a question, and invite a user. | Should | A new admin can complete the checklist in under 10 minutes. |
| FR-063 | An admin can export all organization data, including documents and conversations, on request. | Must (for paid plans) | The export contains the organization's documents and conversations. |
| FR-064 | An admin can request deletion of the organization and its data. | Must (for paid plans) | Data is removed within the published retention period, and the admin receives confirmation. |
| FR-065 | An admin can view an audit log of important actions, including uploads, deletions, role changes, and exports. | Should | Each log entry includes the actor, action, and time. |
| FR-066 | A platform owner can produce a monthly invoice record for each organization from its plan and usage. | Could | An invoice record can be exported as CSV or PDF. |
| FR-067 | A user can send feedback or contact support from the application. | Should | The message is delivered to the configured support channel and its delivery result is recorded. |

---

## 9. Traceability

Each requirement should be traced to a story in [the user stories](04-user-stories.md). If a requirement has no story, ask who needs it.
