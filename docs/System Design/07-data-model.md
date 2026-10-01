# 07 — Data Model

**Status:** Approved v2 (reference) | **Last updated:** 2026-10-01

---

## 1. Principles

1. Every tenant-owned table has `tenant_id uuid NOT NULL`.
2. One PostgreSQL database; each **module owns its tables** (see [06](06-architecture.md)). Other modules use the owner's service, not direct queries.
3. UUID primary keys; `created_at` and `updated_at` on every table.
4. Soft delete for documents (`deleted_at`); chunks of deleted documents are removed by a cleanup job.
5. Isolation enforced by Postgres row-level security (RLS), see [10](10-security-and-tenancy.md).
6. Migrations with Alembic; backward compatible (add first, remove later).

### Multi-Tenant Data Isolation & RLS Security Boundary

```mermaid
flowchart TD
    subgraph TENANT_ROOT ["Tenant Root Entity"]
        TENANT["<b>tenants (id: UUID)</b><br/>Root of data isolation & monthly token quota"]
    end

    subgraph ISOLATED_TABLES ["Tenant-Isolated Tables (Every row has tenant_id)"]
        T_USERS["<b>users & invitations</b><br/>email unique per tenant"]
        T_DOCS["<b>documents & categories</b><br/>soft-deleted with deleted_at"]
        T_CHUNKS["<b>document_chunks</b><br/>HNSW vector embeddings & tsvector"]
        T_CHAT["<b>conversations & messages</b><br/>session turns, tokens & citations"]
        T_ACT["<b>pending_actions & escalations</b><br/>HITL approval state machine"]
        T_USE["<b>usage_events & audit_logs</b><br/>financial token tracking"]
    end

    subgraph RLS_GATE ["PostgreSQL Row-Level Security Engine (Fail-Closed)"]
        SESSION["<b>SET LOCAL app.tenant_id = :current_tenant</b>"]
        CHECK{"<b>tenant_id = NULLIF(current_setting('app.tenant_id'), '')::uuid</b>"}
        
        SESSION --> CHECK
        CHECK -- "Match" --> OK["<b>Rows Returned (Isolated to Tenant)</b>"]
        CHECK -- "No match or NULL" --> FAIL["<b>Zero Rows Returned (Fails Closed)</b>"]
    end

    TENANT --> T_USERS & T_DOCS & T_CHAT & T_ACT & T_USE
    T_DOCS --> T_CHUNKS
    ISOLATED_TABLES -.->|"Guarded by RLS policy"| RLS_GATE

    style TENANT_ROOT fill:#111827,stroke:#c084fc,stroke-width:2px,color:#ffffff
    style ISOLATED_TABLES fill:#111827,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style RLS_GATE fill:#111827,stroke:#4ade80,stroke-width:2px,color:#ffffff

    style TENANT fill:#271b3d,stroke:#c084fc,stroke-width:2px,color:#ffffff
    style T_USERS fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style T_DOCS fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style T_CHUNKS fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style T_CHAT fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style T_ACT fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style T_USE fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style SESSION fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style CHECK fill:#3b2413,stroke:#fbbf24,stroke-width:2px,color:#ffffff
    style OK fill:#142918,stroke:#4ade80,stroke-width:2px,color:#ffffff
    style FAIL fill:#3f1418,stroke:#ef4444,stroke-width:2px,color:#ffffff
```

---

## 2. Entity Relationships

