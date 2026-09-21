---
name: ha-aml-tick
description: Periodic tick for ha-aml. Remainder + lead.
---

Run tick conductor. Remainder lanes only + lead.

`bash ~/.grok/skills/ha-aml/scripts/ctl.sh tick --out OUT`
then `workflow name=ha-aml-tick args.out=OUT`

See main command ha-aml.md .
