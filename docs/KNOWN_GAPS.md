# KNOWN_GAPS

> 这些是**未完成内容**，不是工程缺陷。`BLOCKING: no` 表示不阻塞 v1 发布。

## GAP-001 — Global Sourcing 临时品牌名

- BLOCKING: no
- OWNER: business / supplier
- TRIGGER: 收到正式品牌命名
- Note: 当前用临时名占位，非 bug。

## GAP-002 — 产品参数 TBD

- BLOCKING: no
- OWNER: supplier
- TRIGGER: 工厂提供真实规格参数
- Note: 页面参数区为占位，待工厂资料到位替换。

## GAP-003 — accessories-kit 占位图

- BLOCKING: no
- OWNER: business
- TRIGGER: 真实配件包素材到位
- Note: `static/src/img/v04/products/accessories-kit.webp` 为占位。

## GAP-004 — v04 supply 占位图

- BLOCKING: no
- OWNER: business
- TRIGGER: 真实工厂 / QC / 出货素材到位
- Note: `static/src/img/v04/supply/*` 为占位。

## 明确 NOT a gap

- **Product Interest 未单独存储**：已确认存入 `crm.lead.description`（见 DECISIONS ADR-002），属设计选择，非缺陷。
