# NORTHSTAR — ha-dani-ops

**Infra we actually learned (paths, not passwords):**
- AMS user `danielcliente` (proof: `dev/ha-live/proof/HA-SERVICE-PUMA-INFRA.md`)
- Dash `puma.jailbroken.tech` — `/health` `/api/service` `/api/perimeter`
- Perimeter hosts: lx-prod/uat, front, cdn-s3, ws-ferhub, ws-gplaygap, gppay, PAM Calimaco **staging**,
  operator wallets, tgio-ar, 24vivo, enracha-agents
- **bad:** elite-play BFF 503 — **theirs**, not an HA outage
- S3 canary still public (cite, do not fetch objects)
- HOLDs baked into the service doc: no jailbroken-tenant mix, no live patch `api.gplaygap.com`, no money-write

**DONE** = a change window exists, perimeter is current (disk and/or SOCKS GET of health),
and any live write is HOLD.

`danielcliente` has **no HA token**. Do not try to arm HA on that user.
Third-party health: SOCKS only.

## Not this pack

Live nginx/API patch on gplaygap. Restart AMS as root. Mixing loot unit into client reports.
Money-write. Mac ISP.

## Acceptance

1. Down hosts named honestly. elite-play 503 classified as theirs.
2. Dash passwords never appear in OUT (path to ACCESS.md only).
3. HOLD.md always present while live-patch remains forbidden.
