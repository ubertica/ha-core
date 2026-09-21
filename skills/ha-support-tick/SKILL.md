---
name: ha-support-tick
description: >
  Periodic tick for ha-support. Remainder lanes + sync + lead. Use for maintenance.
---

# ha-support-tick

Tick conductor for the ha-support team.

```bash
bash ~/.grok/skills/ha-support/scripts/ctl.sh tick --out "$OUT"
# then workflow name=ha-support-tick
```

Skips lanes that have READY.* + on-disk artifact. Always runs sync/lead equivalents.
See `references/AUTONOMY.md` and main `SKILL.md`.
