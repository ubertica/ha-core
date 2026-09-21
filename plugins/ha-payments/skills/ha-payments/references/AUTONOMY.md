# AUTONOMY — ha-payments (runtime)

Running domain team. **Not** a factory. Do **not** copy forge spec/scaffold phases.

## Default: autonomous dispatch

Operator says `/ha-payments` or “cerrá rails W2–W4” → parent:

1. OUT = `$HA_PAYMENTS_OUT` default `$PUMAPAY_OUT/payments`
2. Preflight: `paths.sh`; mkdir `.bus`; bus `teams/` exists
3. `ctl.sh auto --out "$OUT"`
4. Workflow `ha-payments`
5. Skip READY+artifact lanes
6. Always `pay-sync` + `pay-lead`
7. `ctl.sh verify`
8. Live PSP mentioned without `PUMAPAY_LIVE_PSP=1` → HOLD in SUMMARY

## ctl.sh

```bash
source "$PUMAPAY_ROOT/equipos/lib/paths.sh"
bash "$GROK_HOME/skills/ha-payments/scripts/ctl.sh" auto --out "$HA_PAYMENTS_OUT"
bash "$GROK_HOME/skills/ha-payments/scripts/ctl.sh" tick --out "$HA_PAYMENTS_OUT"
bash "$GROK_HOME/skills/ha-payments/scripts/ctl.sh" selftest
bash "$GROK_HOME/skills/ha-payments/scripts/ctl.sh" verify --out "$HA_PAYMENTS_OUT"
```

Repo (no GROK_HOME):

```bash
bash "$PUMAPAY_ROOT/equipos/plugins/ha-payments/skills/ha-payments/scripts/ctl.sh" selftest
```

No factory rebuild of this pack.

## Tick

Remainder + **always** sync + lead. Idempotent READY. Refresh SUMMARY from disk.

## Lane order

```
rails ∥ psp ∥ webhooks
  └─ qa ∥ test ∥ dev
       └─ sync → lead
```

`qa` must read rails+psp+webhooks. `test` after rails.

## Selftest

Scripts + `pay-*` agents + workflows `ha-payments.rhai` + `ha-payments-tick.rhai` (repo or GROK_HOME) + SKILL/NORTHSTAR/CONTRACT/AUTONOMY. No LLM spawn.

## Never

- Nested `grok -p`
- Spawn ledger/risk/ppdev from a lane
- Live money without operator flag
- Hardcode operator home or dead docs trees as OUT
- Invented GO
