# 18 — Customer Discovery Plan

**Status:** Draft v1 | **Last updated:** 2026-10-02

> Goal: **Validate that the problem is real and that someone will pay for a solution**, both before and during development. Conduct 10–15 conversations.

## 1. Time and timing

- Spend about **1.5 hours per week** (from a 10-hour weekly capacity). This reduces development time by about 15%, which is a worthwhile investment.
- **Weeks 1–8** (while Phases 0–2 are underway): conduct 10–15 interviews.
- **Gate A (after Phase 2, around November):** make a decision based on the interviews (see section 7).

## 2. Who to talk to

| Segment | How to reach |
|---|---|
| HR managers/executives, admin/ops managers | LinkedIn, friends and family working in companies, university alumni and IT club network |
| Founders of 30-300 employee companies | Referrals; ask every person "who is the HR head in your company?" |
| Your own past colleagues | Ask what policies confused them |

Rules:
- **Do not approach your employer's clients or customers**, and do not use any employer data or relationships (see the employment section of the [commercial readiness checklist](20-commercial-readiness-checklist.md)).
- Target: **10 conversations with decision makers or HR**, not only friends.

## 3. Outreach message (copy and edit)

**English (LinkedIn):**
> Hi [Name], I'm a software engineer in Dhaka working on tools that help HR/admin teams answer repeated employee questions about company policies. I'm not selling anything, just researching. Could I ask you 5-6 questions about how this works in your company? 20 minutes, whenever convenient.

**English (WhatsApp/message):**
> Hello [Name], I am a software engineer researching a tool to help company HR and admin teams answer employees' questions about company policies. I am not selling anything; I would like to learn from your experience. Would you have 20 minutes for a conversation?

## 4. Interview rules (The Mom Test)

1. Ask about **past behavior**, not future opinions. Ask "What happened the last time?" rather than "Would you use this tool?"
2. Do not pitch during the first 20 minutes.
3. Treat compliments as neither evidence nor commitment.
4. Look for specific evidence: numbers, examples, tools, time, and money.
5. Do not rush to fill silence; give the person time to think.
6. End by asking for a concrete commitment: a pilot, an introduction, or more time.

## 5. Interview script (30 minutes)

**Opening (2 min):** Introduce yourself and explain, "I am researching, not selling."

**Context (5 min)**
1. What is your role, and how many employees work at your company?
2. Which documents or tools do you use for policies and HR work (shared drives, WhatsApp, email, HRIS)?

**Behavior (10 min)**
3. What policy question did an employee ask most recently? What happened?
4. About how often do these questions come up in a week, and who asks them?
5. Who answers, and how long does it take?
6. When was an answer last wrong or out of date? What happened?
7. What do employees do when they cannot find an answer?
8. What process do you use to help new employees?

**Solutions tried (5 min)**
9. Have you tried to solve this (with an FAQ, chatbot, ChatGPT, or training)?
10. What did not work?

**Constraints (5 min)**
11. What languages are the documents written in (Bengali, English, or a mix)?
12. What concerns would the company have about putting documents in the cloud? Are there documents that must never be shared?
13. What tools does the company pay for in this area, and who approves the spending?

**Closing (3 min)**
14. Who else would be useful to speak with about this?
15. If I offered a small pilot, could you try it for two weeks with three or four documents?

## 6. Signal table

| Strong signal | Weak signal (ignore) |
|---|---|
| Specific recent example with numbers | "Yes this sounds useful" |
| They already tried to solve it (spent time or money) | "Maybe in the future" |
| They offer an introduction, documents, or time | Only compliments |
| A budget owner is identified | "I'll check with someone" with no name |
| They ask when they can use it | Asks only about features |

## 7. Tracking sheet (one row per conversation)

| Date | Name/Role | Company size | Industry | Problem seen? (Y/N + quote) | Frequency | Tools used | Language | Data concerns | Budget owner | Next step | Pilot interest (0-3) |
|---|---|---|---|---|---|---|---|---|---|---|---|

## 8. Decision at Gate A (after 10 conversations)

| Result (heuristic, not law) | Decision |
|---|---|
| 5+ describe the problem unprompted AND 3+ want a pilot AND 1+ identifies budget | Proceed: build for pilots, add Phase 8 (pilot readiness) |
| Problem is real but only in one niche (for example garments HR) | Narrow ICP, adjust features and wording |
| Problem is mild or nobody wants a pilot | Continue as portfolio and learning project, skip commercial work |
| Concern is data privacy | Prioritize privacy features and hosting story, or consider other buyer segments |

## 9. Pilot offer (use when interest is strong)

```
OpsPilot pilot (free, 60 days)
- 1 admin and up to 30 employees
- You provide 5-10 real policy documents (we sign a simple confidentiality note)
- Weekly 20-minute feedback call
- You can stop and request deletion of all data at any time
- If it works for you: discounted founding-customer price
- In return: honest feedback, and permission to use an anonymous case study
```

Before pilots start, read [20 section 4 and 7](20-commercial-readiness-checklist.md).
