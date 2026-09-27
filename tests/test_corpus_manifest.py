#!/usr/bin/env python3
"""百项目清单结构测试。"""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "tests" / "project-corpus.json"
ALLOWED_STATUS = {
    "verified",
    "partial",
    "not-run",
    "blocked",
    "not-implemented",
}
REQUIRED_SOURCES = {
    "docs",
    "implementation",
    "configuration",
    "tests_or_generated_authority",
}


def fail(message: str) -> "NoReturn":
    raise SystemExit(f"FAIL: {message}")


def main() -> int:
    if not MANIFEST.is_file():
        fail(f"缺少清单: {MANIFEST}")
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    projects = payload.get("projects")
    if not isinstance(projects, list):
        fail("projects 必须是数组")
    if len(projects) < 100:
        fail(f"项目数不足 100: {len(projects)}")

    repos: set[str] = set()
    for index, project in enumerate(projects, start=1):
        if not isinstance(project, dict):
            fail(f"第 {index} 项不是对象")
        repo = project.get("repo")
        commit = project.get("commit")
        if not isinstance(repo, str) or "/" not in repo:
            fail(f"第 {index} 项 repo 无效: {repo!r}")
        if repo in repos:
            fail(f"仓库重复: {repo}")
        repos.add(repo)
        if not isinstance(commit, str) or len(commit) < 7:
            fail(f"{repo} 缺少固定 commit SHA")
        sources = project.get("sources")
        if not isinstance(sources, dict):
            fail(f"{repo} 缺少 sources")
        missing = REQUIRED_SOURCES - set(sources)
        if missing:
            fail(f"{repo} 缺少证据类别: {sorted(missing)}")
        status = project.get("status")
        if status not in ALLOWED_STATUS:
            fail(f"{repo} 状态无效: {status!r}")

    print(f"PASS: {len(projects)} 个不同项目的清单结构有效")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
