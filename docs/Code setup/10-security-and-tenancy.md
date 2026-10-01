# 10 — Security and Tenancy Design

**Status:** Approved v2 (reference) | **Last updated:** 2026-10-01

## 1. Assets and threats

| Asset | Threat | Control |
|---|---|---|
| Tenant documents | Cross-tenant read | 4-layer isolation (below) |
| Credentials | Theft, brute force | Argon2 password hashing, login rate limit, short-lived access token, rotating refresh token |
| LLM budget | Abuse, runaway cost | Per-user and per-tenant limits, token cap, usage alerts |
| Answers | Prompt injection, hallucination | Section 3, "I don't know" rule, evaluation set |
| Personal data | Leak via logs or LLM provider | Log masking, no document content in logs, provider data settings checked |
| Infrastructure | Exposed ports, vulnerable images | Only reverse proxy public, image scan in CI, secrets in environment |
| Uploaded files | Malicious files, huge files | Type and size validation, parse in worker, never execute content |

## 2. Tenant isolation: 4 layers

1. **Identity:** the access token carries `tenant_id` and `role`. A client can never choose a tenant ID.
2. **Application:** every repository query filters by the tenant from the request context.
3. **Database (RLS):** per request, inside the transaction run `SELECT set_config('app.tenant_id', '<id>', true);`. Policies reject rows of other tenants. The app connects with a **non-owner role**, tables use `FORCE ROW LEVEL SECURITY`, and migrations use another privileged role. The worker sets the tenant from the job payload the same way.
4. **Tests:** an automated test creates two tenants, calls every read endpoint and a retrieval query with tenant A's token, and expects zero rows of tenant B. Runs in CI.

Also: object storage keys prefixed by `tenant_id/`; cache keys include `tenant_id`; log lines include `tenant_id`.

**Known tricky parts to test in Phase 1:** connection pooling (the setting must be transaction-local), login lookup before the tenant is known (controlled exception), background jobs (tenant from payload), admin reporting queries.

## 3. Prompt injection design

A malicious document or user may contain text such as "ignore previous instructions".

| Rule | Implementation |
|---|---|
| Retrieved text is **data, not instructions** | System prompt states this; sources placed in a clearly delimited block |
| No authority from content | Tools and permissions come from the server, never from text |
| No side effects without human confirmation | Agent only proposes actions (Flow 4) |
| Least-privilege tools | Read-only database role for any query tool; allow-listed tables |
| Output checks | Answer grounded in sources; block secrets and system prompt leakage |
| Test | Attack test set (malicious documents and questions) in CI (NFR-012) |

## 4. Authentication and authorization

- Roles: `admin`, `employee`. Checked in route dependencies; role also used as a retrieval filter (`allowed_roles`).
- Access token lifetime ~15 minutes; refresh token rotating, stored hashed, reuse detection revokes the token family.
- Passwords: minimum length, Argon2, never logged.
- Use proven libraries for JWT and hashing; do not write cryptography yourself.
- MCP endpoint (Phase 4) uses the same token model and filters.

## 5. Privacy

- Logs: no document content, no full questions at INFO level; mask emails and IDs where possible.
- LLM provider: document that content is sent to the provider; use settings that disable training on API data; local model option later.
- Tenant deletion removes rows, files, and cached data.
- Audit log for admin actions.

## 6. Secrets and configuration

- Secrets only in environment variables or a secret manager; `.env.example` has names only.
- Secret scanning in CI; no secrets in Docker images.

## 7. Security checks in CI

Dependency audit, Docker image scan (Trivy), secret scan, isolation test, prompt injection test set.
