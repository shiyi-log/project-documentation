# 路由图

路由是可选的决策辅助工具，用来说明文档任务为何采用某条路径；它不是强制工作流，也不要求创建 route 文件。

## 路由键

```text
<intent>.<project_profile>.<artifact>.<risk>.<evidence>
```

### 意图

`create`, `update`, `review`, `audit`, `migrate`, `archive`

### 项目画像

`basic`, `library`, `multi_module`, `service`, `platform`, `infra`, `regulated`

### 文档产物

`readme`, `setup`, `architecture`, `api`, `data`, `ops`, `security`, `changelog`, `decision`

### 风险与证据

Risk: `low`, `medium`, `high`, `regulated`
Evidence: `static`, `test`, `runtime`, `external`, `production`

## 路由优先级

1. 用户明确的目标和范围。
2. 已授权动作和禁止的副作用。
3. 实际仓库结构、源码、配置、测试和现有文档。
4. 生命周期、风险、外部依赖和受众。
5. 该规则的权威来源。
6. 默认模板。

不能仅凭“个人项目”或“企业项目”推断路由。

## 升级信号

如果任务涉及数据库、迁移、支付、隐私、生产、链操作、多服务、外部权威文档、兼容性、生成产物、发布或受监管数据，建议升级到更高风险路由。

发生行为变更时，路由不能停留在展示层：

```text
implementation → public contract/API → compatibility/migration → generated docs → tests → release/operations
```

不能仅因为 README 或 changelog 容易编辑，就假设它是权威来源。

## 降级信号

如果任务只是改一行文字、修改单个低风险文件，或边界明确且不影响行为与运维，可以使用更小的路由。

## 输出示例

```text
route: update.service.data.high.runtime
authority: migration source + service contract + deployment guide
docs: must update migration/upgrade notes; may update architecture; README out of scope
ledger: recommended because the migration is persistent and rollback-sensitive
progress: in-progress
next: inspect existing migration and upgrade-order documentation
```
