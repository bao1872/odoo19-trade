# Production Deployment — odoo19-trade

First production deployment topology for `175.178.86.231`.

## First-deployment topology (C3, Owner-authorized)

    Internet :8069
        ↓
    Odoo 19 (public)
    0.0.0.0:8069
        ↓
    local PostgreSQL (localhost only)
    DB = odoo19

- Public endpoint: http://175.178.86.231:8069/
- Odoo binds `0.0.0.0:8069` directly (no reverse proxy in front).
- PostgreSQL listens only on `127.0.0.1:5432`.

## Collision deviation (Phase 2 gate)

Port 80 was already occupied by an existing, unrelated application
`lineagem` (nginx catch-all `server_name _` → 301 → :8001). Per the
C3 contract ("do not overwrite unrelated server blocks", "stop unrelated
services occupying port 80 is NOT authorized"), Odoo is served directly
on `:8069` instead of behind nginx `:80`.

`deploy/nginx/odoo19-trade.conf` is retained as a reference and MUST NOT
be installed until port 80 is freed for Odoo.

## Files

- `systemd/odoo19-trade.service` — systemd unit (User=odoo).
- `odoo-prod.conf.example` — production config template (no secrets).
- `nginx/odoo19-trade.conf` — DEFERRED reverse-proxy config for :80.

## Server layout

    /opt/odoo19-trade/          Git code + pinned Odoo source + venv
    /etc/odoo19-trade.conf      production config + secrets (0640 root:odoo)
    /var/lib/odoo19-trade/      filestore/session data (odoo:odoo)
    /var/log/odoo19-trade/      logs (odoo:odoo)
    /var/backups/odoo19-trade/  manual DB backups

## Deployment notes

- Fresh production DB `odoo19` (local dev DB is NOT imported).
- Odoo upstream pinned at `1a13ceeaee12fe5cc50f287c31f217d4be2a2eaf`.
- HTTP only (no TLS). Treat as temporary; add domain + Let's Encrypt later.
- Do not enter admin password / collect sensitive data over HTTP.
