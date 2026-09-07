{
    "name": "Trade Website",
    "summary": "B2B sourcing and manufacturing website",
    "description": """
Trade Website
=============

Public B2B marketing website for the trading business.

Scope:
- public B2B marketing website
- homepage
- product index / product detail pages
- manufacturing / quality / company pages
- request a quote form (official website form -> crm.lead)

Out of scope:
- eCommerce checkout
- dynamic product catalog
- custom product model
- sales/purchase customization
    """,
    "author": "Trade Website",
    "category": "Website/Website",
    "version": "19.0.1.0.5",
    "license": "LGPL-3",
    "depends": ["website", "website_crm"],
    "post_init_hook": "post_init_hook",
    "data": [
        "views/homepage.xml",
        "views/products.xml",
        "views/solution.xml",
        "views/company_pages.xml",
        "views/request_quote.xml",
        "views/navigation.xml",
        "views/header.xml",
        "views/footer.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "trade_website/static/src/scss/site.scss",
            "trade_website/static/src/scss/homepage.scss",
            "trade_website/static/src/scss/products.scss",
            "trade_website/static/src/scss/pages.scss",
        ],
    },
    "installable": True,
    "application": False,
}
