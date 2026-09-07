# ARCHITECTURE

> Odoo 服务业务。优先配置，其次开发。

## Boundary

- **Configure（不写代码）**：网站菜单、页面内容、i18n 翻译、网站表单字段映射、主题样式 —— 用 Odoo 官方能力与 QWeb/XML。
- **Develop（C2/C3）**：仅当官方模型 / 配置不足以支撑**已验证**的真实业务结构。

## Out of Scope（来自 `trade_website/__manifest__.py`）

- eCommerce checkout
- dynamic product catalog
- custom product model
- sales / purchase customization

## Module Map

- `trade_core`：业务核心（共享逻辑如有）
- `trade_website`：公开 B2B 营销站
  - depends：`website`, `website_crm`
  - version：`19.0.1.0.6`
  - 网站表单 → 官方 `crm.lead`（不自定义字段，见 DECISIONS ADR-002）
  - i18n：EN (`en_US`) + ZH (`zh_CN`)，PO 347 条
  - 产品：`air-duster` / `instant-print-camera` / `ultrasonic-cutter`

## When to escalate to C3

出现以下任一 → 先设计评审，IDE 不得直接做：

- 新增 Odoo 模块
- 自定义业务模型 / 新核心实体
- 新外部 integration（支付、物流、ERP 对接）
- production 变更 / 部署
- 替换技术路线

## Runtime Ownership Rule

> **Never mutate an object until its runtime ownership is established.**

修改任何对象前先确认：它在 runtime 中由谁拥有（XML ID? template? DB record? post_init_hook?）。
