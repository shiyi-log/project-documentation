# Codex 公共技能集合仓库设计

## 状态

- 设计状态：已获用户批准，等待规范复核
- 日期：2026-09-28
- 时区：`Asia/Shanghai`（UTC+08:00）
- 当前仓库：`shiyi-log/project-documentation`
- 目标仓库：`shiyi-log/codex-public-skills`

## 背景与问题

当前仓库以单一 `project-documentation` 技能为根目录，仓库名称、README、贡献指南和安装说明都把仓库解释为一个技能。本机 `~/.codex/skills` 已经维护了 15 个可公开的本地技能。继续把这些技能分别维护在本机、只上传其中一个，会造成来源不清、版本漂移、安装方式不一致和远端公共资产缺少统一索引。

本次改造将仓库提升为“公共技能集合”这一更准确的边界，同时保留现有 `project-documentation` 的 Git 历史和已经验证的内容。

## 目标

1. 在一个公开仓库中维护本机 15 个公共技能的可审查源码和必要元数据。
2. 让每个技能保持独立目录、独立 `SKILL.md` 和独立资源，不改变技能之间的触发边界。
3. 提供明确的目录清单、安装说明和可复用的本地同步入口。
4. 将 GitHub 仓库改名为 `shiyi-log/codex-public-skills`，保持原有提交历史。
5. 保留当前仓库版本较新的 `project-documentation` 内容，避免用较旧的本机安装副本回退已验证文档。
6. 通过可重复的静态验证、技能校验和远端 SHA 校验交付。

## 非目标

- 不把 15 个技能合并成一个新的巨大 `SKILL.md`。
- 不上传 `/Users/a399/.codex/skills/.system` 下的系统技能。
- 不上传本机 Git 元数据、生成缓存、`.artifacts`、`__pycache__`、凭据、令牌、Cookie、私钥、密码或运行时账号数据。
- 不在本次改造中自动覆盖正在使用的本机技能目录。
- 不把本地静态验证、GitHub 推送或仓库改名描述成生产运行时验收。

## 公共技能清单

本次集合初始清单固定为以下 15 个目录：

1. `adapt-claude-desktop-zh-macos`
2. `config`
3. `desktop-data-port-allocation`
4. `github-ci-runner`
5. `hatch-pet`
6. `jiema-project`
7. `mtproxyl-maintainer`
8. `naming-chinese-brands`
9. `project-documentation`
10. `project-ledger`
11. `shop`
12. `shop-bot-network-stats`
13. `shuangxiang-project`
14. `tron-project`
15. `tronh-project`

清单是同步脚本和目录验证的边界；后续增加或移除技能必须同时修改清单、目录和变更记录。

## 目录与职责

迁移后的仓库使用以下顶层结构：

```text
codex-public-skills/
├── skills/
│   ├── adapt-claude-desktop-zh-macos/
│   ├── config/
│   ├── desktop-data-port-allocation/
│   ├── github-ci-runner/
│   ├── hatch-pet/
│   ├── jiema-project/
│   ├── mtproxyl-maintainer/
│   ├── naming-chinese-brands/
│   ├── project-documentation/
│   ├── project-ledger/
│   ├── shop/
│   ├── shop-bot-network-stats/
│   ├── shuangxiang-project/
│   ├── tron-project/
│   └── tronh-project/
├── catalog/
│   └── skills.json
├── tools/
│   └── sync_local_skills.py
├── docs/
│   ├── project-ledger.md
│   └── superpowers/
├── README.md
├── CONTRIBUTING.md
├── CHANGELOG.md
└── LICENSE
```

- `skills/` 是技能源码的唯一集合目录；技能内部资源原样保留，除路径迁移外不做无关重写。
- `catalog/skills.json` 是集合索引，不重复复制完整技能正文；至少包含目录名、显示名、来源根、版本（存在时）、描述和同步时间。
- `tools/sync_local_skills.py` 负责从 `/Users/a399/.codex/skills` 读取清单并同步到 `skills/`。默认只报告差异；显式写入时才复制，且拒绝清单外目录和排除路径。
- `docs/project-ledger.md` 记录读写、验证、远端操作、复用和回滚证据。
- 根 README 只描述集合级安装和维护；技能的专门规则继续由各自的 `SKILL.md` 权威维护。

## `project-documentation` 的权威来源

当前工作树中的 `project-documentation` 已包含后续的中文规则、固定 SHA 的项目清单和百项目一致性验证结果，HEAD 为 `2d6f911d32058e56606ff78e9712bab4cacea4d6`。本次迁移将这些当前仓库内容放入 `skills/project-documentation/`，不使用本机安装副本覆盖它们。

