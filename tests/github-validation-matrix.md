# GitHub 验证矩阵

第一批验证语料覆盖不同结构和风险。上游仓库只读，本项目不会写入这些仓库。

只读盘点日期：2026-09-27（Asia/Shanghai，UTC+08:00）。默认分支和代表性路径通过 GitHub API 读取。

| 仓库 | 默认分支 | 项目画像 | 代表性表面 | 路由场景 |
|---|---|---|---|---|
| `sharkdp/fd` | `master` | 基础 CLI | `README.md`、`CONTRIBUTING.md`、`CHANGELOG.md`、`Cargo.toml`、`tests/` | `update.basic.readme.low.static` |
| `psf/requests` | `main` | 成熟库 | `README.md`、`.github/CONTRIBUTING.md`、`HISTORY.md`、`docs/api.rst`、发布流程、`tests/` | `update.library.api.medium.test` |
| `encode/httpx` | `master` | 有独立文档的库 | `README.md`、贡献指南、`CHANGELOG.md`、`docs/api.md`、兼容性文档、`mkdocs.yml`、`tests/` | `update.library.api.medium.test` |
| `immich-app/immich` | `main` | 多服务自托管应用 | 贡献指南、架构、数据库迁移、安装、测试、备份恢复和文档构建工作流 | `update.service.data.high.runtime` |
| `apache/airflow` | `main` | 大型工作流平台 | 贡献指南、ADR、核心文档、管理/部署文档、发布管理和 Provider 表面 | `update.platform.architecture.high.external` |
| `kubernetes/kubernetes` | `master` | 有外部权威的基础设施项目 | README、贡献指南、构建文档、OpenAPI 说明、集群文档、发布/构建脚本 | `review.infra.ops.high.external` |

## 通过条件

- 小型工作不能被强制套用企业文档流程。
- 复杂工作不能被压缩成只改 README。
- route、ledger、workflow、progress 只在有用时建议。
- 必须识别外部权威和生成文档。
- 必须保留证据分级边界。
- 不能修改任何上游仓库。

## 盘点结果

- 六个仓库都有项目特定的入口文档和贡献/开发信号。
- 成熟库和大型项目都暴露了独立的 API、架构、测试、发布、运维、迁移或构建表面，而不是只有一个通用 README。
- 小型 CLI 的文档表面较紧凑，证明技能必须支持有界路径而不引入企业仪式。
- API 树的结构盘点只是结构证据，不能证明每个命令、测试、发布或生产工作流都通过。