```mermaid
erDiagram
    TENANTS ||--o{ USERS : "has members"
    TENANTS ||--o{ DOCUMENTS : "owns"
    TENANTS ||--o{ CONVERSATIONS : "owns"
    TENANTS ||--o{ ESCALATION_CONTACTS : "configures"
    TENANTS ||--o{ USAGE_EVENTS : "records"
    
    DOCUMENTS ||--o{ DOCUMENT_CHUNKS : "split into"
    USERS ||--o{ CONVERSATIONS : "starts"
    CONVERSATIONS ||--o{ MESSAGES : "contains"
    CONVERSATIONS ||--o{ ESCALATIONS : "context for"
    CONVERSATIONS ||--o{ PENDING_ACTIONS : "proposes"
    
    MESSAGES ||--o{ CITATIONS : "references"
    MESSAGES ||--o| FEEDBACK : "rated by"
    DOCUMENT_CHUNKS ||--o{ CITATIONS : "cited by"

    TENANTS {
        uuid id PK
        string name
        string slug
        int monthly_token_cap
        string status
        timestamp created_at
    }

    USERS {
        uuid id PK
        uuid tenant_id FK
        string email
        string password_hash
        string role
        string status
    }

    DOCUMENTS {
        uuid id PK
        uuid tenant_id FK
        string title
        uuid category_id FK
        string storage_key
        string content_hash
        string status
        string[] allowed_roles
        timestamp deleted_at
    }

    DOCUMENT_CHUNKS {
        uuid id PK
        uuid tenant_id FK
        uuid document_id FK
        int ordinal
        text content
        int page
        string section
        vector embedding
        tsvector tsv
        string[] allowed_roles
    }

    CONVERSATIONS {
        uuid id PK
        uuid tenant_id FK
        uuid user_id FK
        string title
        timestamp created_at
    }

    MESSAGES {
        uuid id PK
        uuid tenant_id FK
        uuid conversation_id FK
        string role
        text content
        boolean answered
        int input_tokens
        int output_tokens
        int latency_ms
    }

    CITATIONS {
        uuid id PK
        uuid tenant_id FK
        uuid message_id FK
        uuid chunk_id FK
        int page
        string section
        float score
    }

    PENDING_ACTIONS {
        uuid id PK
        uuid tenant_id FK
        uuid conversation_id FK
        string type
        jsonb payload
        string status
        timestamp expires_at
    }

    ESCALATIONS {
        uuid id PK
        uuid tenant_id FK
        uuid conversation_id FK
        uuid contact_id FK
        string status
        timestamp created_at
    }

    USAGE_EVENTS {
        uuid id PK
        uuid tenant_id FK
        uuid user_id FK
        string model
        int input_tokens
        int output_tokens
        decimal cost_usd
    }
```

---

## 3. Tables by Owning Module

| Module | Table | Key columns | Notes |
|---|---|---|---|
| identity | `tenants` | id, name, slug, monthly_token_cap, status | Root of isolation |
| identity | `users` | id, tenant_id, email (unique per tenant), password_hash, role (`admin`/`employee`), status | One tenant per user in v1 |
| identity | `refresh_tokens` | id, tenant_id, user_id, token_hash, expires_at, revoked_at, replaced_by | Rotation, reuse detection |
| identity | `invitations` | id, tenant_id, email, role, token_hash, expires_at, accepted_at | |
| documents | `document_categories` | id, tenant_id, name | HR, IT, Finance |
| documents | `documents` | id, tenant_id, title, category_id, source_type, storage_key, source_url, content_hash, status, failure_reason, allowed_roles, deleted_at | `content_hash` prevents duplicates; changing `allowed_roles` also updates chunk roles in the same transaction |
| ingestion | `ingestion_jobs` | id, tenant_id, document_id, status, attempts, error, started_at, finished_at | Job state, retries |
| ingestion | `document_chunks` | id, tenant_id, document_id, ordinal, content, page, section, allowed_roles, embedding, embedding_model, tsv, token_count | Search table |
| chat | `conversations` | id, tenant_id, user_id, title | |
| chat | `messages` | id, tenant_id, conversation_id, role, content, status (`complete`/`failed`/`cancelled`), answered (bool), no_answer_reason, model, input_tokens, output_tokens, latency_ms | One row per turn; `answered=false` rows feed knowledge gaps (FR-051) |
| chat | `citations` | id, tenant_id, message_id, document_id, chunk_id, page, section, score | |
| chat | `feedback` | id, tenant_id, message_id, rating, comment | |
| escalation | `escalation_contacts` | id, tenant_id, category_id, name, email | |
| escalation | `escalations` | id, tenant_id, conversation_id, user_id, contact_id, status, delivery_status | |
| agent | `pending_actions` | id, tenant_id, conversation_id, type, payload jsonb, status, expires_at | `proposed`, `confirmed`, `rejected`, `executed`, `failed`, `expired` |
| usage | `usage_events` | id, tenant_id, user_id, kind, model, input_tokens, output_tokens, cost_usd | Source for dashboard and caps |
| core | `audit_logs` | id, tenant_id, actor_id, action, target, created_at | Who did what |

---

## 4. Key DDL (Reference)

