"""
v0.6.2 — remove the duplicate custom Contact menu.

We used to ship our own ``trade_website.menu_contact`` under About, which
coexisted with Odoo's official ``website.menu_contactus`` (rendered
top-level on a clean install). That produced a 6th top-level menu, violating
the strict 5-top-menu constraint.

This migration removes ONLY our obsolete duplicate and then re-wires the
navigation via ``configure_navigation``, which now reuses the official
``website.menu_contactus`` under our About group.

DO NOT unlink ``website.menu_home`` or ``website.menu_contactus`` — those are
official menus we intentionally reuse.
"""

from odoo import SUPERUSER_ID, api
from odoo.addons.trade_website.hooks import configure_navigation


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})

    # Remove only OUR obsolete duplicate Contact menu.
    obsolete_contact = env.ref(
        "trade_website.menu_contact",
        raise_if_not_found=False,
    )

    if obsolete_contact:
        obsolete_contact.sudo().unlink()

    configure_navigation(env)
