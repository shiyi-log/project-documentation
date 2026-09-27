# Route map

Routing is an optional decision aid. It explains why a documentation task takes a particular path; it is not a mandatory workflow or a requirement to create a route file.

## Route key

```text
<intent>.<project_profile>.<artifact>.<risk>.<evidence>
```

### Intent

`create`, `update`, `review`, `audit`, `migrate`, `archive`

### Project profile

`basic`, `library`, `multi_module`, `service`, `platform`, `infra`, `regulated`

### Artifact

`readme`, `setup`, `architecture`, `api`, `data`, `ops`, `security`, `changelog`, `decision`

### Risk and evidence

Risk: `low`, `medium`, `high`, `regulated`
Evidence: `static`, `test`, `runtime`, `external`, `production`

## Routing priority

1. User's explicit goal and scope.
2. Authorized actions and forbidden side effects.
3. Actual repository structure, source, configuration, tests, and existing docs.
4. Lifecycle, risk, external dependencies, and audience.
5. The authoritative source for the rule.
6. Default templates.

Never infer the route from “personal project” or “enterprise project” alone.

## Upgrade signals

Suggest a higher-risk route when the task touches databases, migrations, payment, privacy, production, chain operations, multiple services, external authoritative docs, compatibility, generated artifacts, release publication, or regulated data.

For behavior changes, route beyond the presentation surface:

```text
implementation → public contract/API → compatibility/migration → generated docs → tests → release/operations
```

Do not assume a README or changelog is the authoritative source merely because it is easy to edit.

## Downgrade signals

Use a smaller route when the task is a one-line wording correction, a single-file low-risk note, or a clearly bounded update with no behavior or operational impact.

## Output example

```text
route: update.service.data.high.runtime
authority: migration source + service contract + deployment guide
docs: must update migration/upgrade notes; may update architecture; README out of scope
ledger: recommended because the migration is persistent and rollback-sensitive
progress: in-progress
next: inspect existing migration and upgrade-order documentation
```
