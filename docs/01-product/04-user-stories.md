# 04 — User Stories

**Status:** Draft v1 | **Owner:** Awolad | **Last updated:** 2026-09-30

> **How to write:**
> - Story = a task from the **user's perspective**. Pattern: `As a [role], I want [action], so that [benefit].`
> - **Do not omit "so that" (benefit).** That explains why the feature is needed.
> - Under each story, include **Acceptance Criteria**: `Given [context], When [action], Then [result].`
> - Link each story with its corresponding FR ID (traceability).
> - Keep them small: one story = 1 task, roughly 1-3 days of work.

---

## Personas

| Persona | Description | Goal |
|---|---|---|
| **Employee** (e.g., Rafi, developer, 6 months in company) | Has questions about leave, IT, expenses | Get an answer fast, without disturbing anyone |
| **Admin** (e.g., Nusrat, HR manager) | Owns company documents | Keep information correct, reduce repeated questions |
| **Escalation contact** | HR / IT / Finance person | Receive only questions that need a human, with context |

### Persona Architecture & Goals

```mermaid
flowchart TD
    subgraph P1 ["Persona: Employee (e.g., Rafi)"]
        EMP["<b>Rafi — Software Engineer</b><br/>• Needs policy answers quickly (leave, remote work, equipment)<br/>• Wants to avoid social hesitation & disturbing teammates"]
    end

    subgraph P2 ["Persona: Admin (e.g., Nusrat)"]
        ADM["<b>Nusrat — HR Operations Lead</b><br/>• Manages source policies & access permissions<br/>• Wants to eliminate repetitive FAQ interruptions<br/>• Monitors unanswered questions to close knowledge gaps"]
    end

    subgraph P3 ["Persona: Escalation Contact"]
        ESC["<b>Department Lead (HR / IT / Finance)</b><br/>• Handles complex or exception policy queries<br/>• Demands pre-packaged conversation context"]
    end

    style P1 fill:#111827,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style P2 fill:#111827,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style P3 fill:#111827,stroke:#fbbf24,stroke-width:1px,color:#ffffff

    style EMP fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style ADM fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style ESC fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
```

---

## Epic A: Get Answers

### US-001 Ask a question
As an **Employee**, I want to ask a question in plain language, so that I get the rule without searching documents. *(FR-020, FR-021)*

- **Given** the leave policy is uploaded, **when** I ask "How many casual leave days do I get?", **then** I receive an answer based on the policy.
- **Given** the answer is being generated, **when** the first words are ready, **then** they appear immediately.

### US-002 See sources
As an **Employee**, I want to see where each answer came from, so that I can trust it and read the original. *(FR-022)*

- **Given** an answer is shown, **when** I look below it, **then** I see the document name and page or section.

### US-003 Honest "I don't know"
As an **Employee**, I want the assistant to say when it does not know, so that I am never given a made-up rule. *(FR-023)*

- **Given** no document covers my question, **when** I ask it, **then** I see "I could not find this in the company documents" and an option to escalate.

### US-004 Continue later
As an **Employee**, I want to reopen my past conversations, so that I can ask a follow-up later without repeating myself. *(FR-024)*

- **Given** I asked a question yesterday, **when** I open my history, **then** I can continue that conversation.

### US-005 Rate an answer
As an **Employee**, I want to mark an answer helpful or not, so that the company can improve it. *(FR-025)*

### Conversational Answer Journey

