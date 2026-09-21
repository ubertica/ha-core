---
name: ha-dani-handoff-tick
description: >
  Periodic tick for ha-dani-handoff. Remainder lanes + sync + lead. Civil. No loot. No live writes.
---

# ha-dani-handoff-tick

Tick conductor for the ha-dani-handoff team.

```bash
bash ~/.grok/skills/ha-dani-handoff/scripts/ctl.sh tick --out "$OUT"
# then workflow name=ha-dani-handoff-tick
```

Skips lanes that have READY.* + on-disk artifact. Always runs sync/lead equivalents.
Civil scan must stay clean. See `~/.grok/skills/ha-dani-handoff/references/AUTONOMY.md`.
