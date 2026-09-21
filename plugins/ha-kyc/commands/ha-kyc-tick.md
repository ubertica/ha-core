---
name: ha-kyc-tick
description: Periodic tick for ha-kyc. Remainder + lead.
---

Run tick conductor. Remainder lanes only + lead.

`bash ~/.grok/skills/ha-kyc/scripts/ctl.sh tick --out OUT`
then `workflow name=ha-kyc-tick args.out=OUT`

See main command ha-kyc.md .
