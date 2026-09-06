#!/bin/bash
# 启动 Odoo 19（前台运行，Ctrl+C 停止）
cd "$(dirname "$0")" || exit 1
export PATH="/opt/homebrew/opt/postgresql@17/bin:$PATH"
exec ./venv/bin/python odoo-19/odoo-bin -c odoo.conf "$@"
