#!/usr/bin/env python3
"""固定 GitHub 项目快照并执行文档多源一致性静态审计。

该工具只读上游仓库。它不声称完成浏览器、部署、生产或发布验收；
这些边界会以状态和原因保留在逐项目结果中。
"""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path
from typing import Any


STATUS = {"verified", "partial", "not-run", "blocked", "not-implemented"}
DEFAULT_BRANCHES = ("main", "master", "develop")
DOC_NAMES = re.compile(
    r"^(README(?:\.[^.]+)?|CHANGELOG(?:\.[^.]+)?|CONTRIBUTING(?:\.[^.]+)?|"
    r"DOCUMENTATION(?:\.[^.]+)?|LICENSE(?:\.[^.]+)?)$",
    re.I,
)
DOC_DIRS = {"docs", "doc", "documentation", "website", "book"}
IMPL_DIRS = {
    "src",
    "lib",
    "app",
    "apps",
    "cmd",
    "pkg",
    "server",
    "backend",
    "frontend",
    "packages",
    "internal",
}
CONFIG_NAMES = {
    "Makefile",
    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
    "pyproject.toml",
    "setup.cfg",
    "tox.ini",
    "package.json",
    "Cargo.toml",
    "go.mod",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "mkdocs.yml",
    "mkdocs.yaml",
    "docusaurus.config.js",
    "docusaurus.config.ts",
    "book.toml",
    "typedoc.json",
}
CONFIG_SUFFIXES = {".yml", ".yaml", ".toml", ".json", ".ini", ".cfg", ".xml"}
TEST_DIRS = {"test", "tests", "spec", "__tests__", "integration", "e2e"}
SOURCE_SUFFIXES = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".go",
    ".rs",
    ".java",
    ".kt",
    ".rb",
    ".php",
    ".c",
    ".cc",
    ".cpp",
    ".h",
    ".hpp",
}
COMMAND_RE = re.compile(
    r"`((?:python3?|uv|pip3?|poetry|pytest|npm|pnpm|yarn|cargo|go|make|"
    r"docker|docker-compose|kubectl|helm)\s+[^\n`]+)`"
)
PORT_RE = re.compile(r"(?:localhost|127\.0\.0\.1|0\.0\.0\.0):(\d{2,5})")
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)#\s]+)")


def run(cmd: list[str], cwd: Path | None = None, timeout: int = 120) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
        check=False,
    )


def read_text(path: Path, limit: int = 200_000) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")[:limit]
    except OSError:
        return ""


def rel_paths(root: Path) -> list[str]:
    paths: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if len(path.parts) - len(root.parts) > 5:
            continue
        paths.append(path.relative_to(root).as_posix())
    return sorted(paths)


def discover_sources(root: Path) -> dict[str, list[str]]:
    docs: list[str] = []
    implementation: list[str] = []
    configuration: list[str] = []
    tests_or_generated: list[str] = []
    for rel in rel_paths(root):
        path = root / rel
        parts = Path(rel).parts
        name = path.name
        suffix = path.suffix.lower()
        if name.lower().startswith("readme") or DOC_NAMES.match(name):
            docs.append(rel)
        if parts and parts[0].lower() in DOC_DIRS:
            docs.append(rel)
        if parts and parts[0].lower() in IMPL_DIRS:
            implementation.append(rel)
        elif suffix in SOURCE_SUFFIXES and len(parts) <= 3:
            implementation.append(rel)
        if name in CONFIG_NAMES or (
            parts and parts[0] in {".github", ".circleci", ".buildkite", "ci"}
        ):
            configuration.append(rel)
        elif suffix in CONFIG_SUFFIXES and len(parts) <= 3:
            configuration.append(rel)
        if parts and (parts[0].lower() in TEST_DIRS or "test" in name.lower()):
            tests_or_generated.append(rel)
        lower = rel.lower()
        if any(marker in lower for marker in ("openapi", "swagger", "schema", "typedoc", "sphinx", "mkdocs")):
            tests_or_generated.append(rel)
    return {
        "docs": sorted(set(docs))[:80],
        "implementation": sorted(set(implementation))[:120],
        "configuration": sorted(set(configuration))[:100],
        "tests_or_generated_authority": sorted(set(tests_or_generated))[:120],
    }