其余 14 个技能从本机 `/Users/a399/.codex/skills/<name>/` 导入。导入前执行文件清单和敏感模式扫描；发现不适合公开的文件时停止该文件的导入并在台账中记录，而不是静默上传。

## 同步与安装边界

同步工具必须支持以下行为：

1. 读取固定技能清单并拒绝清单外目录。
2. 默认 dry-run，输出新增、修改、删除和排除的相对路径。
3. 显式写入时复制普通文件和符号链接目标内容，但不复制源目录中的 `.git`、缓存和生成产物。
4. 写入前检查技能目录存在 `SKILL.md`，并校验 frontmatter 的 `name` 与目录名一致或由明确兼容规则解释。
5. 不修改 `/Users/a399/.codex/skills`；本次只把本机技能上传到仓库。
6. 后续从仓库安装时，使用集合 README 描述的逐技能复制或链接方式，避免把仓库根目录误当作单一技能目录。

## 远端改名与 Git 交付

远端操作顺序如下：

1. 在本地完成迁移、文档、索引、同步工具和验证。
2. 检查 `git diff --check`、测试、技能校验、敏感模式扫描和最终 staged 文件名。
3. 提交集合迁移。
4. 使用已登录的 `shiyi-log` 账号将 GitHub 仓库从 `project-documentation` 改名为 `codex-public-skills`。
5. 更新本地 `origin` URL 到新仓库地址并推送 `main`。
6. fetch 后比较 `HEAD` 与 `origin/main`，读取远端元数据确认名称、公开性和默认分支。
7. 若远端改名或推送失败，保留本地提交和原远端地址，记录阻塞原因，不删除本机文件、不强推覆盖历史。

GitHub 改名是可逆的：如需回滚，可将远端名称改回旧名、将 `origin` 恢复为旧地址，并保留集合迁移提交；技能源码不会依赖仓库名。

## 验证与接受标准

### 静态结构

- 15 个清单目录全部存在，且每个目录恰好有一个入口 `SKILL.md`。
- 清单不包含 `.system` 技能或未声明目录。
- 集合目录中没有 `.git`、`.artifacts`、`__pycache__`、编译缓存或凭据类文件。
- `catalog/skills.json` 与 `skills/` 目录、每个入口 frontmatter 相互一致。

### 技能质量

- 对每个技能执行本地 `quick_validate.py`；校验失败的技能不得标记为已上传。
- 运行当前仓库已有的 `tests/validate_skill.py` 及其适用测试。
- 运行 `git diff --check`。

### Git 与远端

- 提交前确认 staged 文件只包含本次集合迁移、文档、索引、工具和台账变更。
- 推送后 `git rev-parse HEAD` 与 `git rev-parse origin/main` 完全一致。
- GitHub 元数据显示仓库名为 `codex-public-skills`、公开、未归档、默认分支为 `main`。

### 证据边界

上述检查只证明源码集合、文档、索引、同步工具和远端 Git 交付；不证明每个技能对应的外部服务、真实账号、生产系统、浏览器、链、数据库或第三方 provider 已运行。

## 失败、恢复与后续维护

- 导入失败：保留失败源目录不变，记录具体路径和错误，修复后重新执行 dry-run。
- 敏感扫描失败：不上传疑似敏感文件；必要时将技能标为未上传并等待明确处理。
- 校验失败：修复技能本身或调整集合元数据，不跳过验证直接推送。
- 推送失败：不重复创建提交；先检查 `HEAD`、远端分支和远端错误，再按实际状态重试。
- 远端改名失败：保持原仓库名和本地 `origin`，将集合迁移作为未完成交付记录。
- 回滚：使用迁移前 SHA 恢复本地集合提交，或恢复远端仓库名；不删除本机源技能。

后续统一维护以 `skills/` 和 `catalog/skills.json` 为仓库权威，以同步工具的 dry-run 差异作为变更入口；每次技能变更必须更新相应技能内部版本/变更记录（若该技能已有该约定）、集合 `CHANGELOG.md` 和项目台账。

## 本次实施顺序

1. 创建并自审本设计规范。
2. 编写实施计划。
3. 建立集合目录、同步工具、索引和集合级文档。
4. 导入 14 个本机技能，并迁移当前仓库版本的 `project-documentation`。
5. 执行结构、技能、敏感文件和仓库测试。
6. 提交本地迁移。
7. 执行 GitHub 仓库改名、更新远端、推送并做 SHA/元数据回读。
8. 追加台账关闭条目，明确已完成项和仍未运行的外部边界。
