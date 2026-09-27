# project-documentation

`project-documentation` 是一个用于创建、更新、审查和审计项目文档的 Codex 技能。

它按项目实际复杂度自适应：

- 一行 README 修正保持小范围；
- 库的变更可以路由到 API、兼容性、迁移和发布文档；
- 多服务或基础设施变更可以展开架构、数据、部署、恢复、外部权威和验证边界；
- 个人维护者的项目如果规模大或风险高，同样可以使用更高文档层级。

路由、台账、工作流和进度跟踪都是可选建议，不是强制仪式。不可妥协的边界是状态真实、范围受控、秘密受保护、证据诚实。

## 安装

将本目录复制或链接到 Codex 技能目录：

```text
~/.codex/skills/project-documentation
```

对于本仓库，安装路径就是本 README 所在目录。放入用户配置的技能目录后，新 Codex 会话即可发现该技能。

## 参考文档

- `references/route-map.md`
- `references/progress-model.md`
- `references/document-levels.md`
- `references/document-templates.md`
- `references/quality-checklist.md`
- `references/一致性审计.md`

## 验证

压力场景和加载技能前的 RED 基线在 `tests/`。项目清单是只读上游输入，覆盖 CLI、库、多服务应用、平台和基础设施；百项目验证还会记录固定 SHA 和逐项目多源证据。
