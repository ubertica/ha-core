---
name: ha-fraud-tick
description: >
  Periodic tick for ha-fraud. Remainder lanes + sync + lead. Use for maintenance.
---

# ha-fraud-tick

Tick conductor for the ha-fraud team.

```bash
bash ~/.grok/skills/ha-fraud/scripts/ctl.sh tick --out "$OUT"
# then workflow name=ha-fraud-tick
```

Skips lanes that have READY.* + on-disk artifact. Always runs sync/lead equivalents.
See `references/AUTONOMY.md` and main `SKILL.md`.
