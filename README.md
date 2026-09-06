# Odoo 19 社区版开发环境

仓库：https://github.com/bao1872/odoo19-trade

Odoo 19.0（FINAL，源码来自 `odoo/odoo` 分支 `19.0`，commit `1a13cee`）。

## 目录结构

```
trade/
├── odoo-19/          # Odoo 19 社区版源码（上游，不入库，见 scripts/setup-odoo.sh）
├── addons/           # 自定义模块（trade_core 为脚手架示例）
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
./start.sh -d odoo19 -i base,web,trade_core --without-demo --stop-after-init
```

首次上线前请把 `odoo.conf` 里的 `admin_passwd` 改成自己的值（留空默认为 `admin`）。

## 运行

```bash
brew services start postgresql@17      # 数据库
./start.sh -d odoo19                   # 启动，前台运行，Ctrl+C 停止
```

访问 http://127.0.0.1:8069 ，登录：`admin` / `admin`。

## 常用命令

```bash
# 新建模块脚手架
./venv/bin/python odoo-19/odoo-bin scaffold my_module addons

# 安装 / 升级模块（--stop-after-init 表示装完退出）
./start.sh -d odoo19 -i my_module --stop-after-init
./start.sh -d odoo19 -u my_module --stop-after-init

# 重建数据库（重新初始化）
dropdb -h localhost odoo19
./start.sh -d odoo19 -i base,web,trade_core --without-demo --stop-after-init

# 查看日志
tail -f logs/odoo.log
```

## 环境

- Python 3.11.7（venv），依赖见 `odoo-19/requirements.txt`
- PostgreSQL 17（Homebrew `postgresql@17`），DB 用户默认为当前系统用户（需 superuser / createdb 权限）
- Node v22（前端资源构建）
- `wkhtmltopdf` 未安装，仅影响 PDF 报表打印，需要时 `brew install wkhtmltopdf`
