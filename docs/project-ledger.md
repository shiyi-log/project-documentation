# 项目台账

## 2026-09-28T18:25:20+08:00 — 建立公共技能集合仓库改造基线

- 状态 / Status: 进行中
- 目标 / Goal: 将当前单一 `project-documentation` 技能仓库改造成可统一维护的 Codex 公共技能集合，并在验证后改名为 `codex-public-skills`、上传本机公共技能。
- 读取 / Read:
  - `README.md`、`SKILL.md`、`CONTRIBUTING.md`、`CHANGELOG.md` — 当前仓库是单一 `project-documentation` 技能，包含文档指导、验证脚本和中文验证报告。
  - `git status --short --branch`、`git rev-parse HEAD`、`git log -5 --oneline` — 基线分支为 `main`，工作树干净，当前 HEAD 为 `2d6f911d32058e56606ff78e9712bab4cacea4d6`。
  - `git remote -v`、GitHub 仓库元数据 — 当前远端为公开仓库 `shiyi-log/project-documentation`，默认分支为 `main`。
  - `/Users/a399/.codex/skills/*` — 本机可公开技能目录共 15 个，未纳入 `.system` 技能。
  - `gh repo view shiyi-log/codex-public-skills` — 候选新仓库名当前未占用。
- 修改 / Write: `docs/project-ledger.md` — 创建本次改造的追加式证据台账；可逆：是。
- 时间逻辑 / Time logic: 使用系统时间和 `Asia/Shanghai`（UTC+08:00）记录人类排序；远端校验使用 Git 提交 SHA，不使用相对日期作为状态。
- 验证 / Verification:
  - `git status --short --branch` → 工作树干净；静态本地证据。
  - `gh auth status --hostname github.com` → `shiyi-log` 账号已登录，GitHub 写入能力尚未在本条目中执行；认证信息不记录。
  - 本机技能目录枚举 → 15 个候选公共技能；尚未完成敏感文件扫描和导入。
- 利用 / Reuse: 后续每次同步、校验、提交、推送、远端改名和回滚均追加本台账；回滚路径为恢复迁移前提交或按 Git SHA 恢复集合目录，不删除本机原始技能。
- 限制 / Limits: 本条目只记录基线和设计阶段；尚未修改技能目录、尚未执行 GitHub 仓库改名、尚未推送。
- 下一步 / Next: 写入并自审集合仓库设计规范，随后请求用户复核规范。

## 2026-09-28T18:26:08+08:00 — 提交集合仓库设计规范

- 状态 / Status: 进行中
- 目标 / Goal: 固化已批准的集合仓库设计，供实施前复核。
- 读取 / Read: `docs/superpowers/specs/2026-09-28-codex-public-skills-design.md`、`docs/project-ledger.md` — 自审无未解决占位项，目录职责、同步边界、验证和回滚路径一致；`git diff --check` 通过。
- 修改 / Write: `docs/superpowers/specs/2026-09-28-codex-public-skills-design.md`、`docs/project-ledger.md` — 提交设计规范和基线台账；规范提交 SHA 为 `1bdab27`；可逆：是。
- 时间逻辑 / Time logic: 使用 `Asia/Shanghai`（UTC+08:00）记录设计提交时间；远端改名尚未执行。
- 验证 / Verification: `git diff --cached --check` → 退出码 0；`git commit -m "docs: define public skills collection architecture"` → 退出码 0；静态/本地证据。
- 利用 / Reuse: 后续实施计划和代码变更必须以该规范为边界；可通过恢复迁移前 SHA 或回滚本次设计提交恢复。
- 限制 / Limits: 用户尚未复核书面规范；技能导入、敏感扫描、测试、GitHub 改名和推送均未运行。
- 下一步 / Next: 等待用户复核设计文件，收到确认后编写实施计划。

## 2026-09-29T13:30:47+08:00 — 重装前提交推送预检

