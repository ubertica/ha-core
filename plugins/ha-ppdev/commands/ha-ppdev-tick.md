---
name: ha-ppdev-tick
description: Periodic tick for ha-ppdev. Remainder + lead.
---

Run tick conductor. Remainder lanes only + lead.

`bash ~/.grok/skills/ha-ppdev/scripts/ctl.sh tick --out OUT`
then `workflow name=ha-ppdev-tick args.out=OUT`

See main command ha-ppdev.md .
