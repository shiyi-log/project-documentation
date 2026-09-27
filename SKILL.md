---
name: project-documentation
description: Use when creating, updating, reviewing, organizing, or auditing project documentation such as README files, setup guides, architecture notes, API contracts, data models, runbooks, security notes, changelogs, or documentation standards.
---

# Project Documentation

## Overview

Choose documentation by the project's actual complexity, risk, lifecycle, and audience. The project owner's identity does not determine the documentation level: one person may maintain a large platform, and a team may maintain a tiny utility.

The goal is useful, current, evidence-aware documentation—not a fixed enterprise paperwork set.

## Core rules

- Preserve the user's scope. Do not turn a one-line edit into a documentation audit.
- Separate current facts, verified behavior, plans, assumptions, limits, `not-run`, and `blocked`.
- Use one authoritative source for each rule; link to it instead of copying drift-prone text.
- Document failure, recovery, rollback, compatibility, and external dependencies when they affect the requested scope.
- When behavior, API, schema, migration, generated output, compatibility, or release behavior changes, trace every affected documentation surface instead of updating only README or changelog.
- Never write real secrets, tokens, cookies, private keys, passwords, or unredacted personal data.
- Do not claim “complete”, “verified”, “production-ready”, “safe”, or “recoverable” without matching evidence.
- Route decisions, ledgers, workflows, and progress tracking are recommendations. Use them when they reduce risk or improve reuse; never force them onto trivial work.

## Recommended decision path

Use this path when it helps; compress or skip steps for a small, clear task and say what was omitted.

1. Identify the intent: create, update, review, audit, migrate, or archive.
2. Inspect the existing documentation entry point and the implementation sources that can prove the claim.
3. Classify the project by structure and risk: basic, library, multi-module, service, platform, infrastructure, or regulated.
4. Select only the documents that answer the user's question. Read the relevant reference below.
5. Decide whether a route key, ledger, workflow checklist, or progress status would be useful. They are optional.
6. Write the smallest complete change, then perform proportionate checks on links, commands, examples, tests, generated artifacts, and failure/recovery claims.
7. State the changed files, evidence, limits, unrun checks, and next step. If the task is larger than one turn, provide a lightweight progress state.

## Route and progress output

When routing is useful, expose the decision briefly:

```text
route: <intent>.<project_profile>.<artifact>.<risk>.<evidence>
authority: <repository file, external docs, generated source, or code>
docs: <must update / may update / out of scope>
ledger: <recommended / not needed>
progress: <current state>
next: <smallest safe next step>
```

Read [references/route-map.md](references/route-map.md) for route relationships and upgrade/downgrade signals. Read [references/progress-model.md](references/progress-model.md) only when progress tracking adds value.

## Document selection

Read [references/document-levels.md](references/document-levels.md) when project size or risk is unclear. Read [references/document-templates.md](references/document-templates.md) when creating a new document. Read [references/quality-checklist.md](references/quality-checklist.md) before claiming a documentation task is complete.

## Common mistakes

- Updating only README when an API, migration, generated artifact, or release note is the real authority.
- Updating only a changelog while leaving the API contract, compatibility note, migration guide, or generated docs stale.
- Treating a clean-database migration test as proof that existing installations upgrade safely.
- Treating code rollback as proof that destructive data changes can be rolled back.
- Treating “release notes prepared” or “build passed” as proof that a package or deployment was published.
- Treating a passing unit test, Markdown check, build, or HTTP 200 as proof of deployment, release, production, or business acceptance.
- Forcing a ledger, route matrix, formal workflow, or progress file onto a one-line or one-off change.
- Treating “document everything” as permission to rewrite the repository without first bounding audience and scope.
- Copying stale commands, ports, paths, versions, or configuration examples without checking the source.
