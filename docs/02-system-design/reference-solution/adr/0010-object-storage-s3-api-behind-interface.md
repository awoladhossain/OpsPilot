# ADR-0010: Object storage through an S3-API interface; do not depend on MinIO

- **Status:** Accepted (mentor recommendation). Replaces the earlier assumption of MinIO.
- **Date:** 2026-10-02

## Context
Uploaded documents must be stored outside the database. Earlier design assumed MinIO. Research on 2 Oct 2026 shows MinIO's community edition stopped publishing Docker images and binaries in October 2025, entered maintenance mode in December 2025, and the repository was archived in April 2026. Existing builds still work, but new projects should not start on it.

## Options considered
1. **MinIO (archived community edition or a community fork).**
2. **SeaweedFS** (open source, S3 API, single container for development).
3. **Garage** (lightweight, needs a configuration file).
4. **Managed S3-compatible service** (cloud object storage) for production.

## Decision
- Application code talks to an internal **`FileStorage` interface** using the **S3 API** (never a vendor-specific SDK).
- **Local development:** SeaweedFS container (`server -s3`).
- **Production:** choose later (Phase 6): managed S3-compatible storage if the budget allows, otherwise SeaweedFS on the server.
- Tests use a fake or temporary-directory implementation.

## Why
- The interface protects us from another vendor change; swapping storage becomes configuration.
- SeaweedFS is actively maintained and starts with one command.
- A managed service removes backup and disk management from a solo operator.

## Consequences
- **Good:** no lock-in, simple tests, clear upgrade path.
- **Bad / trade-offs:** local SeaweedFS runs without authentication unless configured (never expose it); one more thing to verify in Phase 6.
- **Follow-up:** pick production storage in Phase 6; consider data location when customers ask where data is stored (see commercial readiness checklist).

## Related
FR-010, NFR-014, NFR-025, [06 Architecture](../06-architecture.md)
