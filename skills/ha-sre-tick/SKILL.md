---
name: ha-sre-tick
description: >
  Periodic tick for ha-sre. Remainder lanes + sync + lead. Use for maintenance.
---

# ha-sre-tick

Tick conductor for the ha-sre team.

```bash
bash ~/.grok/skills/ha-sre/scripts/ctl.sh tick --out "$OUT"
# then workflow name=ha-sre-tick
```

Skips lanes that have READY.* + on-disk artifact. Always runs sync/lead equivalents.
See `references/AUTONOMY.md` and main `SKILL.md`.
