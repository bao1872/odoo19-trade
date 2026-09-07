"""
v0.4 — build the website navigation hierarchy (idempotent).

Odoo renders each website's navigation from that website's own
"Top Menu for Website N" record. Menus declared in data XML with
parent_id="website.main_menu" (or with no website_id) never show up,
and every module upgrade would reset that parent again.

So `views/navigation.xml` only declares menu *entities* (name / url /
sequence) and this migration wires them into each website's top menu.

Target hierarchy:

    Home                        (official, untouched)
    Products            (20)
        All Products            (21)
        Cordless Air Duster     (22)
        Instant Print Camera    (23)
        Ultrasonic Cutter       (24)
    Our Solution        (30)
        Overview                (31)
        Manufacturing Control   (32)
        Quality & Documentation (33)
        Product Selection Focus (34)
    About               (50)
        About Us                (51)
        Contact                 (52)
    Request a Quote     (80)    (CTA)
"""

from odoo import SUPERUSER_ID, api

# (name, url, sequence, parent_name or None for top level)
# Parents must appear before their children.
MENU_TREE = [
    ("Products", "/products", 20, None),
    ("All Products", "/products", 21, "Products"),
    ("Cordless Air Duster", "/products/cordless-air-duster", 22, "Products"),
    ("Instant Print Camera", "/products/instant-print-camera", 23, "Products"),
    ("Ultrasonic Cutter", "/products/ultrasonic-cutter", 24, "Products"),

    ("Our Solution", "/solution", 30, None),
    ("Overview", "/solution", 31, "Our Solution"),
    ("Manufacturing Control", "/manufacturing", 32, "Our Solution"),
    ("Quality & Documentation", "/quality", 33, "Our Solution"),
    ("Product Selection Focus", "/our-advantage", 34, "Our Solution"),

    ("About", "/about-us", 50, None),
    ("About Us", "/about-us", 51, "About"),
    ("Contact", "/contactus", 52, "About"),

    ("Request a Quote", "/request-quote", 80, None),
]

# Legacy top-level entries now consolidated under Our Solution / About.
LEGACY_TOP_LEVEL = ("Manufacturing", "Quality", "Our Advantage")


def _find(Menu, name, website_id):
    """Existing record for this name: prefer website-owned, else unassigned."""
    menu = Menu.search([
        ("name", "=", name),
        ("website_id", "=", website_id),
    ], order="id", limit=1)
    if not menu:
        menu = Menu.search([
            ("name", "=", name),
            ("website_id", "=", False),
        ], order="id", limit=1)
    return menu


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    Menu = env["website.menu"].sudo()

    for website in env["website"].sudo().search([]):
        top_menu = Menu.search([
            ("website_id", "=", website.id),
            ("parent_id", "=", False),
            ("name", "like", "Top Menu for Website%"),
        ], limit=1)
        if not top_menu:
            continue

        # ---- Phase A: resolve + wire every node (parents first) --------
        node_id = {}
        for name, url, seq, parent_name in MENU_TREE:
            menu = _find(Menu, name, website.id)
            if not menu:
                menu = Menu.create({"name": name, "url": url})
            parent_id = node_id[parent_name] if parent_name else top_menu.id
            menu.write({
                "parent_id": parent_id,
                "website_id": website.id,
                "sequence": seq,
            })
            if not menu.child_id:
                # stored compute forces '#' on menus that have children
                menu.write({"url": url})
            node_id[name] = menu.id

        # ---- Phase B: drop leftovers of previous installs --------------
        # Same name, different record: children were re-parented in
        # phase A, so cascading here is safe.
        for name, _url, _seq, _parent in MENU_TREE:
            Menu.search([
                ("name", "=", name),
                ("id", "!=", node_id[name]),
                "|", ("website_id", "=", website.id), ("website_id", "=", False),
            ]).unlink()

        # ---- Phase C: remove legacy consolidated top-level entries -----
        for legacy in LEGACY_TOP_LEVEL:
            Menu.search([
                ("name", "=", legacy),
                "|", ("website_id", "=", website.id), ("website_id", "=", False),
            ]).unlink()