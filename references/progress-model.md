# 进度模型

进度跟踪是可选项。只有任务跨多个文件、依赖外部检查、需要交接，或存在有意义的阻断/未运行状态时才使用；微小编辑不要创建额外进度系统。

## 任务状态

```text
unscoped → routed → in-progress → review → verification → complete
                         ├→ blocked
                         ├→ not-implemented
                         ├→ not-run
                         └→ cancelled
```

`complete` 只表示约定的任务边界已满足，不表示整个项目、生产部署或外部验收完成。

## 技能实现阶段

```text
design
→ route-map
→ references
→ skill-body
→ RED baseline
→ GREEN verification
→ REFACTOR
→ GitHub validation
→ release
```

技能实现进度必须与用户项目功能进度分开。“技能正文存在”不等于“技能已验证”。

## 证据标签

使用精确标签：

- `verified`：声明的检查确实运行并产生支持证据；
- `not-run`：本次没有尝试该检查；
- `blocked`：前置条件阻止了检查；
- `planned`：计划做但尚未实现；
- `partial`：只检查了请求边界的一部分。

对于 100 项目规模验证，还要记录固定 SHA、仓库唯一性、证据类别和逐项目限制。项目统计不能替代项目级记录。

如果省略进度系统，最终回复仍要提供简短状态和下一步。