def check_links(root: Path, docs: list[str]) -> dict[str, Any]:
    checked = 0
    broken: list[str] = []
    for rel in docs:
        path = root / rel
        if path.suffix.lower() not in {".md", ".mdx", ".rst", ".txt"}:
            continue
        text = read_text(path)
        for target in LINK_RE.findall(text):
            if target.startswith(("http://", "https://", "mailto:", "#", "git@")):
                continue
            checked += 1
            candidate = (path.parent / target).resolve()
            if not candidate.is_file() and not candidate.is_dir():
                broken.append(f"{rel} -> {target}")
    return {"checked": checked, "broken": broken[:40]}


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(read_text(path))
        return value if isinstance(value, dict) else {}
    except json.JSONDecodeError:
        return {}


def check_commands(root: Path, docs: list[str], config: list[str]) -> dict[str, Any]:
    commands: list[str] = []
    unknown: list[str] = []
    package_scripts: set[str] = set()
    make_targets: set[str] = set()
    for rel in config:
        path = root / rel
        if path.name == "package.json":
            package_scripts.update(load_json(path).get("scripts", {}).keys())
        if path.name == "Makefile":
            make_targets.update(re.findall(r"^([A-Za-z0-9_.-]+):", read_text(path), re.M))
    for rel in docs:
        text = read_text(root / rel)
        for raw in COMMAND_RE.findall(text):
            command = raw.strip().splitlines()[0].strip()
            commands.append(command[:160])
            tokens = command.split()
            if tokens[:2] in (["npm", "run"], ["pnpm", "run"], ["yarn", "run"]) and len(tokens) >= 3:
                if tokens[2] not in package_scripts:
                    unknown.append(f"{rel}: {command}")
            elif tokens and tokens[0] == "make" and len(tokens) >= 2:
                target = tokens[1].split("|", 1)[0]
                if target not in make_targets:
                    unknown.append(f"{rel}: {command}")
            elif tokens and tokens[0] in {"pytest", "python", "python3", "uv", "pip", "pip3"}:
                if not any((root / d).is_dir() for d in TEST_DIRS):
                    unknown.append(f"{rel}: {command}")
    return {
        "checked": len(commands),
        "commands": commands[:60],
        "unknown": unknown[:40],
    }


def check_ports(root: Path, docs: list[str], config: list[str]) -> dict[str, Any]:
    documented: set[str] = set()
    configured: set[str] = set()
    for rel in docs:
        documented.update(PORT_RE.findall(read_text(root / rel)))
    for rel in config:
        configured.update(PORT_RE.findall(read_text(root / rel)))
    unmatched = sorted(documented - configured)
    return {
        "documented": sorted(documented),
        "configured": sorted(configured),
        "unmatched": unmatched,
    }


def validate_checkout(project: dict[str, Any], root: Path) -> dict[str, Any]:
    sources = discover_sources(root)
    links = check_links(root, sources["docs"])
    commands = check_commands(root, sources["docs"], sources["configuration"])
    ports = check_ports(root, sources["docs"], sources["configuration"])
    present = {key: bool(value) for key, value in sources.items()}
    source_count = sum(present.values())
    reasons: list[str] = []
    if source_count < 3:
        reasons.append("少于三类独立证据")
    if not present["docs"]:
        reasons.append("未发现文档入口")
    if not present["implementation"]:
        reasons.append("未发现实现目录或源码")
    if not present["configuration"]:
        reasons.append("未发现配置/自动化")
    if not present["tests_or_generated_authority"]:
        reasons.append("未发现测试或生成权威")
    if links["broken"]:
        reasons.append(f"发现 {len(links['broken'])} 个断链")
    if commands["unknown"]:
        reasons.append(f"发现 {len(commands['unknown'])} 个文档命令无法在配置/测试中定位")
    if ports["unmatched"]:
        reasons.append(f"发现文档端口未在配置中定位: {', '.join(ports['unmatched'])}")
    if source_count == 4 and not links["broken"] and not commands["unknown"] and not ports["unmatched"]:
        status = "verified"
    elif source_count >= 3:
        status = "partial"
    else:
        status = "blocked"
    return {
        "repo": project["repo"],
        "default_branch": project.get("default_branch"),
        "commit": project["commit"],
        "status": status,
        "sources": sources,
        "source_presence": present,
        "checks": {"links": links, "commands": commands, "ports": ports},
        "reasons": reasons,
        "limits": [
            "这是固定提交上的静态多源审计，不等同于浏览器、部署、生产或发布验收。",
            "仅当文档声明能够被实现、配置/自动化和测试/生成权威定位时才标记 verified。",
        ],
    }


