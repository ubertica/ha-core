---
name: ha-release-tick
description: Periodic tick for ha-release. Remainder + lead.
---

Run tick conductor. Remainder lanes only + lead.

`bash ~/.grok/skills/ha-release/scripts/ctl.sh tick --out OUT`
then `workflow name=ha-release-tick args.out=OUT`

See main command ha-release.md .
