# 20 — Commercial Readiness Checklist

**Status:** Draft v1 | **Last updated:** 2026-10-02

> **Important:** I am not a lawyer or accountant. This checklist identifies **questions to ask**; it is not legal or tax advice. Bangladesh's laws, taxes, and payment rules can change. Consult a lawyer and chartered accountant before making major decisions.
> The payment and data-protection information from online research was checked on **2 October 2026** and must be verified again.

---

## 1. Readiness gates: what is needed at each stage

| Stage | Requires |
|---|---|
| Discovery interviews | Nothing from this list except section 2 |
| Demo to prospects | Demo environment with fake documents |
| Private pilot (free) | Sections 2, 3 (pilot note), 4 (basic), 5 (basic), 7 |
| First paying customers | All sections |

## 2. Employment and intellectual property (resolve this first)

You work full time as an AI Engineer at DATAZLY. Before selling the product:

- [ ] **Read your offer letter and company policies.** Your offer letter contains a confidentiality clause that prohibits sharing company information. I did not see a separate moonlighting or intellectual-property clause in the offer-letter text reviewed here. Read the **full employment agreement, handbook, and policies** if available.
- [ ] Ask HR or your manager, and request a written answer: "May I work on a personal project or side business? Are there restrictions? Who owns the intellectual property?"
- [ ] Use **separate devices and accounts** where possible. **Never** use company laptops, repositories, data, or client data.
- [ ] Do not approach an employer's customer or prospect when the business overlaps.
- [ ] Check for a **conflict of interest**. Be especially careful if DATAZLY also sells AI knowledge assistants.
- [ ] Keep written records of the answers and decisions.

## 3. Business and tax basics (Bangladesh)

- [ ] Discuss the business structure (sole proprietorship with a trade license or a private limited company) with an accountant. The choice affects customers, payment gateways, and legal liability.
- [ ] Trade license, TIN, business bank account.
- [ ] Ask an accountant whether VAT/BIN registration is required based on revenue.
- [ ] Invoice format ar bookkeeping (even simple spreadsheet).
- [ ] Ask whether any incentives or registrations apply to the software and IT sector.

## 4. Contracts and policies to prepare (lawyer review)

| Document | Purpose | Needed for |
|---|---|---|
| Terms of Service | Rules of use, liability limits, termination | Paid customers (pilot: short version) |
| Privacy Policy | What data, why, where, who sees | Before any real user data |
| Data Processing Agreement (DPA) | You process customer's employee data on their behalf | Before customer uploads documents |
| Acceptable Use Policy | No illegal content, no personal-record uploads | Paid |
| Pilot agreement / NDA | Confidentiality, 60-day scope, deletion right | Pilot |
| SLA (simple) | Availability goal, support response (do not promise 24/7) | Paid |
| Subprocessor list | LLM provider, hosting, email, storage | Public page |

Draft these documents from a lawyer's template or a reputable open template, then have a lawyer **review them**.

## 5. Data protection (Bangladesh)

Research summary (verify): Bangladesh's **Personal Data Protection Ordinance, 2025** was approved by the cabinet in October 2025 and gazetted in November 2025 together with a National Data Governance Ordinance. Reports describe: consent requirements, rights to access, correct, and delete data, breach notification, special protection for sensitive data (health, financial and similar), and limits on **transferring data outside Bangladesh**. It was issued as an ordinance, so **ask a lawyer about its current status, final text, and effective rules.**

What it means for OpsPilot (design and process):

- [ ] You will send employee-company documents to an **overseas LLM provider**: check cross-border transfer rules, disclose it in the Privacy Policy and DPA, list providers as subprocessors, and prefer provider settings with no training on your data.
- [ ] **Do not accept salary, medical, or personal employee records in v1.** Say it in the Acceptable Use Policy and onboarding screen. Policies and SOPs only.
- [ ] Offer **data location** information honestly: where is hosting, where do model calls go. Consider a local-hosting or local-model option later if customers demand it (Phase 7 model server helps).
- [ ] **Deletion and export** per tenant (Phase 8 tasks).
- [ ] **Breach response plan**: who you notify, in what time, template message.
- [ ] Log hygiene: no document content in logs (already NFR-014).
- [ ] Find out whether you must register or appoint anyone under the ordinance.

## 6. Billing and payments

Research summary (verify): several 2026 sources state **Stripe does not accept businesses registered in Bangladesh**. Options people use:

| Option | Notes |
|---|---|
| **Manual invoice + bank transfer or mobile wallet** (bKash, Nagad and similar) | Zero code, perfect for first customers in Dhaka |
| **Local payment gateways** (for example SSLCommerz and similar) | Verify onboarding, fees, subscription support, requirements |
| **Merchant of Record platforms** (Paddle, Lemon Squeezy, Dodo Payments) | For international customers; they handle tax. Sources mention onboarding friction for founders in Bangladesh and vendor blogs are biased, so verify directly |
| **Foreign entity + Stripe** | Needs a legal entity abroad; expensive and complex; only with advice |

**Mentor decision:** first customers via **manual invoices**. Do not write payment code before the first paying customer. Decide the provider in **ADR-0011** after Gate A (target segment = local or international?).

## 7. Security and trust package

Customers will ask. Prepare **before** pilots:

- [ ] **Security overview** (1 page): isolation (RLS), encryption in transit and at rest, access control, logging, backups.
- [ ] **Data flow diagram** (reuse the architecture container diagram, simplified).
- [ ] **Subprocessor list** (LLM, embedding, hosting, email, storage).
- [ ] Encryption at rest for database and storage volumes, HTTPS everywhere.
- [ ] Backups and a tested restore (Phase 6).
- [ ] Admin **audit log** (who uploaded or deleted what).
- [ ] **Incident response plan**: detect, contain, notify, learn.
- [ ] **Vulnerability disclosure**: `security@` mailbox and a short policy.
- [ ] Dependency and image scans in CI (NFR-015).
- [ ] Independent penetration test before big customers (later, paid).

## 8. Support and operations

- [ ] Support mailbox and a ticket log.
- [ ] Response-time promise you can keep (suggest: 1 business day; **no 24/7 promise** while you are one person with a job).
- [ ] **Uptime monitor and public status page.**
- [ ] Runbooks: service down, queue stuck, LLM provider down, disk full, restore from backup.
- [ ] Maintenance windows and customer notice.
- [ ] Customer onboarding checklist and a "first 30 days" email.
- [ ] Feedback loop: weekly pilot call, in-app feedback.

## 9. Product readiness

- [ ] Self-serve onboarding for admin (sample document, guided first question).
- [ ] **Tenant data export and deletion** (offboarding).
- [ ] Plans, limits, and usage view (Phase 8).
- [ ] Transactional email deliverability: **SPF, DKIM, DMARC**.
- [ ] Help pages: how to upload, supported formats, privacy FAQ.
- [ ] Changelog.
- [ ] Abuse prevention: rate limits, upload limits, tenant suspension.

## 10. Go-to-market basics (small)

- [ ] One-page website: problem, how it works, trust (privacy), contact.
- [ ] 2-minute demo video (recorded at end of each phase).
- [ ] Pilot pipeline sheet (from [18](18-customer-discovery-plan.md)).
- [ ] Case study template for first pilots.
- [ ] Where customers gather: HR communities, LinkedIn groups, alumni networks.

## 11. Money controls

- [ ] Spending cap and alerts on every LLM provider account.
- [ ] Per-tenant token caps (already designed, NFR-009).
- [ ] Monthly cost review: LLM, server, email, domain, monitoring.
- [ ] Separate business bank account and simple bookkeeping.
