# DECISIONS (ADR)

> 轻量决策日志。每条含 Decision / Reason / Status / Trigger to revisit。
> Status 取值：Proposed / Accepted / Superseded（Superseded 须链接替代 ADR）。

## ADR-001 — Website v1 Engineering Baseline

- Status: Accepted
- Date: 2026-09-07
- Decision: 以 commit `460c28b` 作为 Website v1 工程基线，打 tag `website-v1-baseline`。
- Reason: 代码、菜单、i18n、双语运行、CRM 表单、响应式、clean install / upgrade 均已跑通；之后无为验收制造的无意义提交。
- Trigger to revisit: 下一个需破坏基线兼容的大变更前，先评估是否新建 baseline（新 tag，不移动旧 tag）。

## ADR-002 — 不创建 crm.lead Product Interest 自定义字段

- Status: Accepted
- Date: 2026-09-07
- Decision: 网站表单的产品兴趣写入官方 `crm.lead.description`，**不**新增 `crm.lead.product_interest` 字段。
- Reason: 仅 3 个产品；description 已保存稳定英文值，且不泄漏中文产品名（如「无线电动吹尘器」）。
- Trigger to revisit: 需要按产品做 CRM 过滤 / 报表 / 自动化时。

## ADR-003 — 菜单结构：5 个顶级项，About 收纳 Contact

- Status: Accepted
- Date: 2026-09-07
- Decision: 顶级菜单固定 5 项（EN+ZH 各一）；About 下含 About Us / Contact us；复用官方 website contact 菜单，不自定义。
- Reason: runtime 证明 `website.menu_home` 仅为 template menu，非运行菜单；必须按真实运行层级治理。
- Trigger to revisit: 业务需要新增顶级栏目（如独立 Solutions / Blog）时。

## ADR-004 — 资产治理：production-safe 进 repo，源素材留外部

- Status: Accepted
- Date: 2026-09-07
- Decision: Git repo 只放 production-safe / public runtime 资产；原始工厂照片 / supplier 文档 / 报价 / 认证留外部 product-material workspace，不自动进 public Git repo。
- Reason: 曾因 reference count=0 误删真实产品 detail 图；且客户 / 供应商机密不应默认进公开仓库。
- Trigger to revisit: 引入「产品材料包」结构时沿用本约定。

## ADR-005 — 数据库：禁止手工 SQL 修正式数据

- Status: Accepted
- Date: 2026-09-07
- Decision: 直接 `UPDATE` / `DELETE` / `INSERT` 业务 / runtime 数据需 Owner 显式授权；诊断用 SQL 仅恢复实验环境，最终须用 code + migration 重建。
- Reason: 前几轮直接改 `arch_db`、SQL 删记录是最大风险源。
- Trigger to revisit: 永不默认放宽。
