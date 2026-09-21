---
name: ha-support-tick
description: Periodic tick for ha-support. Remainder + lead.
---

Run tick conductor. Remainder lanes only + lead.

`bash ~/.grok/skills/ha-support/scripts/ctl.sh tick --out OUT`
then `workflow name=ha-support-tick args.out=OUT`

See main command ha-support.md .
