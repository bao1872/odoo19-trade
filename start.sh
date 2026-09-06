#!/bin/bash
# 启动 Odoo 19（前台运行，Ctrl+C 停止）
cd "$(dirname "$0")" || exit 1
mkdir -p logs data

# macOS Homebrew 的 psql/pg_config 不在默认 PATH 里，若存在则加进来
[ -d /opt/homebrew/opt/postgresql@17/bin ] && export PATH="/opt/homebrew/opt/postgresql@17/bin:$PATH"

exec ./venv/bin/python odoo-19/odoo-bin -c odoo.conf "$@"
