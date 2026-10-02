# ADR-0009: Agent built with LangGraph; tools only propose actions

- **Status:** Accepted (mentor recommendation); verify current framework documentation at the start of Phase 4
- **Date:** 2026-10-01

## Context
The assistant should do more than answer: draft emails, propose tickets, escalate, query read-only data. Risks: prompt injection and unintended side effects (NFR-012, FR-041).

## Options considered
1. **Hand-written loop calling the LLM and tools.**
2. **LangGraph (explicit graph of steps, state, and human-in-the-loop support).**
3. **Higher-level agent framework with more automation.**

## Decision
Build the agent with **LangGraph**, with explicit states, a small set of typed tools, and a hard rule: **tools never perform side effects; they create a `pending_action`.** Execution happens only after user confirmation in normal application code.

## Why
- Explicit graph makes behaviour inspectable, testable, and traceable.
- Human-in-the-loop fits the confirmation requirement.
- Relevant skill for AI engineering roles.
- Propose-only design limits the damage of prompt injection.

## Consequences
- **Good:** safer agent, clear audit trail, evaluable tool selection.
- **Bad / trade-offs:** framework learning curve and API changes over time; more structure than a simple loop.
- **Follow-up:** agent evaluation set (tool selection accuracy) in Phase 4; keep a thin adapter so the framework can be replaced.

## Related
FR-040..042, NFR-012, [09 Flow 4](../09-key-flows.md)
