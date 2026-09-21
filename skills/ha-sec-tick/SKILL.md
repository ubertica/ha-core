---
name: ha-sec-tick
description: >
  Periodic tick for ha-sec. Remainder lanes + sync + lead. Use for maintenance.
---

# ha-sec-tick

Tick conductor for the ha-sec team.

```bash
bash ~/.grok/skills/ha-sec/scripts/ctl.sh tick --out "$OUT"
# then workflow name=ha-sec-tick
```

Skips lanes that have READY.* + on-disk artifact. Always runs sync/lead equivalents.
See `references/AUTONOMY.md` and main `SKILL.md`.
