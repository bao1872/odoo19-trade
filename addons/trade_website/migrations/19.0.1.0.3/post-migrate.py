"""
Purpose:
    Legacy migration intentionally disabled / no-op.
From version:
    19.0.1.0.3
Invariant:
    No website menu or shared Odoo template is modified.
Destructive:
    no
Rollback assumption:
    Nothing was changed; safe to re-run or skip.

The original 19.0.1.0.3 migration managed website menus
by translatable names and could affect shared Odoo menu
templates.

Navigation is now owned by configure_navigation() and the
19.0.1.0.5 / 19.0.1.0.6 migrations.
"""


def migrate(cr, version):
    pass
