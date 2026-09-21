---
name: ha-pragmatic-tick
description: >
  Periodic tick for ha-pragmatic. Remainder lanes + sync + lead. Use for maintenance.
---

# ha-pragmatic-tick

Tick conductor for the ha-pragmatic team.

```bash
bash ~/.grok/skills/ha-pragmatic/scripts/ctl.sh tick --out "$OUT"
# then workflow name=ha-pragmatic-tick
```

Skips lanes that have READY.* + on-disk artifact. Always runs sync/lead equivalents.
See `references/AUTONOMY.md` and main `SKILL.md`.
