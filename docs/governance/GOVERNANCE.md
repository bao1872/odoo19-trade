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

### 模型讨论门槛（含安全例外）

- **默认**：至少连续 **5–10 个真实交易周期**出现同一结构性问题，才允许讨论新的核心业务模型。
- **可立即升级的例外**（仍需 Owner / Reviewer 批准，但不要求等待 5–10 单）：
  - security
  - compliance
  - legal
  - data integrity
  - accounting correctness
  - irreversible workflow constraint

## 1. Four Governance Layers

| 层级 | 核心问题 | 最终裁决者 |
|---|---|---|
| Business Governance | 这个功能值不值得做 | Owner |
| Architecture Governance | 应该配置还是开发 | Architect / Reviewer |
| Change Governance | Executor 可以改到什么程度 | Change Scope（§5） |
| Runtime Governance | 什么证据才算 Executor PASS | Verification Gate（RELEASE_CHECKLIST.md） |

## 2. Roles（由权限定义，不绑定工具）

### Owner

最终批准权：Business Model / Product Scope / Workflow / New Module / Schema / External Integration / Production / Destructive DB Operation。

### Architect / Reviewer

负责：方案设计、约束边界、审计、风险判断、是否值得工程化、给 Executor 明确 implementation contract。
**不直接覆盖 Owner 的业务决定。**

### Executor

可以：read / diagnose / edit approved scope / test / commit / push（在 scope 与 task contract 内）。
不可以自行：改业务模型 / 加新模块 / 换技术路线 / 改 DB schema / SQL 修正式数据 / 部署 / 安装依赖 / 扩展本轮 scope。

当前通常：

- ChatGPT = Architect / Reviewer
- IDE / Codex = Executor

> **authority follows role, not tool.** 换工具（Claude Code、人工开发者等）不改变上述权限边界。

反例（错误治理）：

```text
Requirement: verify responsive
Executor: no browser → install Chromium        ← 越权改环境
```

正确：

```text
no browser → report capability gap → look for approved tooling → STOP if unavailable
```

## 3. Three-Level Acceptance（核心护栏）

验收分三层，**Executor 无权宣布最终 PASS**：

1. **EXECUTOR PASS**
   Executor 完成 approved gates。允许按 task contract commit / push。
2. **REVIEWER PASS**
   Reviewer 从 canonical Git remote 独立检查实际 diff / files / evidence。
3. **OWNER ACCEPTED**
   Owner 接受业务结果。

规则：

- Executor **MUST NOT** 声明：`FINAL PASS` / `PROJECT COMPLETE` / `BASELINE COMPLETE`。
- Executor 只能声明：`EXECUTOR PASS — awaiting Reviewer audit`。
- 只有 **REVIEWER PASS** 之后，才允许称 engineering verification complete。
- **Executor PASS ≠ Reviewer PASS ≠ Owner Accepted。**

## 4. Push Policy

- **C0 / C1**：Executor gates PASS 后，允许 push 到当前 approved branch，供 Reviewer 从 remote 审计。
- **C2 / C3**：除非 task contract 明确允许，不得直接 push architecture / schema change 到 `master`。
- 当前项目暂不引入复杂 PR workflow。

禁止：

- force push
- rewrite shared history
- move baseline tags

## 5. Change Class

| Class | 例子 | 要求 |
|---|---|---|
| C0 | 文案、图片、CSS 微调 | targeted affected-page smoke |
| C1 | QWeb 页面、菜单、表单 | module upgrade + affected route + browser/runtime |
| C2 | schema、CRM 字段、business logic | clean install current code on empty DB + upgrade replay from immediately previous released module version + data test |
| C3 | 架构、模块、新 integration、production | 必须先设计评审 |

> 注意：QWeb / XML / SCSS 都属于 code change，必须按其 Change Class 验证（见 ARCHITECTURE §Boundary）。

## 6. Task Contract（任务执行合同）

每个 implementation task 开始时，Executor **必须先报告**：

```text
Goal:
Change Class:
Approved Scope:
Forbidden Scope:
Expected Invariants:
Required Evidence:
Commit/Push Policy:
```

Owner / Reviewer 给的任务即为 contract。

例（响应式验证）：

```text
Goal: responsive verification
Class: C0 verification
Approved Scope: browser smoke only
Forbidden: install dependencies
Invariant: no code change
Evidence: 390 / 768 / 1024 / 1440
```

如果在 Observe 阶段发现任务实际需要更高 Change Class：

> **STOP → 提出 reclassification → 等待授权。**

## 7. Code truth vs Runtime truth

所有审计报告必须分两项，最后才给 Executor PASS：

