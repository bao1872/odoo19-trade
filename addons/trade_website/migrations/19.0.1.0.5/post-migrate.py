"""
v0.5 — repair / stabilize the website navigation hierarchy.

The menu records in ``views/navigation.xml`` are now created with
``noupdate="1"`` and carry no parent_id / website_id. This migration wires
them into the website's top menu (keyed by XML ID, not by the translatable
name) and marks their ir.model.data as noupdate so future upgrades never
strip the parent_id that was just set.

See addons/trade_website/hooks.py for the hierarchy definition.
"""

from odoo import SUPERUSER_ID, api
from odoo.addons.trade_website.hooks import configure_navigation


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})

    configure_navigation(env)

    env["ir.model.data"].sudo().search([
        ("module", "=", "trade_website"),
        ("model", "=", "website.menu"),
    ]).write({
        "noupdate": True,
    })
