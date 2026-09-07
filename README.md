# Odoo 19 社区版开发环境

仓库：https://github.com/bao1872/odoo19-trade

Odoo 19.0（FINAL，源码来自 `odoo/odoo` 分支 `19.0`，commit `1a13cee`）。

## 目录结构

```
trade/
├── odoo-19/          # Odoo 19 社区版源码（上游，不入库，见 scripts/setup-odoo.sh）
├── addons/
│   ├── trade_core/       # 有意为空的未来业务扩展基础模块（当前无业务逻辑）
│   └── trade_website/    # 活动的公开 B2B 营销网站
├── venv/             # Python 虚拟环境
├── data/             # Odoo filestore / sessions
├── logs/             # 运行日志
├── odoo.conf         # 主配置
├── scripts/          # 环境脚本
└── start.sh          # 启动脚本
```

## 从零搭建

```bash
git clone https://github.com/bao1872/odoo19-trade.git && cd odoo19-trade
./scripts/setup-odoo.sh                 # 拉取 Odoo 19 源码（固定 commit 1a13cee）
python3 -m venv venv && ./venv/bin/pip install -r odoo-requirements.txt
brew services start postgresql@17       # 或已有 PostgreSQL；确保有可建库的 superuser
```

## 安装业务网站模块

`trade_website` 依赖：`website` + `website_crm`。
正式安装只安装 `trade_website` 即可（不再需要 `-i base,web,trade_core`）。

```bash
./start.sh \
  -d odoo19 \
  -i trade_website \
  --without-demo \
  --load-language=zh_CN \
  --stop-after-init
```

> `trade_core` 是预留的业务扩展基础模块，目前不含任何自定义逻辑；
> 仅在未来用真实交易验证工作流后再向内添加 CRM / 销售 / 采购 / 供应链扩展。

## 运行

```bash
brew services start postgresql@17      # 数据库
./start.sh -d odoo19                   # 启动，前台运行，Ctrl+C 停止
```

访问 http://127.0.0.1:8069 ，登录：`admin` / `admin`。

## 公开路由

| 路由 | 说明 |
| --- | --- |
| `/` | 首页 |
| `/products` | 产品列表 |
| `/solution` | 解决方案 |
| `/about-us` | 关于我们 |
| `/request-quote` | 获取报价（官方 `website_crm` 表单 → `crm.lead`） |

产品详情页：`/products/cordless-air-duster`、`/products/instant-print-camera`、
`/products/ultrasonic-cutter`。

## 已知内容等待项（非代码 bug）

- 站点临时公开品牌名为 `Global Sourcing`，待正式品牌确认后替换。
- 三款产品的真实规格参数目前为 **TBD**，待供应商确认后补全。
- 超声波刀附件区、`/solution` 的工厂 / QC / 港口三张示意图仍为 v04 视觉占位，
  待收到真实资料后替换。

## 常用命令

```bash
# 升级模块（--stop-after-init 表示装完退出）
./start.sh -d odoo19 -u trade_website --stop-after-init

# 重建数据库（重新初始化）
dropdb -h localhost odoo19
./start.sh -d odoo19 -i trade_website --without-demo --stop-after-init

# 查看日志
tail -f logs/odoo.log
```

## 环境

- Python 3.11.7（venv），依赖见 `odoo-19/requirements.txt`
- PostgreSQL 17（Homebrew `postgresql@17`），DB 用户默认为当前系统用户（需 superuser / createdb 权限）
- Node v22（前端资源构建）
- `wkhtmltopdf` 未安装，仅影响 PDF 报表打印，需要时 `brew install wkhtmltopdf`
