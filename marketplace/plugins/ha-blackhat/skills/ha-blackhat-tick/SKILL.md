---
name: ha-blackhat-tick
description: >
  Periodic tick for ha-blackhat. Remainder lanes + sync + lead. Use for maintenance.
---

# ha-blackhat-tick

Tick conductor for the ha-blackhat team.

```bash
bash ~/.grok/skills/ha-blackhat/scripts/ctl.sh tick --out "$OUT"
# then workflow name=ha-blackhat-tick
```

Skips lanes that have READY.* + on-disk artifact. Always runs sync/lead equivalents.
See `references/AUTONOMY.md` and main `SKILL.md`.
