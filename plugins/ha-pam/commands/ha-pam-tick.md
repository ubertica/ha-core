---
name: ha-pam-tick
description: Periodic tick for ha-pam. Remainder + lead.
---

Run tick conductor. Remainder lanes only + lead.

`bash ~/.grok/skills/ha-pam/scripts/ctl.sh tick --out OUT`
then `workflow name=ha-pam-tick args.out=OUT`

See main command ha-pam.md .
