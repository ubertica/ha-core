---
name: ha-risk-tick
description: >
  Periodic tick for ha-risk. Remainder lanes + sync + lead. Use for maintenance.
---

# ha-risk-tick

Tick conductor for the ha-risk team.

```bash
bash ~/.grok/skills/ha-risk/scripts/ctl.sh tick --out "$OUT"
# then workflow name=ha-risk-tick
```

Skips lanes that have READY.* + on-disk artifact. Always runs sync/lead equivalents.
See `references/AUTONOMY.md` and main `SKILL.md`.
