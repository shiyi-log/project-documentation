# Contributing

Thank you for improving `project-documentation`.

## Scope

Keep changes focused on reusable project-documentation guidance. Do not turn optional routing, ledgers, workflows, or progress tracking into mandatory ceremony.

## Before opening a pull request

Run:

```bash
python3 tests/validate_skill.py
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
git diff --check
```

For behavior-shaping changes, add or update a pressure scenario and record the observed baseline, the improved behavior, and any remaining loophole.

## Content expectations

- Keep current facts separate from plans and assumptions.
- Use proportionate guidance for small and large projects.
- Avoid secrets and private data.
- Preserve explicit `not-run`, `blocked`, and `partial` boundaries.
- Prefer a narrow correction over a broad rewrite.
