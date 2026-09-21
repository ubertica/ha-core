---
name: ha-dani-ops-tick
description: >
  Periodic tick for ha-dani-ops. Remainder lanes + sync + lead. Civil. No loot. No live writes.
---

# ha-dani-ops-tick

Tick conductor for the ha-dani-ops team.

```bash
bash ~/.grok/skills/ha-dani-ops/scripts/ctl.sh tick --out "$OUT"
# then workflow name=ha-dani-ops-tick
```

Skips lanes that have READY.* + on-disk artifact. Always runs sync/lead equivalents.
Civil scan must stay clean. See `~/.grok/skills/ha-dani-ops/references/AUTONOMY.md`.
