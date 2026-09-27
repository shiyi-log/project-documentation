# RED 基线——加载 `project-documentation` 前

日期：2026-09-27
方法：两个独立基线代理在不加载技能的情况下执行压力场景。

## 观察到的失败

- 小型 CLI 工作会停留在功能附近，但可能遗漏生成的 man page、Shell 补全、本地化或仓库自己的文档生成路径。
- 大型基础设施工作能识别影响面，但可能引入用户未要求的治理流程、台账、路由矩阵或多团队审批工作流。
- “把所有文档写全”被识别为含义不明，但典型回答可能过于浅显，也可能扩展成没有正当边界的大规模重写。
- 库的 API 变更可能只更新 README/changelog，遗漏 API 参考、兼容性、弃用、迁移或发布约定文档。
- 多服务 Schema 变更可能只验证全新数据库，遗漏已有安装升级、迁移顺序、服务契约、回滚限制、可观测性和数据丢失风险。
- 一行 README 修正可能被扩大成完整文档审计或沉重的应用/发布测试。
- 生成文档场景可能只读生成文件或 README，没有同时读取实现、配置/自动化和测试/生成权威。
- 大规模验证可能报告“看过很多项目”，但没有固定 SHA、项目去重和逐项目证据。

## 原始合理化或基线措辞

> “Documentation should stay close to the feature, and the repository’s existing conventions are the source of truth.”

> “The blast radius is large, so documentation must reflect the actual supported workflow and be validated against build automation.”

> “The request is materially ambiguous; documenting everything could mean anything from a README refresh to a full architecture and operations knowledge base.”

> “Do not create a durable ledger unless the user asks for one or the repository already requires it.”

## 从 RED 提炼的技能要求

1. 检查仓库特定的权威来源和生成文档表面。
2. 按实际结构和风险路由，不按所有者身份路由。
3. 保持 route、ledger、workflow 和 progress 机制可选。
4. 区分本地/静态、集成、部署、外部、发布和生产证据。
5. 当 API、迁移、兼容性、运维或发布行为变化时，把文档纳入交付边界。
6. 生成文档必须交叉检查至少三类独立来源，不能凭单一文件下结论。
7. 100 项目规模必须使用固定、去重清单和逐项目状态。
