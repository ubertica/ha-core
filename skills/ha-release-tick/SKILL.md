---
name: ha-release-tick
description: >
  Periodic tick for ha-release. Remainder lanes + sync + lead. Use for maintenance.
---

# ha-release-tick

Tick conductor for the ha-release team.

```bash
bash ~/.grok/skills/ha-release/scripts/ctl.sh tick --out "$OUT"
# then workflow name=ha-release-tick
```

Skips lanes that have READY.* + on-disk artifact. Always runs sync/lead equivalents.
See `references/AUTONOMY.md` and main `SKILL.md`.
