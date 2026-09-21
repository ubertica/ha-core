---
name: ha-pragmatic-tick
description: Periodic tick for ha-pragmatic. Remainder + lead.
---

Run tick conductor. Remainder lanes only + lead.

`bash ~/.grok/skills/ha-pragmatic/scripts/ctl.sh tick --out OUT`
then `workflow name=ha-pragmatic-tick args.out=OUT`

See main command ha-pragmatic.md .
