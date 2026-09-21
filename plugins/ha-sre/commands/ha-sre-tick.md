---
name: ha-sre-tick
description: Periodic tick for ha-sre. Remainder + lead.
---

Run tick conductor. Remainder lanes only + lead.

`bash ~/.grok/skills/ha-sre/scripts/ctl.sh tick --out OUT`
then `workflow name=ha-sre-tick args.out=OUT`

See main command ha-sre.md .
