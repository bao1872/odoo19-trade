# GOVERNANCE

> 项目宪法：**Odoo 服务业务，而不是业务去适应 Odoo。**
> 治理一句话：**Business evidence controls architecture; authority controls changes; runtime evidence controls PASS.**

## 0. Project Constitution — Stage 1: Business Validation

当前阶段目标：跑通

```text
Buyer Lead → Product Discussion → RFQ → Sample → Quote → Order
→ Factory Coordination → QC → Shipment → Payment / Invoice
```

在真实订单证明之前，**不做**：

- 复杂权限体系
- 完整产品主数据平台
- 自建 workflow engine
- 复杂 connector framework
- 独立 mobile app
- 过细 CRM 字段
- 自定义 MRP

宪法条款：

> **No custom business model before repeated real-world evidence demonstrates that the official Odoo model is insufficient.**
> 门槛：**至少连续 5–10 个真实交易周期出现同一结构性问题，才允许讨论新的核心业务模型。**

## 1. Four Governance Layers

| 层级 | 核心问题 | 最终裁决者 |
|---|---|---|
| Business Governance | 这个功能值不值得做 | Owner（你） |
| Architecture Governance | 应该配置还是开发 | Architect / Reviewer |
| Change Governance | IDE 可以改到什么程度 | Change Scope（§4） |
| Runtime Governance | 什么证据才算 PASS | Verification Gate（RELEASE_CHECKLIST.md） |

## 2. Roles

### Owner — 你
最终批准权：Business Model / Product Scope / Workflow / New Module / Schema / External Integration / Production / Destructive DB Operation。

### Architect / Reviewer — AI（我）
负责：方案设计、约束边界、审计、风险判断、是否值得工程化、给 IDE 明确 implementation contract。
**不直接覆盖你的业务决定。**

### Executor — IDE
可以：read / diagnose / edit approved scope / test / commit / push（scope 内）。
不可以自行：改业务模型 / 加新模块 / 换技术路线 / 改 DB schema / SQL 修正式数据 / 部署 / 安装大型依赖 / 扩展本轮 scope。

反例（错误治理）：

```text
Requirement: verify responsive
IDE: no browser → install Chromium        ← 越权改环境
```

正确：

```text
no browser → report capability gap → look for approved tooling → STOP if unavailable
```

## 3. Exploration-First（写代码前 8 步）

```text
1. Observe        2. Establish Authority   3. Define Delta
4. Implement      5. Verify               6. Commit
7. Push           8. Report
```

前三步（Observe / Establish Authority / Define Delta）**不得写代码**。

### Observe 必答

- 当前 HEAD 是什么？
- working tree 是否 clean？
- 当前真实运行状态是什么？
- 代码 owner 在哪里？
- DB 的 canonical state 是什么？

### Establish Authority 核心原则

> **Never mutate an object until its runtime ownership is established.**

例：菜单治理中 `website.menu_home` 只是 template menu，不是运行菜单，不得据此修改。

## 4. Change Class

| Class | 例子 | 要求 |
|---|---|---|
| C0 | 文案、图片、CSS 微调 | targeted smoke |
| C1 | QWeb 页面、菜单、表单 | module upgrade + route + browser |
| C2 | schema、CRM 字段、business logic | clean install + migration + data test |
| C3 | 架构、模块、新 integration、production | 必须先设计评审 |

## 5. Code truth vs Runtime truth

所有审计报告必须分两项，最后才给 PASS：

- **Static Evidence**：code / XML / manifest / schema / PO / paths
- **Runtime Evidence**：HTTP / DB state / rendered DOM / CRM persistence / menu hierarchy / browser behavior

以下语句视为**无效验收证据**：

> “代码逻辑确定性很高，所以风险低。”

- `XML 正确 ≠ Odoo runtime 正确`
- `PO 347/347 ≠ 中文页面正确`
- `Module install EXIT=0 ≠ 菜单结构正确`

## 6. Database Governance

- **Development DB 允许**：diagnostic SELECT / temporary test data / ORM mutation / migration
- **禁止（除非明确授权）**：直接 `UPDATE` / `DELETE` / `INSERT` 业务或 runtime 数据
- 若诊断被迫 SQL 修复：仅用于**恢复实验环境**，不得作为最终修复；之后必须 `code fix → fresh install → upgrade replay` 证明无需手工 SQL 也能重建状态。

## 7. Migration Governance

```text
Migration is immutable after release
except when explicitly neutralized for safety.
```

每个 migration 文件顶部必须写：

```text
Purpose / From version / Invariant / Destructive? (yes/no) / Rollback assumption
```

当前已存在迁移（module `trade_website`）：`19.0.1.0.3` / `19.0.1.0.5` / `19.0.1.0.6`。

## 8. Content / Asset Governance

资产分离：

```text
assets/
├── production/   ← Odoo module 只放这一层
├── source/      ← 原始工厂资料、手机图
└── reference/   ← 未使用 detail 图，不依赖 Git 模板引用决定生死
```

本项目沿用：

```text
addons/trade_website/static/src/img/products/<sku>/{source,selected,docs}
```

> 项目真正有价值的数据：工厂信息 + 参数 + 认证 + 包装 + MOQ + 图片 + 报价 + buyer feedback。

## 9. Decision Log

极轻：`docs/DECISIONS.md`，每条 ADR 仅含 Decision / Reason / Trigger to revisit。

## 10. KNOWN_GAPS vs Bug

- 未完成内容 → `docs/KNOWN_GAPS.md`，标 `BLOCKING / OWNER / TRIGGER`
- 工程缺陷 → 才是 Bug

> IDE 不得把“未完成内容”误认为“工程缺陷”。

## 11. Release Baseline

- `460c28b` = **Website v1 Engineering Baseline**（tag `website-v1-baseline`）
- 所有功能从 baseline 往前；baseline ↔ current 一 compare 即知变化。

## 12. CI Restraint

暂不建设：K8s / Docker pipeline / elaborate GitHub Actions / full E2E farm / release automation。

目前只自动化**便宜的 deterministic check**：

```text
XML parse / Python syntax / git diff --check / PO empty count / broken static refs / forbidden strings
```

等网站频繁改动再加：clean install smoke / browser smoke。
