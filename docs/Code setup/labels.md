# GitHub labels (create these in the repo)

| Label | Meaning |
|---|---|
| `type:task` | Small piece of work |
| `type:spike` | Time-boxed experiment |
| `type:bug` | Defect |
| `type:docs` | Documentation or ADR |
| `phase:0` ... `phase:7` | Phase the work belongs to |
| `priority:must` | Must have |
| `priority:should` | Should have |
| `priority:could` | Could have |
| `area:identity` | identity module |
| `area:documents` | documents module |
| `area:ingestion` | ingestion and worker |
| `area:retrieval` | retrieval |
| `area:llm` | LLM gateway |
| `area:chat` | chat |
| `area:agent` | agent and actions |
| `area:escalation` | escalation |
| `area:admin` | admin and usage |
| `area:infra` | compose, CI/CD, deployment |
| `area:observability` | metrics, logs, traces |
| `area:eval` | evaluation |
| `blocked` | Waiting on something |

## Board columns

`Backlog` > `Ready` > `In progress` (WIP limit 2) > `In review` > `Done`

## Milestones

Create one GitHub Milestone per phase (`Phase 0 Setup` ... `Phase 7 Advanced`) with the due date from the roadmap.

## Where to put the files

- `ISSUE_TEMPLATE/*.md` into `.github/ISSUE_TEMPLATE/`
- `pull_request_template.md` into `.github/`
