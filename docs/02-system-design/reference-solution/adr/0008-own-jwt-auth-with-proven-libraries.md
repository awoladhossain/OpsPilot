# ADR-0008: Own JWT authentication with proven libraries

- **Status:** Accepted (mentor recommendation)
- **Date:** 2026-10-01

## Context
SaaS needs registration, login, invitations, roles, and tenant-aware tokens. Learning goal includes understanding authentication end to end. Security quality matters (NFR-011).

## Options considered
1. **External identity provider (managed or self-hosted).**
2. **Own implementation: short-lived JWT access token, rotating refresh token, Argon2 hashing, built on proven libraries.**

## Decision
Implement **own authentication** with proven libraries for JWT and hashing. Do not write cryptography. Refresh tokens are stored hashed, rotated on use, with reuse detection.

## Why
- Full understanding of the flow, directly useful for interviews and the day job.
- Tenant claim in the token integrates with RLS (ADR-0002).
- Small scope: no social login, no SSO in v1.

## Consequences
- **Good:** full control and learning value.
- **Bad / trade-offs:** security responsibility sits with us; no SSO or MFA in v1.
- **Follow-up:** security tests in CI; consider an external provider if SSO becomes a requirement.

## Related
NFR-011, FR-001..003, [10 Security](../10-security-and-tenancy.md)