def resolve_head(repo: str) -> dict[str, str] | None:
    url = f"https://github.com/{repo}.git"
    result = run(["git", "ls-remote", "--symref", url, "HEAD"], timeout=60)
    if result.returncode != 0:
        return None
    commit = ""
    branch = ""
    for line in result.stdout.splitlines():
        if line.startswith("ref: ") and "\tHEAD" in line:
            branch = line.split("refs/heads/", 1)[-1].split("\t", 1)[0]
        elif "\tHEAD" in line:
            commit = line.split("\t", 1)[0]
    if not commit:
        return None
    return {"repo": repo, "default_branch": branch or "unknown", "commit": commit}


def prepare_manifest(seed: Path, output: Path, workers: int) -> int:
    repos = [
        line.strip()
        for line in seed.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        resolved = list(pool.map(resolve_head, repos))
    projects: list[dict[str, Any]] = []
    for item in resolved:
        if not item:
            continue
        projects.append(
            {
                **item,
                "status": "not-run",
                "sources": {
                    "docs": [],
                    "implementation": [],
                    "configuration": [],
                    "tests_or_generated_authority": [],
                },
            }
        )
    payload = {
        "generated_at": dt.date.today().isoformat(),
        "source": seed.name,
        "projects": projects,
    }
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"已解析 {len(projects)}/{len(repos)} 个仓库")
    if len(projects) < 100:
        return 2
    return 0


def clone_at(project: dict[str, Any], root: Path) -> tuple[bool, str]:
    # codeload 按提交 SHA 提供只读快照，通常比 Git smart-http 更稳定，
    # 也避免为 100+ 个仓库建立持久 Git 工作树。
    archive = root.parent / f"{root.name}.tar.gz"
    extract_dir = root.parent / f"{root.name}.extract"
    url = f"https://codeload.github.com/{project['repo']}/tar.gz/{project['commit']}"
    result = run(
        [
            "curl",
            "-L",
            "--fail",
            "--silent",
            "--show-error",
            "--max-time",
            "240",
            url,
            "-o",
            str(archive),
        ],
        timeout=300,
    )
    if result.returncode != 0:
        return False, (result.stderr or result.stdout)[-1000:]
    try:
        extract_dir.mkdir(parents=True, exist_ok=False)
        with tarfile.open(archive, mode="r:gz") as handle:
            members = []
            skipped_long_paths = 0
            for member in handle.getmembers():
                if len(member.name) > 180 or any(len(part) > 180 for part in Path(member.name).parts):
                    skipped_long_paths += 1
                    continue
                members.append(member)
            base = extract_dir.resolve()
            for member in members:
                target = (extract_dir / member.name).resolve()
                if target != base and base not in target.parents:
                    return False, f"归档路径越界: {member.name}"
            handle.extractall(extract_dir, members=members)
        roots = [path for path in extract_dir.iterdir() if path.is_dir()]
        if len(roots) != 1:
            return False, "归档顶层目录不唯一"
        root.mkdir(parents=True, exist_ok=False)
        for child in roots[0].iterdir():
            shutil.move(str(child), str(root / child.name))
        return True, ""
    except (OSError, tarfile.TarError) as exc:
        return False, f"归档解包失败: {exc}"
    finally:
        archive.unlink(missing_ok=True)
        shutil.rmtree(extract_dir, ignore_errors=True)


def validate_project(project: dict[str, Any], workdir: Path) -> dict[str, Any]:
    safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", project["repo"])
    checkout = workdir / safe_name
    if checkout.exists():
        shutil.rmtree(checkout)
    try:
        ok, error = clone_at(project, checkout)
        if not ok:
            return {
                "repo": project["repo"],
                "default_branch": project.get("default_branch"),
                "commit": project["commit"],
                "status": "blocked",
                "sources": {
                    "docs": [],
                    "implementation": [],
                    "configuration": [],
                    "tests_or_generated_authority": [],
                },
                "source_presence": {},
                "checks": {},
                "reasons": [f"固定快照抓取失败: {error}"],
                "limits": ["未取得本地快照，未执行静态一致性检查。"],
            }
        return validate_checkout(project, checkout)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {
            "repo": project["repo"],
            "default_branch": project.get("default_branch"),
            "commit": project["commit"],
            "status": "blocked",
            "sources": {
                "docs": [],
                "implementation": [],
                "configuration": [],
                "tests_or_generated_authority": [],
            },
            "source_presence": {},
            "checks": {},
            "reasons": [f"审计异常: {exc}"],
            "limits": ["异常发生后没有用猜测替代证据。"],
        }


