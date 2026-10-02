# 17 — Product Brief and Positioning

**Status:** Draft v1 (hypotheses to validate) | **Last updated:** 2026-10-02

> **Writing guidance:** Separate assumptions from evidence. Every claim in this document is currently a **hypothesis**. Customer discovery ([07](18-customer-discovery-plan.md)) will validate or disprove it.

---

## 1. An honest choice: learning project or product

You want to do two things at once: (1) learn AI engineering and (2) build a SaaS product that can be sold. Both are possible, but there is a major risk:

> **You could spend six months writing code and then discover that nobody will buy the product.** This is a common reason SaaS products fail.

Plan:
1. Build the product and conduct customer discovery **in parallel** (about 1.5 hours per week for discovery).
2. Use **decision gates**: do not make a large investment without strong evidence from customers or a pilot.
3. If discovery shows that companies do not have this problem, keep the project as a **portfolio and learning project**. That is still a valuable outcome; the AI engineering skills you gain will remain useful.

## 2. Product in one paragraph

OpsPilot is a SaaS product where a company uploads its policies and documents. Employees ask questions and receive answers **with sources**. If an answer is unavailable or the issue is critical, the question can be sent to a person with its context. Admins can see which questions went unanswered and how much the service costs.

## 3. Ideal Customer Profile (ICP): hypothesis

| Attribute | Hypothesis (to validate) |
|---|---|
| Company size | 30-300 employees |
| Where | Dhaka-based companies first (same city, easy meetings) |
| Industry | Any with many policies: garments/RMG, logistics, banks/NBFI, telecom/ISP, IT/ITES, NGOs, retail chains |
| Documents | PDF and Word policies, circulars, SOPs; some in Bengali, some in English |
| Pain | HR/admin team answers same questions repeatedly; policy changes not known; new joiners confused |
| Buyer | HR head, admin/operations head, founder or COO |
| Users | All employees |
| Champion | HR executive who is tired of repeated questions |
| Anti-ICP | Very large enterprises (long procurement), 5-person startups (few policies), strictly regulated entities that cannot use cloud AI |

## 4. Problem hypotheses (what may be wrong)

| # | Hypothesis | How we disprove it |
|---|---|---|
| H1 | HR/admin teams spend significant time answering repeated policy questions | Interview: "last week, how many times were you asked X?" |
| H2 | Employees hesitate to ask or cannot find the right person | Interview + short employee survey |
| H3 | Documents exist but are scattered or outdated | Ask to see where documents live |
| H4 | Companies will trust a cloud AI with internal policies (not salary or personal data) | Ask directly about data concerns |
| H5 | Bengali support matters | Ask what language policies and questions are in |
| H6 | Someone has a budget and will pay | Ask what they pay for similar tools; ask for a pilot commitment |
| H7 | Existing tools (shared drive, WhatsApp groups, ChatGPT with uploads) are not good enough | Ask what they tried |

## 5. Competitive landscape (categories, not claims)

| Category | Examples (check yourself, do not copy claims) | Why a customer might still choose OpsPilot (hypothesis) |
|---|---|---|
| General AI assistants with file upload or custom assistants | ChatGPT, Claude, Copilot | Admin control, citations, role access, escalation, usage per company |
| Enterprise search and knowledge platforms | Glean-type tools | Price and simplicity for 30-300 employee companies |
| Wiki tools with AI | Notion, Confluence | Customers whose policies live in PDF and Word, not in a wiki |
| HR software with chatbot add-ons | HRIS vendors | Works with any documents, not only inside one HR system |
| DIY | Open-source RAG projects | Customers without engineers |

**Honest note:** large players move fast on generic features. Your wedge must be **narrow**, something big players do not prioritize.

### Candidate wedges (validate with interviews)

1. **Bengali and mixed Bengali-English policy documents** (needs FR-026 Bengali support, currently a Could).
2. **Local price and local payment** (BDT, simple plans).
3. **Escalate to a human with context** (the original problem you described).
4. **Admin sees knowledge gaps** (which questions have no answer yet).
5. **10-minute setup** for non-technical HR.
6. **Data location and privacy clarity** for local companies.

Pick **one or two** after discovery. Do not claim all.

## 6. Positioning statement (fill after discovery)

```
For [HR / operations teams at 30-300 employee companies in Bangladesh]
who [lose time answering the same policy questions],
OpsPilot is [an AI policy assistant]
that [gives employees cited answers from the company's own documents and escalates to a person when needed],
unlike [general chatbots and wikis]
because [wedge 1] and [wedge 2].
```

## 7. Product principles

1. **Trust over cleverness:** every answer cites sources, or says "I don't know".
2. **Admin stays in control:** what is uploaded, who sees it, what it costs.
3. **Privacy by design:** tenant isolation, no document content in logs.
4. **Simple first:** a non-technical HR person can start in 10 minutes.
5. **Honest limits:** show confidence, do not pretend to make HR or legal decisions.

## 8. Product metrics

| Metric | Definition | Target (initial hypothesis) |
|---|---|---|
| Activation | Admin uploads at least 3 documents and employees ask at least 10 questions in week 1 | 60% of pilot companies |
| Weekly active employees | Employees asking at least 1 question per week / invited employees | 30% |
| Answer rate | Questions with a cited answer / all questions | 80% |
| Helpfulness | Thumbs up / rated answers | 75% |
| Escalation rate | Escalated / all questions | under 10% |
| Gross margin per customer | (Revenue - LLM - infrastructure) / revenue | see [19](19-pricing-and-packaging.md) |

## 9. Non-goals (for the first customers)

- Enterprise SSO, custom contracts, on-premise deployment
- Handling salary or personal employee records
- Replacing HR or legal decisions
