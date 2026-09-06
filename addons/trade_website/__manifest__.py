{
    "name": "Trade Website",
    "summary": "B2B sourcing and manufacturing website",
    "description": """
Trade Website
=============

Official website UI for the trading business.

Scope of this module:
- public website homepage (QWeb + SCSS)

Out of scope:
- product / eCommerce logic
- CRM / sales automation
- custom models and controllers
    """,
    "author": "My Company",
    "website": "https://www.yourcompany.com",
    "category": "Website/Website",
    "version": "19.0.1.0.0",
    "license": "LGPL-3",
    "depends": ["website"],
    "data": [
        "views/homepage.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "trade_website/static/src/scss/homepage.scss",
        ],
    },
    "installable": True,
    "application": False,
}
