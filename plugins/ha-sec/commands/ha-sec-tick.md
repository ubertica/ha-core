---
name: ha-sec-tick
description: Periodic tick for ha-sec. Remainder + lead.
---

Run tick conductor. Remainder lanes only + lead.

`bash ~/.grok/skills/ha-sec/scripts/ctl.sh tick --out OUT`
then `workflow name=ha-sec-tick args.out=OUT`

See main command ha-sec.md .
