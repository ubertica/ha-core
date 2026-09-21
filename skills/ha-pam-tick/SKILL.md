---
name: ha-pam-tick
description: >
  Periodic tick for ha-pam. Remainder lanes + sync + lead. Use for maintenance.
---

# ha-pam-tick

Tick conductor for the ha-pam team.

```bash
bash ~/.grok/skills/ha-pam/scripts/ctl.sh tick --out "$OUT"
# then workflow name=ha-pam-tick
```

Skips lanes that have READY.* + on-disk artifact. Always runs sync/lead equivalents.
See `references/AUTONOMY.md` and main `SKILL.md`.
