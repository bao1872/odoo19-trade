"""
Navigation integrity.

Odoo renders each website's navigation from that website's own
``website.menu_id`` (the "Top Menu for Website N" record). The records in
``views/navigation.xml`` are declared as independent entities (no
``parent_id`` / ``website_id``) on purpose: writing a fixed parent in XML
would be reset on every module upgrade.

So the hierarchy is owned here, keyed strictly by **XML ID** (never by the
translatable ``name`` field). Two callers use it:

* ``post_init_hook``  — fresh install (records created by XML, then wired).
* ``migrations/19.0.1.0.5/post-migrate.py`` — existing DB upgrade.

(MENU_TREE order matters: a parent must appear before its children.)
"""

MENU_TREE = [
    ("menu_products", None, 20),
    ("menu_products_all", "menu_products", 21),
    ("menu_product_air_duster", "menu_products", 22),
    ("menu_product_instant_camera", "menu_products", 23),
    ("menu_product_ultrasonic_cutter", "menu_products", 24),

    ("menu_solution", None, 30),
    ("menu_solution_overview", "menu_solution", 31),
    ("menu_manufacturing", "menu_solution", 32),
    ("menu_quality", "menu_solution", 33),
    ("menu_our_advantage", "menu_solution", 34),

    ("menu_about", None, 50),
    ("menu_about_us", "menu_about", 51),
    ("menu_contact", "menu_about", 52),

    ("menu_request_quote", None, 80),
]


def configure_navigation(env):
    """Wire the trade_website menu records into the website's top menu."""
    website = env["website"].sudo().search([], order="id", limit=1)
    if not website:
        return

    top_menu = website.menu_id.sudo()
    resolved = {}

    for xml_name, parent_xml_name, sequence in MENU_TREE:
        menu = env.ref(
            f"trade_website.{xml_name}",
            raise_if_not_found=False,
        )
        if not menu:
            raise RuntimeError(
                f"Missing website menu XML ID: "
                f"trade_website.{xml_name}"
            )

        parent = (
            resolved[parent_xml_name]
            if parent_xml_name
            else top_menu
        )

        menu.sudo().write({
            "website_id": website.id,
            "parent_id": parent.id,
            "sequence": sequence,
        })

        resolved[xml_name] = menu


def post_init_hook(env):
    configure_navigation(env)
