# project-documentation

`project-documentation` is a Codex skill for creating, updating, reviewing, and auditing project documentation.

It is intentionally adaptive:

- a one-line README correction stays small;
- a library change can route through API, compatibility, migration, and release documentation;
- a multi-service or infrastructure change can surface architecture, data, deployment, recovery, external authority, and validation boundaries;
- a personal developer can use any documentation level when the project is large or risky.

Routing, ledgers, workflows, and progress tracking are optional recommendations, not mandatory ceremony. The hard boundaries are truthful status, scope discipline, secret protection, and honest evidence.

## Install

Copy or symlink this directory to the Codex skills directory:

```text
~/.codex/skills/project-documentation
```

For this repository checkout, the installed path is the directory containing
this README. A fresh Codex session can discover the skill after it is placed
under the user's configured skills directory.

## References

- `references/route-map.md`
- `references/progress-model.md`
- `references/document-levels.md`
- `references/document-templates.md`
- `references/quality-checklist.md`

## Validation

Pressure scenarios and the pre-skill RED baseline are in `tests/`. The GitHub corpus is read-only and covers a CLI, libraries, a multi-service app, a platform, and infrastructure.
