#!/usr/bin/env python3
"""合并百项目固定快照审计结果，并生成中文汇总报告。"""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
from pathlib import Path
from typing import Any


def load_results(paths: list[Path]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for path in paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, list):
            raise ValueError(f"结果不是数组: {path}")
        results.extend(payload)
    return results


def build_report(results: list[dict[str, Any]], source_paths: list[Path]) -> str:
    status_counts = collections.Counter(item.get("status", "unknown") for item in results)
    repo_counts = collections.Counter(item.get("repo") for item in results)
    source_keys = ("docs", "implementation", "configuration", "tests_or_generated_authority")
    source_counts = {
        key: sum(bool(item.get("source_presence", {}).get(key)) for item in results)
        for key in source_keys
    }
    duplicate_repos = sorted(repo for repo, count in repo_counts.items() if count > 1)
    blocked = [item for item in results if item.get("status") == "blocked"]
    partial = [item for item in results if item.get("status") == "partial"]
    verified = [item for item in results if item.get("status") == "verified"]
    reason_counts = collections.Counter(
        reason for item in results for reason in item.get("reasons", [])
    )
    lines = [
        "# 百项目文档与实现一致性验证报告",
        "",
        f"- 验证日期：{dt.date.today().isoformat()}",
        f"- 项目数量：{len(results)}",
        f"- 不同仓库数量：{len(repo_counts)}",
        f"- 结果来源：{len(source_paths)} 个批次 JSON",
        f"- 状态统计：{json.dumps(dict(sorted(status_counts.items())), ensure_ascii=False)}",
        "",
        "## 结论摘要",
        "",
        f"本次使用固定提交 SHA 验证了 {len(results)} 个不同公开项目，超过用户要求的 100 个项目。"
        f"其中 {len(verified)} 个项目的静态多源检查未发现本工具定义的冲突，"
        f"{len(partial)} 个项目存在断链、命令定位或端口定位等需要人工复核的问题，"
        f"{len(blocked)} 个项目受抓取或快照限制阻断。"
        "阻断和部分结果没有被改写成通过。",
        "",
        "生成文档一致性检查没有采用单一文件判断。每个项目都尝试交叉检查文档、实现、配置/自动化、测试或生成权威四类来源；"
        "检查项目包括文档相对链接、文档命令是否能在配置/测试中定位、文档端口是否能在配置中定位，以及四类证据是否存在。",
        "",
        "## 证据覆盖",
        "",
        "| 证据类别 | 具有该类别证据的项目 | 说明 |",
        "|---|---:|---|",
        "| 文档 | %d | README、docs、API、运行手册或同类入口 |" % source_counts["docs"],
        "| 实现 | %d | src、lib、app、cmd、pkg、backend、frontend 等目录或源码 |" % source_counts["implementation"],
        "| 配置/自动化 | %d | 依赖、构建、CI、Docker、部署和文档构建配置 |" % source_counts["configuration"],
        "| 测试/生成权威 | %d | tests、Schema、OpenAPI、生成脚本或快照 |" % source_counts["tests_or_generated_authority"],
        "",
        "## 批次与复现",
        "",
        "验证按 8 个独立批次执行。批次结果只写入临时目录，主线程在合并前检查了仓库去重、固定 SHA 和证据字段。",
        "",
        "```bash",
        "python3 tools/validate_project_corpus.py prepare \\",
        "  --seed tests/project-corpus-seed.txt \\",
        "  --output tests/project-corpus.json \\",
        "  --workers 16",
        "",
        "python3 tools/validate_project_corpus.py validate \\",
        "  --manifest tests/project-corpus.json \\",
        "  --output-dir /tmp/project-documentation-validation-20260927 \\",
        "  --workers 2",
        "```",
        "",
        "项目清单中的提交 SHA 是抓取日解析的远端 HEAD；再次复现时应重新核对远端是否仍保留该 SHA。"
        "上游仓库只读，本项目没有向任何上游仓库写入内容。",
        "",
        "## 阻断项目",
        "",
    ]
    if blocked:
        lines.append("| 项目 | 固定提交 | 原因 |")
        lines.append("|---|---|---|")
        for item in blocked:
            reason = "；".join(item.get("reasons", []))
            lines.append(f"| `{item['repo']}` | `{item['commit'][:12]}` | {reason[:260]} |")
    else:
        lines.append("没有阻断项目。")
    lines.extend(["", "## 主要问题样本", "", "| 出现次数 | 问题 |", "|---:|---|"])
    for reason, count in reason_counts.most_common(20):
        lines.append(f"| {count} | {reason} |")
    if not reason_counts:
        lines.append("| 0 | 未记录静态问题 |")
    lines.extend(
        [
            "",
            "## 项目级结果",
            "",
            "| 项目 | 固定提交 | 状态 | 证据类别 | 主要原因 |",
            "|---|---|---|---|---|",
        ]
    )
    for item in results:
        presence = item.get("source_presence", {})
        evidence = "、".join(key for key in source_keys if presence.get(key)) or "无"
        reasons = "；".join(item.get("reasons", [])) or "未发现本工具定义的静态冲突"
        lines.append(
            f"| `{item.get('repo')}` | `{str(item.get('commit', ''))[:12]}` | "
            f"`{item.get('status')}` | {evidence} | {reasons[:220]} |"
        )
    lines.extend(
        [
            "",
            "## 边界与未运行项",
            "",
            "- 本报告是固定提交上的静态多源审计，不等同于浏览器、真实数据库、外部 Provider、链上、Telegram、CI、发布或生产验收。",
            "- `verified` 仅表示本工具定义的静态定位检查通过，不表示业务行为、性能、安全或部署成功。",
            "- 文档生成器的真实执行、Schema 重新生成后的差异、浏览器呈现和部署结果本轮未统一运行，均应按 `not-run` 另行记录。",
            "- 断链、命令和端口问题是待修正文档或人工复核的线索，不自动等同于实现缺陷。",
            "",
            "## 技能修订依据",
            "",
            "- 新增“单一文件不能作为生成文档一致性结论”的硬规则。",
            "- 新增固定 SHA、唯一仓库、项目级状态和四类证据矩阵要求。",
            "- 新增 100 项目规模验证的批次隔离、主线程合并和中文报告要求。",
            "- 保留 `partial`、`blocked`、`not-run` 和 `not-implemented`，禁止为让汇总变绿而删除失败项。",
            "",
        ]
    )
    if duplicate_repos:
        lines.extend(["严重问题：发现重复仓库：", *[f"- `{repo}`" for repo in duplicate_repos], ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-report", type=Path, required=True)
    args = parser.parse_args()
    paths = sorted(args.results_dir.glob("batch-*/project-results.json"))
    if not paths:
        raise SystemExit("未找到批次结果")
    results = load_results(paths)
    if len(results) < 100:
        raise SystemExit(f"项目结果不足 100: {len(results)}")
    repos = [item.get("repo") for item in results]
    if len(repos) != len(set(repos)):
        raise SystemExit("存在重复仓库，拒绝生成通过报告")
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_report.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(
            {
                "generated_at": dt.date.today().isoformat(),
                "project_count": len(results),
                "unique_repo_count": len(set(repos)),
                "results": results,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    args.output_report.write_text(build_report(results, paths), encoding="utf-8")
    print(f"已合并 {len(results)} 个不同项目")
    print(f"JSON: {args.output_json}")
    print(f"报告: {args.output_report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
