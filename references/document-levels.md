# 文档层级

按项目复杂度和风险选择，不按个人或公司的所有者身份选择。

## 第 1 级——基础或单组件项目

通常足够：

```text
README.md
setup or quickstart
CHANGELOG.md (if releases matter)
TODO or issue tracker (if follow-up work matters)
```

如果更清晰，可以把小文档合并到 README。

## 第 2 级——库或多模块项目

按需增加：

```text
API / usage docs
development / contribution guide
testing guide
architecture or decision notes
data model
```

## 第 3 级——长期运行或对外使用的服务

按需增加：

```text
deployment
operations / runbook
monitoring and alerts
backup and recovery
incident response
security and configuration
```

## 第 4 级——高风险或受监管项目

只有确有理由时增加：

```text
threat model
access control
data retention
audit evidence
compliance
change management
```

任何级别都可以用于个人项目。不要仅因为层级清单列出了某类文档，就创建没有内容的空文档。
