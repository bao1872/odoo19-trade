"""
Purpose:
    Wire navigation menu records into the website top menu via XML ID and mark noupdate.
From version:
    19.0.1.0.5
Invariant:
    All trade_website-owned menu records are wired by XML ID
    into the intended hierarchy and their ir.model.data records
    are marked noupdate.

    This migration alone does NOT guarantee the final five-item
    top-level navigation; duplicate Contact handling is completed
    by 19.0.1.0.6.
Destructive:
    no
Rollback assumption:
    No automatic rollback is supported.
    Restoring a pre-1.0.5 state requires an explicit code/data
    recovery plan; do not clear noupdate as an ad-hoc rollback.

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
