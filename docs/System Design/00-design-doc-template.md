# [Project Name] — System Design Document

**Status:** Draft | In review | Approved
**Author:** [name] | **Last updated:** YYYY-MM-DD
**Related:** [requirements docs, ADRs]

> **How to write:** Fill out sections in order. If a section is not applicable, write "N/A, because ..." (do not leave it blank). Keep it under 8–12 pages.

## 1. Overview
What are we building and why? (3-5 sentences, link to problem statement)

## 2. Goals and non-goals
- Goals:
- Non-goals:

## 3. Architecture drivers
| Requirement | Impact on design |
|---|---|

## 4. Constraints and assumptions
- Constraints (budget, team, time, hardware):
- Assumptions (to validate):

## 5. Capacity estimation
| Item | Estimate | How computed |
|---|---|---|
| Storage | | |
| Traffic | | |
| Cost | | |
| Latency budget | | |

## 6. System context
(Diagram: actors and external systems)

## 7. Architecture
(Diagram: containers)
| Component | Responsibility | Owns (data) | Technology | Scales by |
|---|---|---|---|---|

Evolution path: v0 / v1 / v2

## 8. Data design
(ER diagram, key tables, tenancy strategy, indexes, retention)

## 9. Key flows
(Sequence diagrams for each must-have story, failure handling table)

| Flow | Failure | Handling |
|---|---|---|

## 10. API design
(Conventions, endpoint table, error format, auth)

## 11. Security and privacy
(Threats and controls)

## 12. Observability
(Metrics, logs, traces, alerts, dashboards)

## 13. Deployment and operations
(Environments, CI/CD, backup, rollback)

## 14. Technology choices
| Area | Choice | Alternatives | ADR |
|---|---|---|---|

## 15. Risks and open questions
| Risk / question | Mitigation / owner |
|---|---|

## 16. Review checklist
- [ ] Every must-have requirement maps to design
- [ ] Every driver has a design response
- [ ] Failure scenarios walked through
- [ ] Every major decision has an ADR
