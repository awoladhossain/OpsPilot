# ADR-0002: Tenant isolation with shared tables and row-level security

- **Status:** Proposed (reference)
- **Date:** 2026-10-01

---

### Tenancy Architecture & RLS Defense-in-Depth

```mermaid
flowchart TD
    subgraph OPTIONS ["1. Tenancy Model Comparison"]
        O1["<b>Option 1: Database-per-Tenant</b><br/>Max isolation • Extremely heavy ops • Complex migrations & pooling"]
        O2["<b>Option 2: Schema-per-Tenant</b><br/>High isolation • Repetitive migrations per schema • Connection routing complexity"]
        O3["<b>Option 3: Shared Tables + RLS (CHOSEN)</b><br/>Single DB & schema • Minimal ops • DB-level security enforcement"]
    end

    subgraph DEFENSE ["2. Defense-in-Depth RLS Enforcement Flow"]
        REQ["<b>Incoming API Request</b><br/>Authenticated JWT with tenant_id: 'org_alpha'"]
        
        subgraph APP_LEVEL ["Layer 1: Application Filter"]
            APP["<b>ORM / Query Builder</b><br/>Injects WHERE tenant_id = 'org_alpha'"]
        end

        subgraph DB_LEVEL ["Layer 2: PostgreSQL Row-Level Security (RLS)"]
            CTX["<b>Session Variable Set</b><br/>SET LOCAL app.current_tenant = 'org_alpha'"]
            RLS{"<b>Postgres RLS Policy Engine</b><br/>USING (tenant_id = current_setting('app.current_tenant'))"}
            
            PASS["<b>Row Accessible</b><br/>Matches 'org_alpha' only"]
            BLOCK["<b>Access Physically Refused</b><br/>Blocked at engine level even if app query has a bug"]

            CTX --> RLS
            RLS -- "Matches" --> PASS
            RLS -- "Different Tenant" --> BLOCK
        end

        REQ --> APP
        APP --> CTX
    end

    style OPTIONS fill:#111827,stroke:#fbbf24,stroke-width:1px,color:#ffffff
    style DEFENSE fill:#111827,stroke:#38bdf8,stroke-width:2px,color:#ffffff
    style APP_LEVEL fill:#111827,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style DB_LEVEL fill:#111827,stroke:#4ade80,stroke-width:1px,color:#ffffff

    style O1 fill:#1e293b,stroke:#94a3b8,stroke-width:1px,color:#ffffff
    style O2 fill:#1e293b,stroke:#94a3b8,stroke-width:1px,color:#ffffff
    style O3 fill:#142918,stroke:#4ade80,stroke-width:2px,color:#ffffff

    style REQ fill:#271b3d,stroke:#c084fc,stroke-width:1px,color:#ffffff
    style APP fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style CTX fill:#1e293b,stroke:#38bdf8,stroke-width:1px,color:#ffffff
    style RLS fill:#3b2413,stroke:#fbbf24,stroke-width:2px,color:#ffffff
    style PASS fill:#142918,stroke:#4ade80,stroke-width:2px,color:#ffffff
    style BLOCK fill:#3f1418,stroke:#ef4444,stroke-width:2px,color:#ffffff
```

---

## Context
OpsPilot serves many companies. A leak between companies is the worst failure (NFR-010). The team is one person with a small budget, expected load is 10 tenants with up to 10,000 chunks each.

## Options considered
1. **Database per tenant:** strongest isolation, most operations work (migrations, backups, connections).
2. **Schema per tenant:** strong isolation, migrations repeated for every schema.
3. **Shared tables with `tenant_id` and row-level security (RLS).**

## Decision
Use **shared tables with `tenant_id` and Postgres RLS**, plus application filters and automated isolation tests.

## Why
- One migration path, one backup, fits solo operation.
- RLS makes the database refuse cross-tenant reads even if application code has a bug.
- Enough for the v1 load.

## Consequences
- **Good:** simple operations, easy cross-tenant admin reporting for the platform owner.
- **Bad / trade-offs:** a mistake in policy or connection role breaks isolation; noisy neighbour risk; filtered vector search needs recall testing.
- **Follow-up:** isolation test in CI; revisit if an enterprise customer requires a dedicated database.

## Related
NFR-010, FR-004, [10 Security and tenancy](../10-security-and-tenancy.md)
