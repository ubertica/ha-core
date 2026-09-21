# CONTRACT — ha-payments

Domain team owns **rails / PSP / webhook** contracts. `ha-ppdev` implements. No Fastify handlers in this pack (notes in `IMPL.md` / `CHANGES.md`).

## Inputs

| Input | Path / env |
|---|---|
| OUT | `--out` or `$HA_PAYMENTS_OUT` (default `$PUMAPAY_OUT/payments`) |
| Product SoT | `$PUMAPAY_ROOT/docs/api/CORE-SURFACE.md` |
| Waves | `$PUMAPAY_ROOT/docs/plans/DEV-PLAN.md` |
| Authz | `$PUMAPAY_ROOT/docs/api/AUTH-MODEL.md` |
| Ledger peer | `$PUMAPAY_OUT/ledger/{MODEL,POSTING}.md` |
| Lanes | `$PUMAPAY_ROOT/equipos/lanes/lanes-payments.json` |
| Bus | `$PUMAPAY_BUS` |

## Outputs (under `$PUMAPAY_OUT/payments`)

| Lane | Agent | Artifact | READY |
|---|---|---|---|
| rails | `pay-rails` | `RAILS.md` | `.bus/READY.rails` |
| psp | `pay-psp` | `PSP.md` | `.bus/READY.psp` |
| webhooks | `pay-webhooks` | `WEBHOOKS.md` | `.bus/READY.webhooks` |
| qa | `pay-qa` | `GATES.md` | `.bus/READY.qa` |
| test | `pay-test` | `TEST-REPORT.md` | `.bus/READY.test` |
| dev | `pay-dev` | `CHANGES.md` (+ `IMPL.md`) | `.bus/READY.dev` |
| sync | `pay-sync` | `COLLAB-STATUS.md` | `.bus/READY.sync` |
| lead | `pay-lead` | `SUMMARY.md` | `.bus/READY.lead` |

READY without artifact = HOLD.

## Models

grok-4.6: `pay-rails` `pay-psp` `pay-webhooks` `pay-qa` `pay-sync` `pay-lead`  
grok-build: `pay-test` `pay-dev`  
Matrix: `$PUMAPAY_ROOT/org/AGENT-MODELS.md`.

## HA profile

**FINTECH-BUILD**. No infection/drainer framing.

## Operator flags

| Flag | Meaning |
|---|---|
| `PUMAPAY_LIVE_PSP=1` | Real acquirer/PSP; live money |
| `PUMAPAY_MONEY_WRITES=1` | Persist journals to non-lab DB |
| `PUMAPAY_DESTRUCTIVE_MIGRATE=1` | Drop payment tables |
| unset | **Sandbox / docs only** |

Agents must cite the flag. Live credentials: env/secret store, never artifacts.

## Fail-closed

1. Rail without ledger hold/post mapping → HOLD.
2. Webhook without signature + idempotency → HOLD.
3. PSP.md listing live MIDs as default → HOLD.
4. Authz via `x-user-role` → HOLD.
5. No invented GO (“webhooks work” without TEST-REPORT cases).

## Idempotency

Header `Idempotency-Key` (fallback JSON `idempotency_key`). Scope: `(userid, route, key)` unique. Stored with payment intent id. Same key different body → 409.

## Webhook ingest (contract)

- Verify signature before parse-side effects
- Timestamp skew window (e.g. 5 min)
- Persist `psp_event_id` unique
- Map to intent → `captureHold` / `releaseHold` via ledger
- Retry: exponential; DLQ after N; workers own DLQ (`ppd-workers`)

## Bus

- `$HA_PAYMENTS_OUT/.bus/`
- `$PUMAPAY_BUS/teams/ha-payments.jsonl`
- `$PUMAPAY_BUS/domain-events.jsonl`  
  Topics: `payments.intent.created`, `payments.intent.captured`, `payments.intent.failed`, `payments.webhook.received`, `payments.webhook.rejected`

## Paths law

`$GROK_HOME` `$PUMAPAY_ROOT` `$PUMAPAY_OUT` `$PUMAPAY_BUS` `$HA_PAYMENTS_OUT`.  
Zero `Desktop/puma`, operator home literals, `docs/pumapay-v2`.
