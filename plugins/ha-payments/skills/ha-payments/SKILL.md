---
name: ha-payments
description: >
  Dispatch the PumaPay payments team (pay-rails, pay-psp, pay-webhooks,
  pay-qa, pay-test, pay-dev, pay-sync, pay-lead). Cash-in/out rails mapped
  to CORE-SURFACE, sandbox PSP matrix, signed webhooks, idempotency keys.
  Use when /ha-payments, convert/transfer/withdraw, vouchers, payouts,
  payment-link, or PSP webhook ingest.
---

# ha-payments

Canonical agents: `$GROK_HOME/agents/pay-*.md` (mirror: `$PUMAPAY_ROOT/equipos/agents/`)  
Contract: `references/CONTRACT.md` · Autonomy: `references/AUTONOMY.md`  
Workflow: `ha-payments.rhai` / `ha-payments-tick.rhai`

Parent = grok-4.6. Children cannot spawn children.

## Mission

Own **how money enters and leaves** this instance: rails, PSP adapters, signed webhooks.  
Ledger owns journals. Risk owns allow/review/deny. ppdev implements HTTP + workers.

Every CORE-SURFACE money write has a rail, an idempotency key, a ledger hold/post, and a sandbox path. Live PSP is **off** until `PUMAPAY_LIVE_PSP=1`.

## Paths (portable)

| Env | Default |
|---|---|
| `HA_PAYMENTS_OUT` / `OUT` | `$PUMAPAY_OUT/payments` |
| `PUMAPAY_BUS` | `$GROK_HOME/pumapay-bus` |
| `GROK_HOME` | `$HOME/.grok` |

**Zero** `Desktop/puma`, operator home literals, `docs/pumapay-v2`.

## Lanes

| Agent | Owns | Artifact |
|---|---|---|
| `pay-rails` | State machines for all CORE-SURFACE writes | `RAILS.md` |
| `pay-psp` | Sandbox matrix, vault refs, no live default | `PSP.md` |
| `pay-webhooks` | Signature, replay window, DLQ | `WEBHOOKS.md` |
| `pay-qa` | Gates: no money-write without flag | `GATES.md` |
| `pay-test` | Sandbox e2e cases | `TEST-REPORT.md` |
| `pay-dev` | Impl notes for ppdev | `CHANGES.md` |
| `pay-sync` | Bus ledger/risk/support | `COLLAB-STATUS.md` |
| `pay-lead` | SUMMARY; no invented GO | `SUMMARY.md` |

## CORE-SURFACE map

| Op | Rail | Ledger |
|---|---|---|
| convert quote | `fx.convert` (no money) | none |
| convert execute | `fx.convert` | FX journal |
| transfer | `wallet.transfer` | user↔user post |
| send-to-parent | `agent.send_to_parent` | tree post |
| payment-link | `paylink.create` | hold on clearing inbound |
| auto/deposit | `psp.cashin` | hold→capture |
| withdraw | `psp.cashout` | hold→capture or release |
| voucher* | `agent.voucher` (W3) | hold→post |
| payouts confirm/reject/cancel | `agent.payout` (W4) | hold→post/release |

Staff confirm/reject: **DB groups**, not `x-user-role`.

## Hard rules

1. Idempotency on every money POST.
2. Signed webhooks; unsigned rejected.
3. Sandbox PSP default; live requires operator flag.
4. Rails call ledger; never write balance columns.
5. Skip READY+artifact lanes.
6. No Fastify in this pack.
7. No nested spawn. No invented GO.
8. Secrets out of artifacts.

## Dispatch

```bash
source "$PUMAPAY_ROOT/equipos/lib/paths.sh"
mkdir -p "$HA_PAYMENTS_OUT/.bus"
bash "$GROK_HOME/skills/ha-payments/scripts/ctl.sh" auto --out "$HA_PAYMENTS_OUT"
# workflow name=ha-payments
```

## Tick

```bash
bash "$GROK_HOME/skills/ha-payments/scripts/ctl.sh" tick --out "$HA_PAYMENTS_OUT"
# workflow name=ha-payments-tick
```

Remainder + always `pay-sync` + `pay-lead`.

## Selftest

```bash
bash "$PUMAPAY_ROOT/equipos/plugins/ha-payments/skills/ha-payments/scripts/ctl.sh" selftest
```

## Collab

`references/COLLAB.md`. Topics in CONTRACT.

## Operator flags

`PUMAPAY_LIVE_PSP` · `PUMAPAY_MONEY_WRITES` · `PUMAPAY_DESTRUCTIVE_MIGRATE`
