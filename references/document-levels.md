# Document levels

Choose by project complexity and risk, not by whether the owner is an individual or a company.

## Level 1 — basic or single-component

Usually enough:

```text
README.md
setup or quickstart
CHANGELOG.md (if releases matter)
TODO or issue tracker (if follow-up work matters)
```

Merge small documents into README when that is clearer.

## Level 2 — library or multi-module project

Add what applies:

```text
API / usage docs
development / contribution guide
testing guide
architecture or decision notes
data model
```

## Level 3 — long-running or externally used service

Add what applies:

```text
deployment
operations / runbook
monitoring and alerts
backup and recovery
incident response
security and configuration
```

## Level 4 — high-risk or regulated

Add only when justified:

```text
threat model
access control
data retention
audit evidence
compliance
change management
```

Any level can apply to a personal project. Do not create an empty document merely because a level lists it.
