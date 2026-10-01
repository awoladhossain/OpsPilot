# How to Write Project Docs — Beginner to Professional

> Read this guide repeatedly. Whenever someone asks you to "write requirements" or "write a design doc", follow this guide.
> No need to apologize: nobody is born knowing how to write documentation. It is an engineering discipline developed through deliberate practice.

---

## 1. Why Write Documentation?

```mermaid
graph LR
  subgraph Cost ["Relative Cost to Fix a Requirement Mistake"]
    direction LR
    A["📝 In Documentation<br><b>~5 Minutes</b>"] --> B["📐 In System Design<br><b>~1 Hour</b>"]
    B --> C["💻 During Implementation<br><b>~1–2 Days</b>"]
    C --> D["🚨 In Production<br><b>~5+ Days</b>"]
  end
  style A fill:#e6f4ea,stroke:#137333,stroke-width:2px
  style D fill:#fce8e6,stroke:#c5221f,stroke-width:2px
```

1. **Clarifies your own thinking.** Wherever you get stuck while writing is an area you don't fully understand yet. That is a great signal because you caught it before writing code.
2. **Helps others understand.** Recruiters, teammates, or even yourself 3 months from now.
3. **Catches mistakes cheaply.** Fixing an ambiguity in documentation takes 5 minutes. Fixing it after writing code, tests, and database migrations takes 5 days.

**In technical interviews:** *"I first defined the problem, scoped the requirements, and then derived the architecture."* This immediately demonstrates senior engineering maturity.

---

## 2. Requirements vs. Design (The Most Common Confusion)

```mermaid
flowchart TD
  subgraph Step1 ["Step 1: Requirements (The 'WHAT' & 'WHY')"]
    direction TB
    R1["🎯 Problem Definition"]
    R2["👤 User Needs & Stories"]
    R3["⚙️ Functional Capabilities"]
    R4["📊 Non-Functional Targets (p95, SLA, Costs)"]
    R1 --> R2 --> R3 --> R4
  end

  subgraph Step2 ["Step 2: Architecture & Design (The 'HOW')"]
    direction TB
    D1["🧩 Components & Containers"]
    D2["🗄️ Database Schemas & Models"]
    D3["🔌 APIs, Queues & Caches"]
    D4["🛠️ Tech Stack (FastAPI, Redis, Postgres)"]
    D1 --> D2 --> D3 --> D4
  end

  Step1 ==>|Drives & Informs| Step2
  style Step1 fill:#f8f9fa,stroke:#1a73e8,stroke-width:2px
  style Step2 fill:#f8f9fa,stroke:#ea4335,stroke-width:2px
```

| Dimension | Requirements (Step 1) | Architecture & Design (Step 2) |
|---|---|---|
| **Core Question** | **What** needs to be done? **Why**? | **How** will we build it? |
| **Example** | *"User can upload a PDF and see processing status"* | *"PDF is uploaded to S3, parsed asynchronously by Celery"* |
| **Language** | User-focused domain language, zero technology names | Components, databases, APIs, network protocols, specific libraries |
| **Focus** | Capabilities, business constraints, quality targets | Architecture diagrams, component flow, schemas, tech stack |

> [!TIP]
> **The Litmus Test:** If a line mentions specific tools like FastAPI, Postgres, Redis, Celery, or React, it belongs in **Design**, not Requirements. Never put technology names in requirements documents.

---

## 3. 7 Golden Rules of Documentation

```mermaid
mindmap
  root((7 Golden Rules))
    Single Responsibility
      One file = One purpose
      Separate problem from design
    Specific Metrics
      Avoid vague words
      Always use numbers e.g. p95 < 2s
    Audience Awareness
      Recruiter wants 30s clarity
      Engineers want actionable specs
    Scannability
      One sentence = One idea
      Short paragraphs, tables, bullets
    Single Source of Truth
      Link instead of copy-pasting
      Avoid duplicate definitions
    Empirical Assumptions
      Concrete estimates e.g. 100 concurrent chats
      Flag unknowns as assumptions
    Iterative Evolution
      Living documents in Git
      Rough draft > Blank page
```

