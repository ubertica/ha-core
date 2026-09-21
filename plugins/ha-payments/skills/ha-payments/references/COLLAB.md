# COLLAB — ha-payments

## Paths

| Bus | Path |
|---|---|
| Per-run | `$HA_PAYMENTS_OUT/.bus/` |
| Team | `$PUMAPAY_BUS/teams/ha-payments.jsonl` |
| Domain | `$PUMAPAY_BUS/domain-events.jsonl` |

## Peers (do not spawn)

| To | When |
|---|---|
| `ha-ledger` | every money state change (hold/post) |
| `ha-risk` | before capture; velocity features |
| `ha-kyc` | tier/limit block |
| `ha-ppdev` | workers / webhook ingest impl |
| `ha-support` | failed cash-in/out customer-visible |

## Shape

```json
{"ts":"ISO8601","from":"pay-sync","to":"ha-ledger","type":"domain","severity":"info","path":"$PUMAPAY_OUT/payments/RAILS.md","msg":"voucher hold mapping W3","ids":{"rail":"agent.voucher"}}
```

Append-only. No `/ha-pp-consensus` this round (pack complete ≠ CORE-SURFACE change).
