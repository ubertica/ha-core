---
name: ha-ledger-tick
description: Periodic tick for ha-ledger. Remainder + lead.
---

Run tick conductor. Remainder lanes only + lead.

`bash ~/.grok/skills/ha-ledger/scripts/ctl.sh tick --out OUT`
then `workflow name=ha-ledger-tick args.out=OUT`

See main command ha-ledger.md .
