# 19 — Pricing and Packaging

**Status:** Draft v1 (method and hypotheses; final prices come from customer interviews) | **Last updated:** 2026-10-02

> This document intentionally contains **no final prices**. Prices should not be set by intuition. It explains how to calculate (1) your **cost floor**, (2) the customer's **value**, and (3) suitable **plans and limits**.

## 1. Principles

1. **The floor is your cost plus margin; the ceiling is the customer's value.** Set the price between them.
2. **Simple:** 3 ta plan, ek-line-e bujhano jay.
3. Set **usage limits** (NFR-009), so unusually high usage by one customer does not create a loss.
4. **Charge by a value metric** the customer understands, such as the number of company employees or questions.
5. **Offer early customers a discount, but do not make the product free forever.** Convert to a paid plan after the pilot.

## 2. Cost model (your price floor)

```
Monthly cost per customer =
    LLM cost            (questions x cost per question)
  + embedding cost      (new document tokens x embedding price, mostly one time)
  + infrastructure share (server and services cost / number of customers)
  + payment and platform fees (% of price)
  + support time        (hours x your hourly value)

Floor price = (LLM + embedding + infra share + support) / (1 - target gross margin - fee %)
```

### Example (ALL numbers illustrative, replace with your measurements from Phase 3 and 5)

| Item | Assumption | Result |
|---|---|---|
| Customer size | 50 employees x 20 questions per month | 1,000 questions |
| LLM cost per question | ~$0.0042 (3,000 input and 300 output tokens at illustrative prices, see design guide) | ~$4.2 |
| Infrastructure | $40 per month server shared by 10 customers | $4 |
| Target gross margin | 75% (common SaaS heuristic, not a law) | |
| Payment and platform fee | 4% | |
| **Floor price** | (4.2 + 4) / (1 - 0.75 - 0.04) | **~$39 per month** |

Lessons from the example:
- Infrastructure and LLM are roughly equal here, so **caching and smaller models** (Phase 5, 7) directly improve margin.
- Heavy users (say 5x questions) break the margin, so **question caps per plan** are needed.
- Support time is not in the example; for the first customers it is the biggest hidden cost.

## 3. Value model (your price ceiling)

```
Monthly value = hours saved per month x loaded hourly cost of the people whose time is saved
```

In discovery interviews, ask: "How many hours per week do HR or admin staff spend answering repeated questions?" Estimate the value as those hours multiplied by the loaded hourly cost. You can then explain the comparison to the customer: "This is the monthly cost of that time; this is what I would charge."

### Price-sensitivity questions (ask 5+ customers, Van Westendorp style)
1. At what price would it be **so cheap that you would question its quality**?
2. At what price would it be a **good deal**?
3. At what price would it be **expensive but still affordable**?
4. At what price would it be **too expensive to consider**?

## 4. Packaging (hypothesis, limits tied to cost)

| | Pilot | Starter | Growth | Business |
|---|---|---|---|---|
| Duration | 60 days free | Monthly or annual | Monthly or annual | Annual, custom |
| Employees (invited users) | up to 30 | up to 50 | up to 200 | custom |
| Documents | up to 20 | up to 100 | up to 500 | custom |
| Questions per month | 1,000 | 3,000 | 15,000 | custom |
| Admin analytics | Basic | Yes | Yes | Yes |
| Escalation | Yes | Yes | Yes | Yes |
| Bengali support | If available | If available | If available | If available |
| Support | Weekly call | Email, 1 business day | Email, 1 business day | Agreed |
| Price | Free | **TBD** | **TBD** | **TBD** |

Limits are **placeholders**. Set them from measured cost per question so that a full-limit customer still meets your margin.

## 5. Policies to decide

| Topic | Starting recommendation |
|---|---|
| Overage | Soft limit: warn at 80%, block at 100% with option to upgrade (NFR-009) |
| Annual prepay | Offer a discount; improves cash flow |
| Founding customers | Discounted price locked for a period in exchange for feedback and a case study |
| Refunds | Written in terms: simple, for example pro-rata within 14 days of first payment |
| Currency | Decide per segment (see [20 section 6](20-commercial-readiness-checklist.md)) |
| Price changes | Notice period in terms |

## 6. How billing is built (do not over-build)

1. **First customers: manual invoices** and bank or mobile-wallet payment. Zero integration code.
2. Product only needs: plans, limits, usage, and an invoice export (Phase 8).
3. Integrate a payment provider **after** the first paying customers and after you choose a provider (ADR-0011).