```sql
CREATE TABLE documents (
  id             uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id      uuid NOT NULL REFERENCES tenants(id),
  title          text NOT NULL,
  category_id    uuid REFERENCES document_categories(id),
  source_type    text NOT NULL CHECK (source_type IN ('upload','url')),
  storage_key    text,
  source_url     text,
  content_hash   text NOT NULL,
  status         text NOT NULL CHECK (status IN ('uploaded','processing','ready','failed')),
  failure_reason text,
  allowed_roles  text[] NOT NULL DEFAULT '{admin,employee}',
  created_at     timestamptz NOT NULL DEFAULT now(),
  updated_at     timestamptz NOT NULL DEFAULT now(),
  deleted_at     timestamptz,
  UNIQUE (tenant_id, content_hash)
);
CREATE INDEX ON documents (tenant_id, status);

CREATE TABLE document_chunks (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       uuid NOT NULL,
  document_id     uuid NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
  ordinal         int  NOT NULL,
  content         text NOT NULL,
  page            int,
  section         text,
  allowed_roles   text[] NOT NULL,
  embedding       vector(1024) NOT NULL,  -- dimension depends on the embedding model
  embedding_model text NOT NULL,
  tsv             tsvector GENERATED ALWAYS AS (to_tsvector('english', content)) STORED,
  token_count     int,
  UNIQUE (document_id, ordinal)
);
CREATE INDEX ON document_chunks USING hnsw (embedding vector_cosine_ops);
CREATE INDEX ON document_chunks USING gin (tsv);
CREATE INDEX ON document_chunks (tenant_id, document_id);

-- Row-level security (repeat for every tenant-owned table)
ALTER TABLE document_chunks ENABLE ROW LEVEL SECURITY;
ALTER TABLE document_chunks FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON document_chunks
  USING (tenant_id = NULLIF(current_setting('app.tenant_id', true), '')::uuid)
  WITH CHECK (tenant_id = NULLIF(current_setting('app.tenant_id', true), '')::uuid);
```

If `app.tenant_id` is not set, the policy compares with NULL and returns **no rows** (fails closed). The application connects with a **non-owner database role**; `FORCE ROW LEVEL SECURITY` also applies the policy to the table owner. Migrations run with a separate privileged role.

Login lookup (find a user by email before the tenant is known) needs a controlled exception: a `SECURITY DEFINER` function or a separate narrowly scoped role. Design this in Phase 1 and test it.

---

## 5. Query Patterns and Indexes

| Query | Index |
|---|---|
| Vector search for one tenant, filtered by role | HNSW on `embedding` plus tenant and role filter |
| Keyword search | GIN on `tsv` |
| List documents by status | `(tenant_id, status)` |
| Conversation history | `messages(conversation_id, created_at)` |
| Usage per day | `usage_events(tenant_id, created_at)` |

> Filtered vector search may return fewer relevant rows when the filter removes many candidates. Test recall on the evaluation set in Phase 3.

---

## 6. Lifecycle and Retention

| Data | Rule |
|---|---|
| Document deleted | Mark `deleted_at`, remove chunks, remove file after grace period |
| Conversations | Kept until user or tenant deletes |
| Usage events | Keep 13 months (assumption) |
| Refresh tokens | Delete after expiry |
| Tenant deletion | Delete all rows by `tenant_id` and all files |

### Document Lifecycle & Async Retention Flow

```mermaid
flowchart TD
    subgraph INGESTION ["1. Ingestion State Machine"]
        UPLOAD["<b>Uploaded</b><br/>Raw file saved to MinIO & row inserted"]
        PROC["<b>Processing</b><br/>Celery worker parsing, chunking & generating embeddings"]
        READY["<b>Ready</b><br/>Chunks & HNSW vectors committed; searchable"]
        FAIL["<b>Failed</b><br/>Error reason recorded; retry backoff"]

        UPLOAD --> PROC
        PROC -->|"Success"| READY
        PROC -->|"Exhausted error"| FAIL
    end

    subgraph DELETION ["2. Soft-Delete & Async Cleanup"]
        DEL_REQ["<b>Admin Deletes Document</b><br/>Sets deleted_at = now()"]
        SEARCH_EX["<b>Immediate Search Exclusion</b><br/>All search queries filter WHERE deleted_at IS NULL"]
        CLEANUP["<b>Async Cleanup Worker</b><br/>1. Hard-deletes document_chunks<br/>2. Evicts semantic cache<br/>3. Purges binary from MinIO storage"]

        READY --> DEL_REQ
        DEL_REQ --> SEARCH_EX
        SEARCH_EX --> CLEANUP
    end

    style INGESTION fill:#111827,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style DELETION fill:#111827,stroke:#f87171,stroke-width:1px,color:#ffffff

    style UPLOAD fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style PROC fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style READY fill:#142918,stroke:#4ade80,stroke-width:2px,color:#ffffff
    style FAIL fill:#3f1418,stroke:#f87171,stroke-width:2px,color:#ffffff
    style DEL_REQ fill:#3b2413,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style SEARCH_EX fill:#142918,stroke:#4ade80,stroke-width:1px,color:#ffffff
    style CLEANUP fill:#3f1418,stroke:#ef4444,stroke-width:2px,color:#ffffff
```

---

## 7. Open Decisions (Resolved in the Named Phase)

| Decision | Phase |
|---|---|
| Embedding model and dimension | 2 (experiment) |
| Chunk size and overlap | 3 (experiment) |
| Keyword search language configuration (English first, Bengali later) | 7 |
