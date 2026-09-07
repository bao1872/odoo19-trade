"""
Legacy migration intentionally disabled.

The original 19.0.1.0.3 migration managed website menus
by translatable names and could affect shared Odoo menu
templates.

Navigation is now owned by configure_navigation() and the
19.0.1.0.5 / 19.0.1.0.6 migrations.
"""


def migrate(cr, version):
    pass
