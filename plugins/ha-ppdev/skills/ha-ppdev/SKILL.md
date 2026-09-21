---
name: ha-ppdev
description: >
  Dispatch the PumaPay Platform Dev team (ppd-arch, ppd-api, ppd-backend,
  ppd-db, ppd-auth, ppd-workers, ppd-test, ppd-tooling, ppd-sync, ppd-lead)
  to build the greenfield API+backend monorepo from zero. OpenAPI-first;
  implements domain contracts from ha-ledger/payments/risk/kyc — does not
  redefine business rules alone. Use when /ha-ppdev, platform dev, scaffold
  monorepo, recreate PumaPay API/backend, or greenfield backend.
---

# ha-ppdev

Canonical agents: `~/.grok/agents/ppd-*.md`  
Contract: `references/CONTRACT.md` · Workflow: `~/.grok/workflows/ha-ppdev.rhai`

Parent = conductor (grok-4.6). Volume lanes may use grok-build. Children **cannot** spawn children.

## Mission

Recreate **PumaPay API + backend from zero** in a clean monorepo.  
Pentest/loot under `~/Desktop/puma/` is **not** the product codebase.

| Env | Default |
|---|---|
| `PPDEV_OUT` | `$HOME/dev/pumapay` (code monorepo) |
| Docs / org | `$HOME/Desktop/puma/docs/pumapay-v2/` |
| Bus | `~/.grok/pumapay-bus/` + `OUT/.bus/` |

## Lanes

| Agent | Owns |
|---|---|
| `ppd-arch` | ADRs, bounded contexts, monorepo layout → `platform/ARCHITECTURE.md` |
| `ppd-api` | OpenAPI + error envelope + versioning → `api/openapi.yaml` |
| `ppd-backend` | Services / handlers / domain wiring → `apps/api/` + `dev/CHANGES.md` |
| `ppd-db` | Schema + migrations (ledger/wallet/outbox) → `db/SCHEMA.md` |
| `ppd-auth` | Identity, JWT/sessions, scopes → `auth/AUTH.md` |
| `ppd-workers` | Jobs, webhook ingest, outbox → `workers/JOBS.md` |
| `ppd-test` | Contract + integration evidence → `test/TEST-REPORT.md` |
| `ppd-tooling` | docker-compose, Makefile, CI local → `tooling/DEVENV.md` |
| `ppd-sync` | Bus ↔ domain teams + ha-pumapay |
| `ppd-lead` | SUMMARY + BOARD + PR order; no invented GO |

## Hard rules

1. Domain teams (`ha-ledger`, `ha-payments`, …) own **business** contracts; this team **implements**.
2. No money-writes / destructive migrate without explicit operator flag.
3. Skip lane if `OUT/.bus/READY.<lane>` exists (idempotent).
4. Secrets redact in chat; full only in gated local env files.
5. Peers do not spawn peers. Parent workflow / TUI only.

## Dispatch

```bash
export PPDEV_OUT="${PPDEV_OUT:-$HOME/dev/pumapay}"
mkdir -p "$PPDEV_OUT"
bash ~/.grok/skills/ha-ppdev/scripts/ctl.sh auto --out "$PPDEV_OUT"
# then: workflow name=ha-ppdev
```

## Tick

```bash
bash ~/.grok/skills/ha-ppdev/scripts/ctl.sh tick --out "$PPDEV_OUT"
# workflow name=ha-ppdev-tick
```

Remainder lanes + always sync + lead.

## Collab

See `~/.grok/pumapay-bus/COLLAB.md` and `docs/pumapay-v2/TEAMS.md`.
