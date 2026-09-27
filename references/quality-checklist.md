# Quality checklist

Use proportionately. A one-line wording fix may need only a diff and link check; a migration or production runbook needs much more.

## Scope and routing

- [ ] Audience and requested boundary are clear.
- [ ] The selected docs answer the request.
- [ ] Out-of-scope docs are not changed.
- [ ] The authoritative source is identified.
- [ ] External documentation is labeled as external and dated when relevant.

## Truth and completeness

- [ ] Current facts are separated from plans and assumptions.
- [ ] Commands, paths, ports, versions, examples, and links were checked.
- [ ] Failure, recovery, rollback, compatibility, and dependency notes are present when applicable.
- [ ] Generated docs or schemas are synchronized when applicable.
- [ ] Public API changes include compatibility, migration, deprecation, or release guidance when applicable.
- [ ] Schema changes distinguish clean-install tests from existing-installation upgrades.
- [ ] Code rollback is distinguished from data rollback, especially for destructive migrations.
- [ ] Release preparation is distinguished from actual tag, package, deployment, or production publication.
- [ ] `not-run`, `blocked`, `partial`, and `not-implemented` boundaries are explicit.

## Safety

- [ ] No secrets, tokens, cookies, private keys, passwords, or raw personal data.
- [ ] No unauthorized deployment, remote write, credential change, or production claim.
- [ ] No false claim from HTTP 200, build success, or a local-only test.

## Optional coordination

- [ ] Route key is exposed when it improves clarity.
- [ ] Ledger is suggested only when it reduces risk or improves reuse.
- [ ] Workflow and progress are compressed or omitted for low-risk work.
- [ ] If used, the final state and next step are clear.
