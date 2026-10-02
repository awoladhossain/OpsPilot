# OpsPilot documentation

This folder is the single source of truth for OpsPilot documentation. Read the sections in order. The numbered prefixes show the recommended reading sequence.

## 1. Product definition

Start with the problem and requirements, then review product discovery and commercial planning.

1. [Documentation writing guide](01-product/00-writing-documentation.md)
2. [Problem statement](01-product/01-problem-statement.md)
3. [Functional requirements](01-product/02-functional-requirements.md)
4. [Non-functional requirements](01-product/03-non-functional-requirements.md)
5. [User stories](01-product/04-user-stories.md)
6. [Scope, assumptions, constraints, and risks](01-product/05-scope-assumptions-risks.md)
7. [Product brief and positioning](01-product/17-product-brief-and-positioning.md)
8. [Customer discovery plan](01-product/18-customer-discovery-plan.md)
9. [Pricing and packaging](01-product/19-pricing-and-packaging.md)
10. [Commercial readiness checklist](01-product/20-commercial-readiness-checklist.md)
11. [Commercial roadmap addendum](01-product/21-commercial-roadmap-addendum.md)

## 2. System design

Read the design guide, architecture decision, template, then the reference solution. Project decisions are in `decisions/`; example decisions for the reference solution are in `reference-solution/adr/`.

- [System design guide](02-system-design/00-system-design-guide.md)
- [Monolith or microservices decision](02-system-design/01-monolith-or-microservices.md)
- [Design document template](02-system-design/02-design-document-template.md)
- [Reference architecture](02-system-design/reference-solution/06-architecture.md)
- [Reference data model](02-system-design/reference-solution/07-data-model.md)
- [Reference API design](02-system-design/reference-solution/08-api-design.md)
- [Reference key flows](02-system-design/reference-solution/09-key-flows.md)
- [Reference security and tenancy](02-system-design/reference-solution/10-security-and-tenancy.md)
- [Reference deployment and observability](02-system-design/reference-solution/11-deployment-and-observability.md)
- [Traceability and design review](02-system-design/reference-solution/12-traceability-and-design-review.md)

## 3. Project planning

- [Project planning guide](03-planning/00-project-planning-guide.md)
- [Roadmap and milestones](03-planning/13-roadmap-and-milestones.md)
- [Backlog](03-planning/14-backlog.md)
- [Working agreements](03-planning/15-working-agreements.md)
- [Learning checkpoints](03-planning/16-learning-checkpoints.md)
- [GitHub issue and pull request templates](03-planning/github-templates/labels.md)

## 4. Code setup

- [Code setup guide](04-code-setup/00-code-setup-guide.md)

## 5. Templates and decisions

- [Project README template](05-templates/README-template.md)
- [Project ADR template](02-system-design/decisions/0000-template.md)
- [Project architecture decisions](02-system-design/decisions/)
- [Reference solution ADRs](02-system-design/reference-solution/adr/)

The original `opspilot-docs/` folder is retained as an import archive. Use this `docs/` folder for all future reading and edits.
