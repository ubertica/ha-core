---
name: ha-dani-authz-tick
description: >
  Periodic tick for ha-dani-authz. Remainder lanes + sync + lead. Civil. No loot. No live writes.
---

# ha-dani-authz-tick

Tick conductor for the ha-dani-authz team.

```bash
bash ~/.grok/skills/ha-dani-authz/scripts/ctl.sh tick --out "$OUT"
# then workflow name=ha-dani-authz-tick
```

Skips lanes that have READY.* + on-disk artifact. Always runs sync/lead equivalents.
Civil scan must stay clean. See `~/.grok/skills/ha-dani-authz/references/AUTONOMY.md`.
