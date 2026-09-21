---
name: ha-marketing-tick
description: >
  Periodic tick for ha-marketing. Remainder lanes + sync + lead. Use for maintenance.
---

# ha-marketing-tick

Tick conductor for the ha-marketing team.

```bash
bash ~/.grok/skills/ha-marketing/scripts/ctl.sh tick --out "$OUT"
# then workflow name=ha-marketing-tick
```

Skips lanes that have READY.* + on-disk artifact. Always runs sync/lead equivalents.
See `references/AUTONOMY.md` and main `SKILL.md`.