```mermaid
flowchart TD
    subgraph ASK ["1. Query & Streaming (US-001)"]
        Q["<b>Employee Asks Question</b><br/>'How many casual leave days do I get?'"]
        STREAM["<b>Real-Time Token Streaming</b><br/>Immediate visual feedback as words generate"]
        Q --> STREAM
    end

    subgraph RESOLUTION ["2. Dual Grounding Branches"]
        DECIDE{"<b>Found in Company Docs?</b>"}
        
        ANS["<b>Grounded Response (US-002)</b><br/>Policy answer displayed with source link & page"]
        UNKNOWN["<b>Honest 'I Don't Know' (US-003)</b><br/>Explicit statement without hallucination"]
        
        STREAM --> DECIDE
        DECIDE -- "Yes" --> ANS
        DECIDE -- "No" --> UNKNOWN
    end

    subgraph ACTIONS ["3. Post-Answer Actions"]
        CITE["<b>Click Source Citation</b><br/>Directly verify excerpt in original PDF"]
        FEEDBACK["<b>Rate Answer (US-005)</b><br/>Thumbs up / down + optional comment"]
        SAVE["<b>Session Preserved (US-004)</b><br/>Reopen chat history anytime for follow-ups"]
        ESCALATE_BTN["<b>Escalate Button</b><br/>One-click transition to human help"]
        
        ANS --> CITE
        ANS --> FEEDBACK
        ANS --> SAVE
        UNKNOWN --> ESCALATE_BTN
    end

    style ASK fill:#111827,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style RESOLUTION fill:#111827,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style ACTIONS fill:#111827,stroke:#4ade80,stroke-width:1px,color:#ffffff

    style Q fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style STREAM fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style DECIDE fill:#3b2413,stroke:#fbbf24,stroke-width:2px,color:#ffffff
    style ANS fill:#142918,stroke:#4ade80,stroke-width:2px,color:#ffffff
    style UNKNOWN fill:#3f1418,stroke:#f87171,stroke-width:2px,color:#ffffff
    style CITE fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style FEEDBACK fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style SAVE fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style ESCALATE_BTN fill:#3f1418,stroke:#f87171,stroke-width:2px,color:#ffffff
```

---

## Epic B: Escalate

### US-010 Escalate an important question
As an **Employee**, I want to send my question to the right person with the context, so that I do not need to explain everything again. *(FR-030, FR-031)*

- **Given** the assistant could not answer, **when** I click "Ask a person", **then** the contact receives my question, the conversation, and the sources found.

### Contextual Escalation Journey

```mermaid
flowchart TD
    subgraph TRIGGER ["1. User Intent (US-010)"]
        CLICK["<b>Employee Clicks 'Ask a Person'</b><br/>Triggered when answer is missing or query is critical"]
    end

    subgraph BUNDLE ["2. Automated Context Packaging"]
        B1["<b>Original Question</b>"]
        B2["<b>Full Chat Transcript</b>"]
        B3["<b>Attempted Citations / Source References</b>"]
        
        CLICK --> B1
        CLICK --> B2
        CLICK --> B3
    end

    subgraph DISPATCH ["3. Targeted Human Routing"]
        ROUTER{"<b>Identify Category</b>"}
        HR["<b>HR Specialist</b><br/>Leaves, harassment, benefits"]
        IT["<b>IT Desk</b><br/>Hardware, VPN, software access"]
        FIN["<b>Finance Desk</b><br/>Reimbursements, salary"]
        
        B1 & B2 & B3 --> ROUTER
        ROUTER -->|"HR Query"| HR
        ROUTER -->|"Tech Issue"| IT
        ROUTER -->|"Expense Issue"| FIN
    end

    style TRIGGER fill:#111827,stroke:#f87171,stroke-width:1px,color:#ffffff
    style BUNDLE fill:#111827,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style DISPATCH fill:#111827,stroke:#4ade80,stroke-width:1px,color:#ffffff

    style CLICK fill:#3f1418,stroke:#f87171,stroke-width:2px,color:#ffffff
    style B1 fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style B2 fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style B3 fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style ROUTER fill:#3b2413,stroke:#fbbf24,stroke-width:2px,color:#ffffff
    style HR fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style IT fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style FIN fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
```

---

## Epic C: Manage Knowledge

### US-020 Upload documents
As an **Admin**, I want to upload company documents, so that employees get answers from them. *(FR-010, FR-012)*

