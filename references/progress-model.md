# Progress model

Progress tracking is optional. Use it when a task spans multiple files, depends on external checks, needs handoff, or has meaningful blocked/not-run states. Do not create a progress system for a trivial edit.

## Task states

```text
unscoped → routed → in-progress → review → verification → complete
                         ├→ blocked
                         ├→ not-implemented
                         ├→ not-run
                         └→ cancelled
```

`complete` means the agreed task boundary is satisfied. It does not mean the whole project, production deployment, or external acceptance is complete.

## Skill implementation stages

```text
design
→ route-map
→ references
→ skill-body
→ RED baseline
→ GREEN verification
→ REFACTOR
→ GitHub validation
→ release
```

Keep implementation progress separate from a user project’s feature progress. “Skill body exists” is not “skill is validated”.

## Evidence labels

Use precise labels:

- `verified`: the stated check actually ran and produced supporting evidence;
- `not-run`: the check was not attempted;
- `blocked`: a prerequisite prevented the check;
- `planned`: intended but not implemented;
- `partial`: only part of the requested boundary was checked.

If progress is omitted, provide a concise status and next step in the final response.
