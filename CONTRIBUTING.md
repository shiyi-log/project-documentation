# 贡献指南

感谢你改进 `project-documentation`。

## 范围

变更应聚焦于可复用的项目文档指导。不要把可选路由、台账、工作流或进度跟踪变成强制仪式。

## 创建拉取请求前

Run:

```bash
python3 tests/validate_skill.py
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
git diff --check
```

行为规则变更必须新增或更新压力场景，并记录观察到的基线、改进后的行为和剩余漏洞。生成文档或大规模验证变更还必须运行 `tools/validate_project_corpus.py`，并在中文报告中保存固定 SHA 和多源证据矩阵。

## 内容要求

- 当前事实必须与计划和假设分开。
- 对小项目和大项目使用相称的指导。
- 避免秘密和私人数据。
- 保留明确的 `not-run`、`blocked` 和 `partial` 边界。
- 生成文档不得只依据单一文件，至少交叉检查实现、配置/自动化和测试/生成权威中的三类来源。
- 至少 100 项目验证必须使用唯一项目和固定提交 SHA。
- 优先进行范围狭窄的修正，不做无边界的大重写。
