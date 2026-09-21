# AUTONOMY — ha-ppdev

## Default: autonomous dispatch

Operator says `/ha-ppdev` or “recreá el backend/API” → parent:

1. Resolve `PPDEV_OUT` (default `~/dev/pumapay`); `mkdir -p`
2. Preflight: HA live, disk writable, bus path exists
3. Launch workflow `ha-ppdev` (or `ctl.sh auto --out`)
4. Parallel remainder lanes (skip READY)
5. Always finish with `ppd-sync` + `ppd-lead`
6. Verify: ARCHITECTURE + openapi path exist OR HOLD with blocker in SUMMARY

## Stack default (if operator silent)

- Runtime: **Node/TypeScript** (Fastify or Nest — arch lane picks one ADR)
- DB: **Postgres**
- Cache/queue: **Redis**
- Migrations: SQL or Drizzle/Prisma — arch documents choice
- OpenAPI 3.1 as contract source of truth

Operator can override in the brief; do not bikeshed forever.

## Wave order (recommended)

Wave A (blocking): `arch` ∥ `tooling`  
Wave B: `api` ∥ `db` ∥ `auth`  
Wave C: `backend` ∥ `workers`  
Wave D: `test` → `sync` → `lead`

## Never

- Nested `grok -p`
- Spawn peer teams from a lane
- Claim DONE without disk evidence
- Put monorepo inside `~/Desktop/puma/` loot root
