# ADR-0006: pgvector first, benchmark against Qdrant in Phase 3

- **Status:** Accepted for v1; validated in Phase 3
- **Date:** 2026-10-01

## Context
We need vector similarity search with tenant and role filters. Expected size is about 100,000 chunks (NFR-018). A relational database is already required. Learning goal includes understanding dedicated vector databases.

## Options considered
1. **PostgreSQL + pgvector.**
2. **Qdrant (dedicated vector database).**
3. **Managed cloud vector service.**

## Decision
Use **pgvector (HNSW index)** for v1. In Phase 3, benchmark pgvector against Qdrant on the evaluation set (recall, latency with filters, memory) and record the result here.

## Decision matrix (subjective, 1-5)

| Criteria | Weight | pgvector | Qdrant |
|---|---|---|---|
| Operational simplicity (solo) | 5 | 5 | 3 |
| Tenant isolation with RLS | 4 | 5 | 3 |
| Performance at larger scale | 2 | 3 | 5 |
| Learning value | 3 | 3 | 5 |
| **Total** | | **60** | **52** |

## Consequences
- **Good:** one database, transactional consistency, RLS covers vectors.
- **Bad / trade-offs:** filtered search recall and speed at larger scale need testing.
- **Follow-up:** revisit if the benchmark shows a clear gap or data grows past the assumption.

## Related
ADR-0002, ADR-0005, NFR-018
