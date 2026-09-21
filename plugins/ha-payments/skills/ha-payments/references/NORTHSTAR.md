# NORTHSTAR — ha-payments

**Team:** `ha-payments` (`pay-*`)  
**Owns:** cash-in / cash-out **rails**, PSP adapter contract, signed webhooks, idempotency for this instance.  
**Does not own:** journal math (ha-ledger), Fastify handlers (ha-ppdev), fraud decisioning (ha-risk).

## DONE (predicate)

Wave 2–4 **payment rails contract** is on disk at `$PUMAPAY_OUT/payments/` and maps **every** CORE-SURFACE money write to a state machine + ledger hold/post + idempotency key:

| Must exist | Meaning |
|---|---|
| `RAILS.md` | State machines for convert, transfer, send-to-parent, payment-link, auto-deposit, withdraw, vouchers, payouts |
| `PSP.md` | Sandbox PSP matrix; vault refs; **no live money** without operator flag |
| `WEBHOOKS.md` | Signed ingest, replay window, idempotency, retry/DLQ |
| `SUMMARY.md` | Honest GO/HOLD |

**DONE ≠** “PSP.md exists”. **DONE =** each SPA write has a rail, a ledger effect, an idempotency story, and a sandbox path.

## Product SoT

- `docs/api/CORE-SURFACE.md` — wallet writes + agents deposits/payouts
- `docs/plans/DEV-PLAN.md` — W2 in-wallet; W3 cash-in vouchers; W4 cash-out
- `docs/api/AUTH-MODEL.md` — JWT `userid`; staff confirm/reject from **DB groups**
- Ledger contracts: `$PUMAPAY_OUT/ledger/{MODEL,POSTING}.md` (peer)

## CORE-SURFACE writes (must appear in RAILS.md)

| SPA path | Wave | Rail |
|---|---|---|
| `POST /wallet/convert/quote` · `execute` | W2 | `fx.convert` |
| `POST /wallet/transfer` | W2 | `wallet.transfer` |
| `POST /wallet/send-to-parent` | W2 | `agent.send_to_parent` |
| `POST /wallet/payment-link` | W2 | `paylink.create` |
| `POST /wallet/payment/auto/deposit` | W2 | `psp.cashin` |
| `POST /wallet/payment/{id}/withdraw` | W2 | `psp.cashout` |
| `GET /wallet/payment-methods?currency=` | W2 | catalog (no money) |
| `GET /wallet/payment-link/enabled` | W2 | flag |
| `GET /wallet/transfer/search-recipient` | W2 | lookup JWT-scoped |
| Deposits vouchers list/create/bulk/extract/edit/cancel | W3 | `agent.voucher` |
| Payouts list/create/confirm/reject/cancel | W4 | `agent.payout` |
| `GET /agents/supreme-parent` | W4 | routing, not money |

## Invariants

1. **Idempotency-Key** (or body `idempotency_key`) on every money POST. Replay = original resource.
2. **Ledger is SoT.** Rails call hold/post/release; they do not UPDATE a balance column.
3. **Signed webhooks.** HMAC (or PSP-native signature) + timestamp window + event-id idempotency. Unsigned = reject.
4. **Sandbox default.** PSP matrix is mock/test. `PUMAPAY_LIVE_PSP=1` required for live money. Unset → HOLD on live capture.
5. **Authz:** resource owner = JWT `userid`. Payout confirm/reject/cancel staff = DB groups. Never `x-user-role` header.
6. **Risk gate:** before capture, consult risk contract (allow/review/deny). Deny ≠ silent drop; return typed error.
7. **No casino PAM rails.** This instance is wallet + agent cash.

## Peers

| Peer | Contract |
|---|---|
| `ha-ledger` | hold/post/release; outbox |
| `ha-ppdev` | HTTP + workers + webhook ingest |
| `ha-risk` | pre-capture decision |
| `ha-kyc` | tier limits on cash-in/out |
| `ha-support` | customer-visible payment states |

## Non-goals

- Live PSP credentials in git
- Implementing Fastify routes here
- 283 `/integrations/*`
- Invented GO on “connected to Stripe live”

## OUT

`$HA_PAYMENTS_OUT` = `$PUMAPAY_OUT/payments`. Portable `$GROK_HOME` `$PUMAPAY_*`.  
**Zero** `Desktop/puma`, operator home literals, `docs/pumapay-v2`.

## Conductor

Parent grok-4.6. `pay-test` / `pay-dev` → grok-build. No nested spawn.