def write_report(results: list[dict[str, Any]], output: Path, manifest: Path) -> None:
    counts: dict[str, int] = {status: 0 for status in STATUS}
    for result in results:
        counts[result["status"]] = counts.get(result["status"], 0) + 1
    lines = [
        "# 百项目文档实现一致性验证报告",
        "",
        f"- 生成日期：{dt.date.today().isoformat()}",
        f"- 清单：`{manifest}`",
        f"- 项目数：{len(results)}",
        f"- 状态统计：{json.dumps(counts, ensure_ascii=False, sort_keys=True)}",
        "",
        "## 方法",
        "",
        "每个项目固定到清单中的提交 SHA，并交叉检查文档入口、实现源码、配置/自动化、测试或生成权威四类来源。"
        "该报告只覆盖静态多源证据，不把本地构建、HTTP 200、单元测试或文档构建成功表述为部署、发布或生产验收。",
        "",
        "## 项目结果",
        "",
        "| 项目 | 提交 | 状态 | 证据类别 | 主要原因 |",
        "|---|---|---|---|---|",
    ]
    for result in results:
        sources = result.get("source_presence", {})
        source_text = "、".join(key for key, present in sources.items() if present) or "无"
        reason = "；".join(result.get("reasons", [])) or "四类来源均可定位，未发现静态冲突"
        lines.append(
            f"| `{result['repo']}` | `{result['commit'][:12]}` | `{result['status']}` | "
            f"{source_text} | {reason[:220]} |"
        )
    lines.extend(
        [
            "",
            "## 复核限制",
            "",
            "- `verified` 只表示固定 SHA 上的静态多源证据可互相定位，不表示生产可用。",
            "- `partial`、`blocked` 和 `not-run` 必须保留具体原因；禁止把缺失证据补写成通过。",
            "- 需要浏览器、真实数据库、外部 Provider、链上、Telegram、CI 或生产验证时，应另建对应证据记录。",
            "",
        ]
    )
    output.write_text("\n".join(lines), encoding="utf-8")


def validate_manifest(
    manifest_path: Path,
    output_dir: Path,
    workers: int,
    min_projects: int,
) -> int:
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    projects = payload.get("projects", [])
    if len(projects) < min_projects:
        print(f"项目数不足 {min_projects}: {len(projects)}", file=sys.stderr)
        return 2
    output_dir.mkdir(parents=True, exist_ok=True)
    temp_root = Path(tempfile.mkdtemp(prefix="project-doc-corpus-"))
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
            futures = [pool.submit(validate_project, project, temp_root) for project in projects]
            results = [future.result() for future in futures]
        (output_dir / "project-results.json").write_text(
            json.dumps(results, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        report = output_dir / "百项目文档实现一致性验证报告.md"
        write_report(results, report, manifest_path)
        print(f"已完成 {len(results)} 个项目的固定 SHA 静态多源审计")
        print(f"报告: {report}")
        return 0
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    prepare = sub.add_parser("prepare", help="从种子清单解析默认分支和 HEAD SHA")
    prepare.add_argument("--seed", type=Path, required=True)
    prepare.add_argument("--output", type=Path, required=True)
    prepare.add_argument("--workers", type=int, default=min(16, (os.cpu_count() or 4) * 2))
    validate = sub.add_parser("validate", help="抓取固定快照并执行多源一致性审计")
    validate.add_argument("--manifest", type=Path, required=True)
    validate.add_argument("--output-dir", type=Path, required=True)
    validate.add_argument("--workers", type=int, default=min(8, os.cpu_count() or 4))
    validate.add_argument(
        "--min-projects",
        type=int,
        default=100,
        help="本次清单至少需要的项目数；批次验证可设置为 1",
    )
    args = parser.parse_args()
    if args.command == "prepare":
        return prepare_manifest(args.seed, args.output, args.workers)
    return validate_manifest(args.manifest, args.output_dir, args.workers, args.min_projects)


if __name__ == "__main__":
    raise SystemExit(main())
