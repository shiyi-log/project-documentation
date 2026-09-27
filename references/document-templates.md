# Document templates

Use the smallest template that answers the request. Replace placeholders; do not leave `TBD` or invented facts in a final document.

## README / entry point

```markdown
# Project name

## Purpose
What problem this solves.

## Current status
What is usable, what is partial, and what is not implemented.

## Quick start
Commands and prerequisites verified for the stated environment.

## Scope
Included and explicitly out of scope.

## More documentation
Links to setup, architecture, API, operations, or security docs when they exist.
```

## Architecture

```markdown
# Architecture

## Context and scope
System boundary and audience.

## Components and data flow
Modules, dependencies, and important state transitions.

## Contracts and source of truth
APIs, schemas, generated artifacts, or code that owns each rule.

## Failure and recovery
Timeouts, retries, partial success, rollback limits, and operator actions.

## Verification and limits
What was checked, what was not run, and what remains uncertain.
```

## Runbook

```markdown
# Runbook

## Preconditions
Environment, permissions, dependencies, and configuration.

## Start / stop / deploy
Commands with expected results.

## Health and logs
Where to check status and what signals matter.

## Failure and recovery
Safe diagnosis, rollback, repair, and escalation.

## Backup and data loss
Recovery point, recovery time, irreversible actions, and limits.
```

## Decision record

```markdown
# Decision: <short title>

## Context
What forced a choice.

## Decision
What is selected.

## Alternatives
What was considered and rejected.

## Consequences
Benefits, costs, limits, and follow-up.
```
