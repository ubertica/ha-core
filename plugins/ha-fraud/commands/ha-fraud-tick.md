---
name: ha-fraud-tick
description: Periodic tick for ha-fraud. Remainder + lead.
---

Run tick conductor. Remainder lanes only + lead.

`bash ~/.grok/skills/ha-fraud/scripts/ctl.sh tick --out OUT`
then `workflow name=ha-fraud-tick args.out=OUT`

See main command ha-fraud.md .
