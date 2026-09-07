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
- Decision: 顶级菜单固定 5 项；About 下使用 Odoo 为该 website 创建的 per-website Contact menu copy；不创建 trade_website 自定义 Contact；绝不修改 shared XML-ID template `website.menu_contactus`。
- Reason: Odoo 19 的 `website.menu_contactus` XML ID 指向 shared template；真正 runtime menu 是 website-scoped copy，无该 XML ID。`trade_website.menu_contact` 已被证明是错误的 duplicate entity。
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

## ADR-006 — Production Deployment Topology (first deployment)

- Status: Accepted
- Date: 2026-09-07
- Decision: First production deployment of odoo19-trade on `175.178.86.231`
  uses native Ubuntu + systemd, with Odoo served **directly on public port
  8069** (`0.0.0.0:8069`), PostgreSQL local-only (DB `odoo19`). Nginx is NOT
  placed in front of Odoo in this first deployment.
- Reason: Port 80 was already occupied by an existing, unrelated application
  `lineagem` (nginx catch-all `server_name _` → 301 → :8001). The C3 contract
  forbids overwriting unrelated server blocks and forbids stopping unrelated
  services occupying port 80 without separate authorization. Owner resolved
  the collision by serving Odoo on `:8069`. Fresh production DB (local dev DB
  not imported). Native deployment (Docker not used; Docker absent on server).
- Trigger to revisit:
  - port 80 is freed for Odoo → install `deploy/nginx/odoo19-trade.conf`,
    switch Odoo to `127.0.0.1:8069` + `proxy_mode=True`, add 80→443 + TLS.
  - multiple application nodes / orchestration needs emerge.
  - hosting environment changes.
