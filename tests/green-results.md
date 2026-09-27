# GREEN results — after loading `project-documentation`

Date: 2026-09-27
Method: two fresh-context agents read the skill and relevant references; no files or upstream repositories were modified.

## Confirmed behavior

- A tiny CLI change was routed as a bounded README/CLI-contract update; architecture, operations, security, ledger, formal workflow, and progress files were omitted.
- A large infrastructure change was routed through implementation, build scripts/CI, authoritative build docs, compatibility, and proportionate validation; a lightweight ledger and progress state were recommended rather than forced.
- “Document everything” was treated as ambiguous; the agents requested audience and lifecycle scope before editing.
- A public library API change was routed through API docs, compatibility/migration notes, tests/examples, and release notes rather than README-only documentation.
- A multi-service schema/boundary change was routed through migration, service contracts, deployment order, rollback limits, runbook, generated artifacts, and separate evidence levels.
- A one-line README correction was kept to a one-line static change with no route file, ledger, workflow, or progress system.

## Remaining loopholes found

- A changelog can claim a behavior change while API semantics or compatibility guidance remain stale.
- A migration that works on a clean database does not prove upgrades for existing installations.
- Code rollback can be possible while data rollback is destructive or lossy.
- “Release documentation prepared”, a local build, or a passing unit test does not prove publication or production acceptance.

These loopholes are addressed by the current skill rules and quality checklist.
