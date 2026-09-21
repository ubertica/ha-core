---
name: ha-aml-tick
description: >
  Periodic tick for ha-aml. Remainder lanes + sync + lead. Use for maintenance.
---

# ha-aml-tick

Tick conductor for the ha-aml team.

```bash
bash ~/.grok/skills/ha-aml/scripts/ctl.sh tick --out "$OUT"
# then workflow name=ha-aml-tick
```

Skips lanes that have READY.* + on-disk artifact. Always runs sync/lead equivalents.
See `references/AUTONOMY.md` and main `SKILL.md`.
