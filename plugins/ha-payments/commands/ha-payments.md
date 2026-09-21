---
name: ha-payments
description: PumaPay payments: CORE-SURFACE rails, sandbox PSP, signed webhooks. Runs full lanes via workflow or tick.
---

Run the conductor. Do not spawn lanes by hand. Do not nested grok -p. Not forge.

1. OUT absolute (default `$HA_PAYMENTS_OUT` = `$PUMAPAY_OUT/payments`)
2. `bash $GROK_HOME/skills/ha-payments/scripts/ctl.sh auto --out OUT`
3. Launch `workflow name=ha-payments args.out=OUT`
4. Optional: `ctl.sh watch --out OUT`
5. Tick: `ctl.sh tick --out OUT` then `ha-payments-tick` workflow.

Always runs lead + sync on tick. Skips READY lanes with on-disk artifacts.
Money/PSP/KYC/migrate flags required for live/destructive work.
