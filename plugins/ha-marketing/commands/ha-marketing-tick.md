---
name: ha-marketing-tick
description: Periodic tick for ha-marketing. Remainder + lead.
---

Run tick conductor. Remainder lanes only + lead.

`bash ~/.grok/skills/ha-marketing/scripts/ctl.sh tick --out OUT`
then `workflow name=ha-marketing-tick args.out=OUT`

See main command ha-marketing.md .
