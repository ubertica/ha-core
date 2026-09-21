---
name: ha-payments-tick
description: Periodic tick for ha-payments. Remainder + always sync + lead. Not forge.
---

`bash $GROK_HOME/skills/ha-payments/scripts/ctl.sh tick --out $HA_PAYMENTS_OUT`
then `workflow name=ha-payments-tick args.out=OUT`

Idempotent READY.<lane>. Do not enable live PSP / live KYC / risk enforce from tick.