1. **One file = one responsibility.** Separate problems, requirements, and design into distinct files.
2. **Be specific; avoid vague words like "good/fast/secure".**
   - ❌ Bad: *"System should be fast."*
   - ✅ Good: *"First token appears within 2 seconds for 95% of chat requests (p95 < 2s)."*
3. **Think about the reader.** Who is reading? What do they need to know? A hiring manager wants to understand your project in 30 seconds.
4. **Use short sentences, bullet points, and tables.** One sentence = one idea. Dense paragraphs rarely get read.
5. **Single source of truth.** Writing the same information in two places leads to outdated docs. Use links instead.
6. **Use concrete numbers.** Instead of "many users", specify "100 concurrent users". If unknown, state it as an "assumption" to be calibrated later.
7. **Drafts will be rough—start anyway.** Commit to Git, iterate, and improve. Documentation is a living document.

---

## 4. How to Write: The 5-Step Process

```mermaid
flowchart LR
  S1["1. Brain Dump<br><i>(10 min freeform)</i>"] --> S2["2. Group<br><i>(Categorize themes)</i>"]
  S2 --> S3["3. Structure<br><i>(Apply headings)</i>"]
  S3 --> S4["4. Rewrite<br><i>(Crisp English)</i>"]
  S4 --> S5["5. Review<br><i>(Audit checklist)</i>"]

  style S1 fill:#f1f3f4,stroke:#5f6368
  style S2 fill:#e8f0fe,stroke:#1a73e8
  style S3 fill:#fef7e0,stroke:#f9ab00
  style S4 fill:#e6f4ea,stroke:#137333
  style S5 fill:#ceead6,stroke:#0d652d,stroke-width:2px
```

1. **Brain dump (10 min):** Write down whatever is in your head without worrying about structure. Just get all thoughts out on paper.
2. **Group:** Categorize ideas by themes (problem, users, pain points, proposed solution).
3. **Structure:** Map content into standard template headings (using the files in this folder).
4. **Rewrite:** Polish with clear, concise sentences in simple English. (Professional English docs ensure recruiters and open-source contributors can easily read your repository on GitHub.)
5. **Review:** Evaluate your document against the checklist in Section 9.

---

## 5. Key Terms & Traceability

```mermaid
flowchart LR
  Actor["👤 Actor / Persona<br><i>(Role: Employee)</i>"] --> Story["📖 User Story<br><i>(US-001: As a... I want...)</i>"]
  Story --> FR["⚙️ Functional Req<br><i>(FR-020: System must...)</i>"]
  FR --> AC["✅ Acceptance Criteria<br><i>(Given... When... Then...)</i>"]
  FR --> ADR["📑 ADR<br><i>(Architectural Decision)</i>"]

  style Actor fill:#fce8e6,stroke:#c5221f
  style Story fill:#e8f0fe,stroke:#1a73e8
  style FR fill:#fef7e0,stroke:#f9ab00
  style AC fill:#e6f4ea,stroke:#137333
  style ADR fill:#f3e8fd,stroke:#9334e6
```

| Term | Meaning | Example |
|---|---|---|
| **Actor / Persona** | Who uses the system (a user role) | Admin, Employee |
| **Functional Requirement (FR)** | **What** the system must do | *"User can upload a PDF"* |
| **Non-Functional Requirement (NFR)** | **How** the system performs (speed, security, cost) | *"p95 latency < 2s"* |
| **MoSCoW** | Prioritization: **M**ust, **S**hould, **C**ould, **W**on't (this version) | Login = Must, Voice = Won't |
| **User Story** | A feature described from the user's perspective | *"As an Employee, I want..., so that..."* |
| **Acceptance Criteria (AC)** | Conditions that verify a feature is "done" | Given / When / Then |
| **Scope** | What is included and what is excluded | In scope / Out of scope |
| **Assumption** | Presumed facts that haven't been validated yet | *"Company has fewer than 500 documents"* |
| **Constraint** | Non-negotiable boundaries or limitations | Solo developer, limited budget |
| **Risk** | Potential failure modes and their mitigations | Hallucinations, prompt injection |
| **ADR** | Architecture Decision Record: what was decided and why | *"pgvector instead of Qdrant"* |

