# ARCHITECTURE

> Odoo 服务业务。优先配置，其次开发。

## Boundary

- **Presentation / Configuration Layer**（仍属 code change，须按 Change Class 验证）：
  - QWeb / XML
  - SCSS
  - i18n
  - 官方 Odoo 配置
  - **但不引入新的** Python business logic / schema / custom core model
- **Develop（C2/C3）**：仅当官方模型 / 配置不足以支撑**已验证**的真实业务结构。

> QWeb / XML / SCSS 仍然属于 code change，必须按 Change Class 验证，不能因“Configure”而绕开 gate。

## Out of Scope（来自 `trade_website/__manifest__.py`）

- eCommerce checkout
- dynamic product catalog
- custom product model
- sales / purchase customization

## Module Map

- `trade_core`：reserved, intentionally empty business-extension foundation（当前无业务逻辑，仅为未来扩展预留）
- `trade_website`：公开 B2B 营销站
  - depends：`website`, `website_crm`
  - version：`19.0.1.0.6`
  - 网站表单 → 官方 `crm.lead`（不自定义字段，见 DECISIONS ADR-002）
  - i18n：EN (`en_US`) + ZH (`zh_CN`)，PO 347 条
  - 产品：`air-duster` / `instant-print-camera` / `ultrasonic-cutter`

## Supported Public Locales（语言不变量）

- Primary / default：`en_US`
- Secondary：`zh_CN`
- 两者必须保持 active。

Runtime invariant：

```text
/          => English default
/en_US/    => English
/zh_CN/    => Simplified Chinese
```

- 若 Odoo canonical redirect 改写 `/en_US/`，实际 canonical English path 可接受，但 `/` 必须面向英文。
- **任何改变 default locale = Business Governance decision。**
- 本轮只写文档，不修改当前 DB / language config。

## When to escalate to C3

出现以下任一 → 先设计评审，Executor 不得直接做：

- 新增 Odoo 模块
- 自定义业务模型 / 新核心实体
- 新外部 integration（支付、物流、ERP 对接）
- production 变更 / 部署
- 替换技术路线

## Runtime Ownership Rule

> **Never mutate an object until its runtime ownership is established.**

修改任何对象前先确认：它在 runtime 中由谁拥有（XML ID? template? DB record? post_init_hook?）。
