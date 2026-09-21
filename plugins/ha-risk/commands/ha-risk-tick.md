---
name: ha-risk-tick
description: Periodic tick for ha-risk. Remainder + lead.
---

Run tick conductor. Remainder lanes only + lead.

`bash ~/.grok/skills/ha-risk/scripts/ctl.sh tick --out OUT`
then `workflow name=ha-risk-tick args.out=OUT`

See main command ha-risk.md .
