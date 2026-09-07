"""
Purpose:
    Remove obsolete duplicate custom Contact menu and rewire per-website actual menu.
From version:
    19.0.1.0.6
Invariant:
    Final per-website top-level navigation contains exactly
    five items. The website-generated per-website Contact
    menu copy is placed under About. The shared
    website.menu_contactus template remains untouched.
Destructive:
    yes — unlinks ONLY trade_website.menu_contact (our obsolete duplicate).
Rollback assumption:
    No routine automatic rollback.
    The custom trade_website.menu_contact entity is obsolete
    by design and must not be independently recreated.
    Any rollback must restore code and data consistently.

We used to ship our own ``trade_website.menu_contact`` under About, which
coexisted with Odoo's official ``website.menu_contactus`` (rendered
top-level on a clean install). That produced a 6th top-level menu, violating
the strict 5-top-menu constraint.

This migration removes ONLY our obsolete duplicate and then re-wires the
navigation via ``configure_navigation``, which reuses the website-generated
per-website Contact menu copy — never the shared ``website.menu_contactus``
template record. The real runtime copy has no XML ID and is located by
website scope + top-menu context + exact URL.

DO NOT unlink ``website.menu_home``. DO NOT mutate the shared
``website.menu_contactus`` template (its ``website_id`` is NULL); only the
per-website copy may be repositioned.
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