- 状态 / Status: 进行中
- 目标 / Goal: 在重装系统前提交并推送当前仓库已完成的本地工作，核验远端一致性，辨明未随仓库备份的本机资产。
- 读取 / Read: `git status --short --branch`、`git remote show origin`、`git ls-remote --heads origin main`、`git log origin/main..HEAD` — `/Users/a399/Documents/ChatGPT/文档技能` 的 `main` 工作树干净，领先远端两个设计与台账提交，远端 `shiyi-log/project-documentation` 的 `main` 仍为 `2d6f911d32058e56606ff78e9712bab4cacea4d6`；`docs/superpowers/specs/2026-09-28-codex-public-skills-design.md`、`README.md`、`SKILL.md`、`CONTRIBUTING.md`、`tests/validate_skill.py`、`tests/test_corpus_manifest.py` — 目前仍为单技能仓库，集合迁移只是待复核设计；`~/.codex/skills` 目录清单 — 本机另有 15 个技能目录，未纳入本仓库；`gh auth status` — `shiyi-log` 活跃认证，另有一个失效的非活跃账号，均不记录凭据内容。
- 修改 / Write: `docs/project-ledger.md` — 追加本次预检与授权边界；可逆：是。此前两个设计提交原样保留。
- 时间逻辑 / Time logic: 使用系统时钟和 `Asia/Shanghai`（UTC+08:00）记录预检时间；用 Git SHA 比较同步状态，不依赖相对时间。
- 验证 / Verification: `git diff --check origin/main..HEAD` → 退出码 0；远端 `main` 已只读核对；专用技能测试、推送后 SHA 比对尚未运行。
- 利用 / Reuse: 本条及后续关闭条目可供重装后核对仓库历史。恢复以远端 URL 和提交 SHA 为准，不对本机原始技能或凭据做删除/覆盖。
- 限制 / Limits: 用户授权当前仓库的提交推送；未授权公开上传本机其他技能、机器级凭据或执行设计中的仓库改名与集合迁移。这次推送不构成全机备份。
- 下一步 / Next: 运行仓库校验并审查 staged 范围，提交台账后推送 `main`，回读远端 SHA。

## 2026-09-29T13:37:50+08:00 — 重装前仓库推送与备份边界

- 状态 / Status: 进行中（本条随提交推送后，仍需回读远端确认）。
- 目标 / Goal: 保存本仓库截至本次操作的提交，并明确系统重装前不能忽略的未备份内容。
- 读取 / Read: `/Users/a399/Documents/ChatGPT/文档技能` 的 `main`、`git ls-remote --heads origin main`、GitHub 仓库元数据 — 原有两个设计提交已从 `2d6f911` 推送到 `6c76be7`，远端名称仍为 `shiyi-log/project-documentation`、公开且默认分支为 `main`；`/Users/a399/Desktop/data` 和 `/Users/a399/Documents/ChatGPT` 下 19 个 Git 工作树的分支、上游和工作区变更数量（未读取私人文件内容）— `shop` 领先上游 8 个提交，`tron` 领先 3 个且有 4 项工作区变更，另有若干仓库含工作区变更或无上游；`tmutil destinationinfo`、`tmutil latestbackup` — 未配置 Time Machine 目标，最新备份不可用；`~/.codex/skills`、Codex 配置/认证、SSH、Git 与 shell 配置路径存在（未记录内容），技能目录约 88 MB；[OpenAI 官方技能说明](https://developers.openai.com/codex/skills/) — 技能以含 `SKILL.md` 的目录为单位。
- 修改 / Write: `docs/project-ledger.md` — 追加本次验证、备份边界及恢复信息；可逆：是。`git push origin main` 已将先前的 `1bdab27` 和 `6c76be7` 推至远端；未修改其他仓库、账号、系统备份或本机技能。
- 时间逻辑 / Time logic: 系统时钟，`Asia/Shanghai`（UTC+08:00）；用提交 SHA 确认同步，不能凭推送时间推断备份完整性。
- 验证 / Verification: `python3 tests/validate_skill.py` → 退出码 0；`python3 tests/test_corpus_manifest.py` → 退出码 0，126 个唯一项目清单结构有效；`python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py .` → 退出码 0；`git diff --check` → 退出码 0；`git push origin main` → 退出码 0；`git ls-remote --heads origin main` → `6c76be7`，与推送时 HEAD 一致。本条自身的提交和推送尚待下步完成，不把未运行结果记作已验证。
- 利用 / Reuse: 重装后可从 `https://github.com/shiyi-log/project-documentation.git` 克隆此仓库并对照远端 `main` SHA；本地 15 个技能、其他工作树和机器配置应另行进行私密离机备份与恢复校验。
- 限制 / Limits: 这不是全机备份；公开仓库不适合承载认证文件、SSH 私钥或未经筛查的本机技能；Time Machine 当前没有可用目标。集合仓库迁移和远端改名仍仅为设计，未实施。
- 下一步 / Next: 仅提交并推送本台账，核验远端最终 SHA；重装前由用户确定其他仓库的提交/推送范围与私密备份目的地，确认可读取备份后才能考虑抹盘。