- **Given** I upload a PDF, **when** processing finishes, **then** its status is "Ready" and questions can use it.
- **Given** processing fails, **when** I check the status, **then** I see "Failed" with a reason.

### US-021 Remove outdated documents
As an **Admin**, I want to delete or replace a document, so that employees never get an outdated rule. *(FR-013)*

- **Given** I deleted a document, **when** someone asks about its content, **then** the old content is not used.

### US-022 Control access
As an **Admin**, I want to restrict some documents to certain roles, so that sensitive information stays private. *(FR-014, FR-004)*

### Knowledge Lifecycle & Access Control Flow

```mermaid
flowchart TD
    subgraph UPLOAD ["1. Ingestion Flow (US-020)"]
        UP["<b>Admin Uploads Policy Doc</b><br/>PDF, DOCX, TXT, Markdown"]
        PROC["<b>Async Processing State</b><br/>Parsing • Chunking • Embedding"]
        READY["<b>Status: Ready</b><br/>Immediately active for employee questions"]
        FAIL["<b>Status: Failed</b><br/>Detailed error reason shown to admin"]
        
        UP --> PROC
        PROC -->|"Success"| READY
        PROC -->|"Error"| FAIL
    end

    subgraph GOVERN ["2. Access & Lifecycle (US-021 & US-022)"]
        AUTH_TAG["<b>Role-Based Access Control (US-022)</b><br/>Restricted documents only answer queries from permitted roles"]
        PURGE["<b>Document Deletion / Replacement (US-021)</b><br/>Old document deleted $\rightarrow$ Chunks immediately expelled from search"]
    end

    READY --> AUTH_TAG
    READY --> PURGE

    style UPLOAD fill:#111827,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style GOVERN fill:#111827,stroke:#c084fc,stroke-width:1px,color:#ffffff

    style UP fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style PROC fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style READY fill:#142918,stroke:#4ade80,stroke-width:2px,color:#ffffff
    style FAIL fill:#3f1418,stroke:#f87171,stroke-width:2px,color:#ffffff
    style AUTH_TAG fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style PURGE fill:#3f1418,stroke:#ef4444,stroke-width:1px,color:#ffffff
```

---

## Epic D: Understand Usage

### US-030 See knowledge gaps
As an **Admin**, I want to see the questions nobody could answer, so that I know which documents to add. *(FR-051)*

### US-031 See cost and usage
As an **Admin**, I want to see questions, tokens, and cost per day, so that I can control spending. *(FR-050)*

### Admin Analytics & Knowledge Improvement Loop

```mermaid
flowchart TD
    subgraph METRICS ["1. Usage & Cost Telemetry (US-031)"]
        M1["<b>Question Volume</b><br/>Total daily / weekly queries"]
        M2["<b>Token Consumption & Spend</b><br/>LLM tokens and financial cost tracking"]
    end

    subgraph GAPS ["2. Knowledge Gap Discovery (US-030)"]
        LOG["<b>Unanswered Questions Log</b><br/>List of queries that triggered 'I don't know'"]
    end

    subgraph ACTION_LOOP ["3. Feedback Loop & Doc Improvement"]
        ADMIN["<b>Admin Reviews Analytics</b><br/>Spots recurring unanswered questions"]
        UPLOAD_NEW["<b>Author & Upload Missing Policy</b><br/>Knowledge base expands directly addressing user needs"]
        
        ADMIN --> UPLOAD_NEW
    end

    M1 & M2 --> ADMIN
    LOG --> ADMIN

    style METRICS fill:#111827,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style GAPS fill:#111827,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style ACTION_LOOP fill:#111827,stroke:#4ade80,stroke-width:1px,color:#ffffff

    style M1 fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style M2 fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style LOG fill:#3f1418,stroke:#f87171,stroke-width:2px,color:#ffffff
    style ADMIN fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style UPLOAD_NEW fill:#142918,stroke:#4ade80,stroke-width:2px,color:#ffffff
```

