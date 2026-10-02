# ADR-0007: Thin internal LLM gateway with fallback

- **Status:** Accepted (mentor recommendation)
- **Date:** 2026-10-01

## Context
The system calls LLM and embedding providers. Providers fail, change prices, and models change. Requirements: provider independence (NFR-025), fallback on failure (NFR-017), token and cost tracking (NFR-008).

## Options considered
1. **Call provider SDKs directly from business code.**
2. **A thin internal interface (`LLMClient`) with one implementation per provider, plus fallback, timeout, retry, and usage accounting.**
3. **A third-party multi-provider library as the gateway.**

## Decision
Build the **thin internal gateway** (option 2) first. It also wraps every call with timeouts, retries, usage events, and tracing. Evaluate a third-party library later, behind the same interface.

## Why
- Teaches the real problems (timeouts, retries, streaming, cost accounting) instead of hiding them.
- Business code never imports a provider SDK, so swapping is a configuration change.
- One place to add caching, routing, and guardrails.

## Consequences
- **Good:** testable (fake provider in tests), easy fallback and routing later.
- **Bad / trade-offs:** some code to maintain; provider-specific features need mapping.
- **Follow-up:** choose the primary provider in Phase 1 and the embedding model in Phase 2.

## Related
NFR-008, NFR-017, NFR-025
