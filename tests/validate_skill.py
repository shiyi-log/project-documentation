#!/usr/bin/env python3
"""Deterministic packaging checks for the project-documentation skill."""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "LICENSE",
    "agents/openai.yaml",
    "references/route-map.md",
    "references/progress-model.md",
    "references/document-levels.md",
    "references/document-templates.md",
    "references/quality-checklist.md",
    "tests/pressure-scenarios.md",
    "tests/baseline-red.md",
    "tests/green-results.md",
    "tests/github-validation-matrix.md",
]


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def main() -> int:
    for relative in REQUIRED_FILES:
        if not (ROOT / relative).is_file():
            fail(f"missing required file: {relative}")

    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    if not skill.startswith("---\n"):
        fail("SKILL.md is missing YAML frontmatter")
    frontmatter = skill.split("---\n", 2)[1]
    if not re.search(r"^name:\s*project-documentation\s*$", frontmatter, re.M):
        fail("frontmatter name is incorrect")
    description = re.search(r"^description:\s*(.+)$", frontmatter, re.M)
    if not description or not description.group(1).startswith("Use when"):
        fail("description must start with 'Use when'")
    all_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [ROOT / "SKILL.md", *sorted((ROOT / "references").glob("*.md"))]
    )
    if "[TODO" in all_text:
        fail("unfinished TODO placeholder found")

    for reference in re.findall(r"\]\((references/[^)]+)\)", skill):
        if not (ROOT / reference).is_file():
            fail(f"broken reference link: {reference}")

    required_concepts = [
        "Route decisions, ledgers, workflows, and progress tracking are recommendations",
        "current facts",
        "not-run",
        "blocked",
        "secrets",
    ]
    for concept in required_concepts:
        if concept.lower() not in skill.lower():
            fail(f"missing core concept: {concept}")

    metadata = (ROOT / "agents/openai.yaml").read_text(encoding="utf-8")
    if "$project-documentation" not in metadata:
        fail("openai.yaml default_prompt must mention $project-documentation")

    print(f"PASS: {len(REQUIRED_FILES)} files and core skill invariants verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