---

## Epic E: Account

### US-040 Set up my organization
As a **Company owner**, I want to register my company and invite my team, so that we can start using OpsPilot. *(FR-001, FR-002, FR-003)*

### Organization Onboarding Journey

```mermaid
flowchart TD
    subgraph SETUP ["1. Registration & Provisioning (US-040)"]
        OWNER["<b>Company Owner</b><br/>Registers company account"]
        ORG["<b>Tenant Workspace Created</b><br/>Shared database with tenant-scoped access controls"]
        OWNER --> ORG
    end

    subgraph TEAM ["2. Team Invitation & Roles"]
        INVITE["<b>Send Email Invitations</b>"]
        R_ADM["<b>Admin Role</b><br/>Manage docs & settings"]
        R_EMP["<b>Employee Role</b><br/>Query knowledge base"]
        
        ORG --> INVITE
        INVITE --> R_ADM
        INVITE --> R_EMP
    end

    style SETUP fill:#111827,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style TEAM fill:#111827,stroke:#c084fc,stroke-width:1px,color:#ffffff

    style OWNER fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style ORG fill:#271b3d,stroke:#c084fc,stroke-width:2px,color:#ffffff
    style INVITE fill:#1e293b,stroke:#94a3b8,stroke-width:1px,color:#ffffff
    style R_ADM fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style R_EMP fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
```

---

## Story to Requirement Map

| Story | Requirements |
|---|---|
| US-001 | FR-020, FR-021 |
| US-002 | FR-022 |
| US-003 | FR-023 |
| US-004 | FR-024 |
| US-005 | FR-025 |
| US-010 | FR-030, FR-031 |
| US-020 | FR-010, FR-012 |
| US-021 | FR-013 |
| US-022 | FR-014, FR-004 |
| US-030 | FR-051 |
| US-031 | FR-050 |
| US-040 | FR-001, FR-002, FR-003 |

## Epic F: Onboarding, data control, and support

### US-050 View plan and usage

As an **Admin**, I want to see my organization's plan and usage, so that I understand our limits and costs.

- **Given** my organization has a plan, **when** I open the usage page, **then** I see current usage and plan limits.
- **Given** usage reaches 80% of a limit, **when** I view the page, **then** I see a warning.

### US-051 Complete first-time setup

As a **new Admin**, I want a guided first-run checklist, so that I can set up the workspace and get value quickly.

- **Given** I have just registered, **when** I follow the checklist, **then** I can upload a document, ask a question, and invite a user in under 10 minutes.

### US-052 Export or delete organization data

As an **Admin**, I want to export or delete my organization's data, so that I remain in control of company information.

- **Given** I request an export, **when** it is ready, **then** it contains the organization's documents and conversations.
- **Given** I request deletion, **when** the retention period ends, **then** the organization's data is removed and I receive confirmation.

### US-053 Review the audit log

As an **Admin**, I want to review important actions, so that I can see who changed what and when.

- **Given** an admin action occurs, **when** I open the audit log, **then** I can see the actor, action, and time.

### US-054 Prepare monthly invoice records

As a **Platform owner**, I want monthly invoice records based on each customer's plan and usage, so that I can bill customers accurately.

- **Given** a billing period is complete, **when** I generate the invoice record, **then** I can export it as CSV or PDF.

### US-055 Send feedback or contact support

As a **User**, I want to send feedback or contact support from the application, so that I can report a problem or share a suggestion.

- **Given** I submit a support message, **when** it is accepted, **then** the application confirms receipt and the message reaches the configured support channel.

## Additional story-to-requirement mappings

| Story | Requirements |
|---|---|
| US-050 | FR-060, FR-061 |
| US-051 | FR-062 |
| US-052 | FR-063, FR-064 |
| US-053 | FR-065 |
| US-054 | FR-066 |
| US-055 | FR-067 |
