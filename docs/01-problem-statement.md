# 01 — Problem Statement

**Status:** Draft v1 | **Owner:** Awolad | **Last updated:** 2026-09-30

> **How to write:** In this file, write only the *problem*, not the solution. Pattern:
> `[Who] cannot [do what] because [why], which causes [impact].`
> The ideas from your draft (hesitation, forgetting follow-ups, reaching out to someone else when critical) were good. They have been organized into sections here.
> Rewrite in your own words; this file is just an example.

---

## 1. Background

Every company has rules, policies, and process information: leave policy, IT rules, expense process, onboarding steps. This information is usually spread across PDFs, shared drives, wikis, and chat messages.

## 2. Problem statement

Employees cannot quickly and confidently find the right company rule or information, because it is scattered and the only alternative is to ask a colleague, which causes wasted time, repeated questions, wrong decisions, and delayed work.

## 3. Who is affected

| Who | Pain |
|---|---|
| **Employee** | Does not know whom to ask, hesitates to ask, or finds nobody available |
| **Manager / HR / IT** | Answers the same questions again and again, gets interrupted |
| **Company admin** | Has no idea what employees are confused about |

## 4. Pain points

1. **Hesitation:** Employee feels uncomfortable asking small or repeated questions.
2. **No time / no person:** The right person is busy, absent, or unknown.
3. **Forgotten follow-ups:** A new question comes to mind later, and asking again is awkward.
4. **Scattered information:** Documents exist but nobody knows where.
5. **No path for critical issues:** When a question is important or the answer is missing, there is no clear way to reach the right person with context.

## 5. Current workaround and why it fails

| Workaround | Why it fails |
|---|---|
| Ask a colleague | Interrupts them, inconsistent answers, depends on availability |
| Search shared drive / Ctrl+F in PDF | Slow, keyword-only, easy to miss the right document |
| Read the full handbook | Nobody does |

## 6. Proposed solution (one paragraph, no technology)

OpsPilot is a SaaS application where a company uploads its rules and documents, and employees ask questions in natural language. The system answers **only from the company's documents**, shows **where the answer came from**, and if the answer is missing or the issue is critical, lets the employee **escalate to a responsible person** with the full context.

## 7. Goals

- Employees get correct, sourced answers in seconds without asking a person.
- Employees can escalate critical or unanswered questions with one action.
- Admins can see what employees are asking and which questions have no answer.

## 8. Non-goals (v1)

- Not a general-purpose chatbot (does not answer outside company documents).
- Not a replacement for HR or legal decisions.
- No mobile app, no voice.

## 9. Success metrics

> Numbers below are **initial targets (assumptions)**. Revise after testing.

| Metric | Target | How to measure |
|---|---|---|
| Answer correctness on test questions | >= 85% | Evaluation dataset |
| Answers with correct citation | >= 80% | Evaluation dataset |
| Time to first response | < 2 s (p95) | Metrics dashboard |
| "I don't know" instead of a wrong answer | 100% on out-of-scope test questions | Evaluation dataset |
| Escalation delivered with context | 100% | Automated test |

## 10. Open questions

- Which document types are needed first (PDF only, or DOCX and web pages too)?
- Who receives an escalation: one contact per company or per category (HR, IT, Finance)?
- Should employees be allowed to see every document, or only some?