---

## 6. Copy-Ready Sentence Patterns

| Doc | Pattern |
|---|---|
| **Problem** | `[Who] cannot [do what] because [why], which causes [impact].` |
| **Functional Req** | `The user can [action] [object] [condition].` |
| **Non-Functional Req** | `[Quality]: [metric] [target] under [condition].` |
| **User Story** | `As a [role], I want [action], so that [benefit].` |
| **Acceptance Criteria** | `Given [context], When [action], Then [result].` |
| **ADR** | `Context (situation) > Decision (action taken) > Consequences (trade-offs).` |

---

## 7. Bad vs. Good Examples

| Bad | Why it's bad | Good |
|---|---|---|
| *"System should be secure."* | Cannot be objectively verified | *"A user from Company A can never retrieve Company B's documents (verified by automated test)."* |
| *"Chat will work fast."* | What does "fast" mean? | *"First token within 2s for 95% of requests."* |
| *"AI answers questions."* | Under what conditions? What if it's wrong? | *"The system answers only from uploaded documents and shows citations. If no source found, it says 'I don't know'."* |
| *"Use FastAPI and pgvector."* (in requirements) | This is an implementation detail (design) | *"Answers are retrieved based on semantic meaning, not exact keywords."* |
| *"Admin can manage everything."* | Too broad and ambiguous | *"Admin can upload, delete, and tag documents."* |
| A long paragraph containing 5 disparate ideas | Hard to read and digest | 5 focused bullet points |

---

## 8. Recommended Document Writing Order

```mermaid
flowchart TD
  P01["01 Problem Statement<br><i>Why are we building this?</i>"]
  P04["04 User Stories<br><i>Who wants what? (Personas & Needs)</i>"]
  P02["02 Functional Req (FR)<br><i>What will the system do? (Derived from stories)</i>"]
  P03["03 Non-Functional Req (NFR)<br><i>How well must it perform? (Speed, Cost, Scale)</i>"]
  P05["05 Scope & Risks<br><i>What is in/out of scope, and what could go wrong?</i>"]
  PADR["Architecture Decision Records (ADR)<br><i>Key technology choices & trade-offs</i>"]
  PREADME["README.md<br><i>Written last; serves as the repository storefront</i>"]

  P01 ==> P04
  P04 ==> P02
  P02 ==> P03
  P03 ==> P05
  P05 ==> PADR
  PADR ==> PREADME

  style P01 fill:#e8f0fe,stroke:#1a73e8,stroke-width:2px
  style P04 fill:#e8f0fe,stroke:#1a73e8,stroke-width:2px
  style P02 fill:#fef7e0,stroke:#f9ab00,stroke-width:2px
  style P03 fill:#fef7e0,stroke:#f9ab00,stroke-width:2px
  style P05 fill:#fce8e6,stroke:#ea4335,stroke-width:2px
  style PADR fill:#f3e8fd,stroke:#9334e6,stroke-width:2px
  style PREADME fill:#e6f4ea,stroke:#137333,stroke-width:2px
```

> [!NOTE]
> While the numerical naming is 01 through 05, drafting **04 (User Stories) before 02 (Functional Requirements)** makes writing requirements significantly easier, since requirements naturally derive from real user stories.

---

## 9. Self-Review Checklist