- **Static Evidence**：code / XML / manifest / schema / PO / paths
- **Runtime Evidence**：HTTP / DB state / rendered DOM / CRM persistence / menu hierarchy / browser behavior

以下语句视为**无效验收证据**：

> “代码逻辑确定性很高，所以风险低。”

- `XML 正确 ≠ Odoo runtime 正确`
- `PO 347/347 ≠ 中文页面正确`
- `Module install EXIT=0 ≠ 菜单结构正确`

## 8. Tooling / Environment Authority

任何新的以下项安装前**必须显式授权**（不只是“大型依赖”）：

- package
- pip dependency
- npm dependency
- browser
- system service
- Docker image
- external CLI

流程：

```text
1. find already-approved existing tool
2. report capability gap
3. STOP if unavailable
```

禁止自动 bootstrap environment。

## 9. Database Governance

- **Development DB 允许**：diagnostic SELECT / temporary TEST records / approved ORM configuration mutation / migration
- 改变 canonical persistent runtime configuration 也必须在 approved scope 内。
- 任何 TEST entity：**必须有可识别的 TEST marker**，并在 verification 后清理。
- **禁止（除非明确授权）**：直接 `UPDATE` / `DELETE` / `INSERT` 业务或 runtime 数据。
- 若诊断被迫 SQL 修复：仅用于**恢复实验环境**，不得作为最终修复；之后必须 `code fix → fresh install → upgrade replay` 证明无需手工 SQL 也能重建状态。

## 10. Data / Secrets / Privacy Governance

**Never commit：**

- password / API key / token
- cookie / session
- DB dump
- customer email / phone / name
- supplier confidential quote / price list
- private certification files
- real CRM export

- 进 Git 的 screenshot / review 材料**不得含真实客户 PII**。
- Production credentials **never** stored in repo。

## 11. Migration Governance

```text
Migration is immutable after release
except when explicitly neutralized for safety.
```

每个 migration 文件顶部必须写：

```text
Purpose:
From version:
Invariant:
Destructive: (yes/no)
Rollback assumption:
```

当前已存在迁移（module `trade_website`）：`19.0.1.0.3` / `19.0.1.0.5` / `19.0.1.0.6`（docstring 已在 v1.1 补齐）。

## 12. Content / Asset Governance

Git repo 可包含：
- runtime 使用的 production-safe 公开资产
- 经明确批准的 production-safe 发布资产

私有 / 源素材留在外部。

外部 / 私有「产品材料工作台」：

```text
product-material-workspace/
├── source/          ← 原始工厂照片、手机图
├── selected/        ← 选中素材
└── docs/            ← supplier 文档、报价、认证、内部备注
```

> 原始工厂照片 / supplier docs / quotes / certifications **MUST NOT** 自动进入 public Git repo。
> 只有经过批准的 production-safe derivative 才进入：
> `addons/trade_website/static/src/img/`

### 资产删除护栏

> **Zero runtime references are evidence of non-use, NOT authorization to delete an asset.**

删除资产前必须确认：
- asset class（资产类别）
- ownership（归属）
- external preservation（外部是否已留存）
- release intent（是否明确弃用发布）

仅以引用计数（reference count = 0）清理资产**禁止**。

## 13. Decision Log

极轻：`docs/DECISIONS.md`，每条 ADR 含 Decision / Reason / Status / Trigger to revisit。

## 14. KNOWN_GAPS vs Bug

- 未完成内容 → `docs/KNOWN_GAPS.md`，标 `STATUS / BLOCKING / OWNER / TRIGGER`
- 工程缺陷 → 才是 Bug

> Executor 不得把“未完成内容”误认为“工程缺陷”。

## 15. Release Baseline & Tag Policy

- `website-v1-baseline` → `460c28b`（**code baseline，在 governance docs 之前**）
- Governance framework 始于 `385ecb5`
- **Release / baseline tags 不可变。Never move an existing baseline tag。**
- 新工程基线创建**新 tag**（如 `website-v1.1-baseline` / `website-v2-baseline`），不得把 `website-v1-baseline` 移到新 commit。

## 16. Authority Precedence

1. Owner 明确的当前指令
2. 现行 GOVERNANCE 规则
3. accepted ADR
4. ARCHITECTURE
5. approved task contract
6. 既有实现 / 注释作为 evidence

但：Owner 若临时授权突破 governance guardrail（如 destructive DB operation / C3），**必须明确写出 exception scope**。重大长期例外应写 ADR。

## 17. CI Restraint

暂不建设：K8s / Docker pipeline / elaborate GitHub Actions / full E2E farm / release automation。

目前只自动化**便宜的 deterministic check**：

```text
XML parse / Python syntax / git diff --check / PO empty count / broken static refs / forbidden strings
```

等网站频繁改动再加：clean install smoke / browser smoke。
