---
name: ha-blackhat-tick
description: Periodic tick for ha-blackhat. Remainder + lead.
---

Run tick conductor. Remainder lanes only + lead.

`bash ~/.grok/skills/ha-blackhat/scripts/ctl.sh tick --out OUT`
then `workflow name=ha-blackhat-tick args.out=OUT`

See main command ha-blackhat.md .
