# RELEASE_CHECKLIST

按 Change Class 选对应 gate。所有 gate 都要求 **Observe** 先行（HEAD + clean tree + runtime state）。验证结论只能声明 **EXECUTOR PASS — awaiting Reviewer audit**（见 GOVERNANCE §3）。

## C0 — 文案 / 图片 / CSS 微调

- [ ] 改动在 approved scope
- [ ] syntax / XML checks **as applicable**（图片 / 纯 CSS 不强制 `py_compile`）
- [ ] targeted affected-page smoke：相关页面 HTTP 200，视觉无破损
- [ ] commit（不强制 full install）

## C1 — QWeb 页面 / 菜单 / 表单

- [ ] module `-u trade_website` upgrade EXIT=0
- [ ] affected route HTTP 200（含 `/en_US/` 与 `/zh_CN/`）
- [ ] browser / runtime：导航 / 菜单层级 / 表单渲染正确
- [ ] 双语各验证一次
- [ ] commit + push（供 Reviewer 从 remote 审计）

## C2 — schema / CRM 字段 / business logic

- [ ] 新 migration 文件含 Purpose / From / Invariant / Destructive / Rollback（见 GOVERNANCE §11）
- [ ] **clean install current code on empty DB** EXIT=0
- [ ] **upgrade replay from immediately previous released module version** 通过
- [ ] 数据测试：ORM 持久化 / 表单写入 / 字段迁移正确
- [ ] i18n 重新导出无遗漏
- [ ] commit；push 需 task contract 明确允许

## C3 — 架构 / 模块 / 新 integration / production

- [ ] 先有 ADR（DECISIONS.md）与 design review 批准
- [ ] Owner 显式授权
- [ ] 设计文档 + implementation contract
- [ ] 之后按 C2 级验证 + 额外 production gate
- [ ] 禁止 Executor 自行扩展 scope

## Universal STOP rules

- 验收没完成 → 不 push
- 测试环境与代码环境混用 → 报告并分离
- 越权（改 schema / 部署 / 自行加模块）→ STOP + report delta，等显式授权
- 禁止 force push / rewrite shared history / move baseline tags
