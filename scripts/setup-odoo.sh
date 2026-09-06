#!/bin/bash
# 拉取 Odoo 19 社区版源码（固定到已验证的 commit，可重复执行）
set -e
cd "$(dirname "$0")/.." || exit 1

ODOO_COMMIT=1a13ceeaee12fe5cc50f287c31f217d4be2a2eaf

if [ -d odoo-19 ]; then
    echo "odoo-19 已存在，跳过"
    exit 0
fi

git clone --depth 1 --branch 19.0 --single-branch https://github.com/odoo/odoo.git odoo-19
cd odoo-19
git fetch --depth 1 origin "$ODOO_COMMIT"
git checkout "$ODOO_COMMIT"
echo "Odoo 源码就绪于 $(pwd)"
