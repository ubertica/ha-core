name: ha-pp-consensus
description: Docs↔dev ACK×2 gate. ctl propose/auto/verify. Tick never votes. Structure r1 closed.
---

Protocol: `$PUMAPAY_ROOT/bus/consensus/CONSENSUS.md`

```bash
# operator-asked vote only — not part of pack complete
bash "$GROK_HOME/skills/ha-pp-consensus/scripts/ctl.sh" propose --id ID --title "..." --paths "docs/api/CORE-SURFACE.md"
bash "$GROK_HOME/skills/ha-pp-consensus/scripts/ctl.sh" auto --id ID
# workflow name=ha-pp-consensus
bash "$GROK_HOME/skills/ha-pp-consensus/scripts/ctl.sh" verify --id ID
bash "$GROK_HOME/skills/ha-pp-consensus/scripts/ctl.sh" tick
```
