# 21 — Roadmap Addendum for a Sellable Product

**Status:** Draft v1 | **Last updated:** 2026-10-02
**Amends:** [13 Roadmap](../03-planning/13-roadmap-and-milestones.md), [14 Backlog](../03-planning/14-backlog.md)

> To prepare OpsPilot for sale, add four things to the plan: **(1) decision gates, (2) a customer-discovery track, (3) Phase 8 pilot readiness, and (4) new requirements.** Move Phase 7 (stretch) later.

## 1. Gates (decision points)

| Gate | When (approx., 10 h/week) | Question | Evidence needed | If no |
|---|---|---|---|---|
| **A: Problem validated?** | End of Phase 2 (~Nov 2026) | Does anyone have this problem and want a pilot? | 10+ interviews, 3+ pilot commitments ([18 section 8](18-customer-discovery-plan.md)) | Continue as learning and portfolio project; skip Phase 8 |
| **B: Pilot ready?** | After Phase 5 + deployment tasks (~Mar 2027) | Is it safe, stable, and honest enough for real documents? | Isolation tests, evaluation scores, live URL, backups, pilot agreement, privacy policy | Fix first; do not start pilot |
| **C: Pay?** | After 4-8 weeks of pilot (~Apr-May 2027) | Will pilots pay? | At least 1-2 verbal or written payment commitments | Learn why, adjust, or stop |

**Rule:** Gates stop you from building a product nobody wants. A "no" at a gate is a result, not a failure.

## 2. Tracks

| Track | Content | Hours per week |
|---|---|---|
| Build | Phases from the roadmap | ~8.5 |
| Discovery | Interviews, tracking, outreach (weeks 1-8) | ~1.5 |
| Commercial (after Gate A) | Legal pages, pricing tests, pilot support | included in Phase 8 and pilot weeks |

## 3. Revised phase order

```
0 Setup > 1 Foundation > 2 Basic RAG > [Gate A] > 3 Better RAG > 4 Agents/Escalation > 5 Hardening
  > 6a Deployment (P6-S7, P6-S8) > 8 Pilot readiness > [Gate B] > PILOT
  > 6b Remaining observability > 7 Advanced (driven by customer needs)
```

Changes:
- **Deployment tasks (P6-S7, P6-S8) move before the pilot**, because a pilot needs a live URL with backups.
- **Phase 7 (stretch) moves after the pilot**, and its items are chosen by what customers ask for (for example Bengali support, local model option).
- If interviews show most documents are in Bengali, **pull the Bengali experiment (P7-S4) forward into Phase 3** and raise FR-026 from Could to Should.

### Revised effort

| Part | Hours |
|---|---|
| Phases 0-5 | 175.5 |
| 6a deployment (P6-S7, P6-S8) | 10 |
| Phase 8 pilot readiness | 34 |
| Discovery (1.5 h x 8 weeks) | 12 |
| **To pilot-ready** | **231.5** (about 278 h with 20% contingency, about 28 weeks, around late April 2027) |
| 6b observability (rest of Phase 6) | 22 |
| Phase 7 | 37 |

Compared with the previous plan, pilot readiness comes slightly later than "Phase 6 complete" (late March) because commercial work has been added. If you have only 6 hours per week, multiply the estimates by 1.7.

## 4. Requirements added to the product specification

The commercial requirements are integrated into the canonical product documents:

- [Functional requirements](02-functional-requirements.md): FR-060 through FR-067 cover plans, limits, onboarding, export and deletion, audit logs, invoice records, and support contact.
- [Non-functional requirements](03-non-functional-requirements.md): NFR-029 through NFR-033 cover data-location disclosure, backup recovery, email authentication, support response time, and restricted data types.
- [User stories](04-user-stories.md): US-050 through US-055 provide acceptance criteria and traceability for those requirements.

## 5. Architecture changes

- New module **`billing`** (plans, subscriptions, limits). Reads `usage`; chat and admin call it. In `pyproject.toml` add `app.modules.billing` to the layer with `retrieval | escalation`: `"app.modules.retrieval | app.modules.escalation | app.modules.billing"`, and create its folder with `service.py`, `models.py`, `repository.py`.
- New tables: `plans`, `subscriptions` (tenant, plan, status, period), optional `invoices`.
- New ADR: **ADR-0010** object storage (done), **ADR-0011** payment provider (decide after Gate A).
- No new services. Still a modular monolith.

## 6. Phase 8: Pilot readiness (34 h)

| ID | Story | Est | Done when |
|---|---|---|---|
| P8-S1 | `billing` module: plans, subscriptions, limit enforcement (80% warn, 100% block) | 5 | Limits enforced (tests) |
| P8-S2 | Guided onboarding checklist and sample policy document | 4 | New admin completes first run in under 10 minutes (timed with a friend) |
| P8-S3 | Tenant data export | 4 | Export contains documents and conversations |
| P8-S4 | Tenant offboarding and deletion workflow | 3 | Deletion test: no rows or files remain |
| P8-S5 | Audit log and admin viewer | 3 | Key actions listed |
| P8-S6 | Legal pages and consent: Terms, Privacy, upload warning (lawyer-reviewed text) | 3 | Pages live; consent recorded |
| P8-S7 | Email setup: SPF, DKIM, DMARC, transactional templates | 3 | Mail test passes |
| P8-S8 | Uptime monitor, status page, incident runbook | 3 | Alert and status page tested |
| P8-S9 | Manual invoicing flow (usage export) and payment-provider research spike for ADR-0011 | 4 | Invoice CSV; research written |
| P8-S10 | Pilot feedback loop: in-app feedback, weekly call template, pilot dashboard | 2 | Feedback stored and reviewed weekly |

**Exit criteria (Gate B):** [ ] all above [ ] isolation and injection tests green [ ] evaluation scores recorded [ ] live HTTPS URL [ ] backup restored once [ ] security overview and subprocessor list published [ ] pilot agreement ready [ ] employer check done ([20 section 2](20-commercial-readiness-checklist.md)).

## 7. Product-specific risks

| Risk | Mitigation |
|---|---|
| Building for months without a customer | Gate A, discovery track |
| Employer conflict | Section 2 of the commercial checklist, in writing |
| Customer data leak | Four-layer isolation, tests, no salary or personal records |
| Wrong answers damage trust | Citations, "I don't know", evaluation gate |
| LLM cost eats margin | Caps, cache, routing, pricing floor ([19](19-pricing-and-packaging.md)) |
| Payment options limited | Manual invoices first, ADR-0011 |
| Support burden on one person with a job | Honest response times, runbooks, small pilot size (2-3) |
| Big vendors ship the same feature | Narrow wedge (Bengali, local price, escalation), speed with customers |
| Data protection law changes | Ask a lawyer, keep deletion and export, document data flows |

## 8. Product operating rhythm (after pilot starts)

- Weekly: pilot call (20 minutes each), review top unanswered questions, fix one thing customers asked for.
- Monthly: cost and margin review, security patch day, changelog post.
- Quarterly: revisit positioning and pricing with real data.
