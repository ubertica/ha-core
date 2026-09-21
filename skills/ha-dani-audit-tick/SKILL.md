---
name: ha-dani-audit-tick
description: >
  Periodic tick for ha-dani-audit. Remainder lanes + sync + lead. Civil. No loot. No live writes.
---

# ha-dani-audit-tick

Tick conductor for the ha-dani-audit team.

```bash
bash ~/.grok/skills/ha-dani-audit/scripts/ctl.sh tick --out "$OUT"
# then workflow name=ha-dani-audit-tick
```

Skips lanes that have READY.* + on-disk artifact. Always runs sync/lead equivalents.
Civil scan must stay clean. See `~/.grok/skills/ha-dani-audit/references/AUTONOMY.md`.
