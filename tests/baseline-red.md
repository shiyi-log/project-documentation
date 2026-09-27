# RED baseline — before loading `project-documentation`

Date: 2026-09-27
Method: two independent baseline agents received pressure scenarios without the skill.

## Observed failures

- Tiny CLI work stayed near the feature but could miss generated man pages, shell completions, localization, or the repository's documentation-generation path.
- Large infrastructure work recognized blast radius but could introduce an unrequested governance process, ledger, routing matrix, or multi-team approval workflow.
- “Document everything” was correctly recognized as ambiguous, but a typical response could either remain too shallow or expand into an unjustifiably broad rewrite.
- Library API changes could update README/changelog while omitting API reference, compatibility, deprecation, migration, or release-convention documentation.
- Multi-service schema changes could validate a clean database and still omit existing-installation upgrades, migration ordering, service contracts, rollback limits, observability, and data-loss risk.
- A one-line README fix could be expanded into a full docs audit or heavy application/release test run.

## Verbatim rationalizations or baseline language

> “Documentation should stay close to the feature, and the repository’s existing conventions are the source of truth.”

> “The blast radius is large, so documentation must reflect the actual supported workflow and be validated against build automation.”

> “The request is materially ambiguous; documenting everything could mean anything from a README refresh to a full architecture and operations knowledge base.”

> “Do not create a durable ledger unless the user asks for one or the repository already requires it.”

## Skill requirements derived from RED

1. Inspect repository-specific source-of-truth and generated documentation surfaces.
2. Route by actual structure and risk, not owner identity.
3. Keep route, ledger, workflow, and progress mechanisms optional.
4. Separate local/static, integration, deployment, external, release, and production evidence.
5. Treat documentation as part of the deliverable boundary when API, migration, compatibility, operations, or release behavior changes.