- [ ] Can a newcomer understand what the doc is about in 1 minute?
- [ ] Are vague adjectives ("fast, easy, good, secure") backed by quantitative metrics?
- [ ] Are technology names excluded from requirements files?
- [ ] Does every requirement have an ID (e.g. FR-001) and priority?
- [ ] Does every "Must" requirement have clear acceptance criteria?
- [ ] Is duplicate information avoided (linked rather than repeated)?
- [ ] Are non-goals / out-of-scope boundaries clearly defined?
- [ ] Are Status and Last Updated date specified at the top?
- [ ] Are formatting and spelling validated in Markdown preview?

---

## 10. Markdown Cheatsheet

````markdown
# Heading 1
## Heading 2
**bold**   *italic*   `inline code`
- bullet
1. numbered
- [ ] checkbox  /  - [x] done
[link text](https://example.com)

| Col A | Col B |
|---|---|
| a | b |

> Quote / note

```python
code block
```

```mermaid
graph LR
  A[Client] --> B[API]
```
````
*(In VS Code, press `Ctrl+Shift+V` to open preview. GitHub renders Mermaid diagrams natively).*

---

## 11. Common Beginner Mistakes

1. **Writing design into requirements** (e.g., specifying "Use FastAPI").
2. **Overscoping:** Marking every feature as "Must". Keep "Must" to 30–40% maximum.
3. **NFRs without numbers:** Writing "fast" or "secure" without measurable targets.
4. **Perfectionism blocking progress:** An ugly draft is infinitely better than a blank page.
5. **Abandoning docs after writing:** Keep docs updated whenever architecture or code changes.
6. **Omitting non-goals:** Without explicit non-goals, scope creep prevents the project from ever finishing.

---

## 12. Complete Documentation Folder Structure

```mermaid
graph TD
  Root["📁 opspilot/"]
  Root --> README["📄 README.md (Storefront)"]
  Root --> Docs["📁 docs/"]
  
  Docs --> D00["📄 00-how-to-write-docs.md"]
  Docs --> D01["📄 01-problem-statement.md"]
  Docs --> D02["📄 02-functional-requirements.md"]
  Docs --> D03["📄 03-non-functional-requirements.md"]
  Docs --> D04["📄 04-user-stories.md"]
  Docs --> D05["📄 05-scope-assumptions-risks.md"]
  
  Docs --> ADR["📁 adr/ (Architecture Decisions)"]
  ADR --> A00["📄 0000-template.md"]
  ADR --> A01["📄 0001-vector-storage-for-document-search.md"]
  ADR --> A02["📄 0002-tenant-isolation-shared-tables-rls.md"]
  ADR --> A03["📄 0003-modular-monolith-not-microservices.md"]
  ADR --> A04["📄 0004-async-ingestion-with-queue.md"]
  ADR --> A05["📄 0005-hybrid-retrieval-with-rerank.md"]

  Docs --> SysDes["📁 System Design/"]
  SysDes --> SD06["📄 06-architecture.md"]
  SysDes --> SD07["📄 07-data-model.md"]
  SysDes --> SD08["📄 08-api-design.md"]
  SysDes --> SD09["📄 09-key-flows.md"]
  SysDes --> SD10["📄 10-security-and-tenancy.md"]
  SysDes --> SD11["📄 11-deployment-and-observability.md"]

  Docs --> CodeSet["📁 Code setup/"]
  CodeSet --> CS12["📄 12-traceability-and-design-review.md"]
  CodeSet --> CS13["📄 13-roadmap-and-milestones.md"]
  CodeSet --> CS14["📄 14-backlog.md"]
  CodeSet --> CS15["📄 15-working-agreements.md"]
  CodeSet --> CS16["📄 16-learning-checkpoints.md"]

  style Root fill:#f8f9fa,stroke:#202124,stroke-width:2px
  style Docs fill:#e8f0fe,stroke:#1a73e8,stroke-width:2px
  style ADR fill:#f3e8fd,stroke:#9334e6,stroke-width:1px
  style SysDes fill:#fef7e0,stroke:#f9ab00,stroke-width:1px
  style CodeSet fill:#e6f4ea,stroke:#137333,stroke-width:1px
```
