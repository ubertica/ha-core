---
name: ha-payments-tick
description: >
  Periodic tick for ha-payments. Remainder lanes + sync + lead. Use for maintenance.
---

# ha-payments-tick

Tick conductor for the ha-payments team.

```bash
bash ~/.grok/skills/ha-payments/scripts/ctl.sh tick --out "$OUT"
# then workflow name=ha-payments-tick
```

Skips lanes that have READY.* + on-disk artifact. Always runs sync/lead equivalents.
See `references/AUTONOMY.md` and main `SKILL.md`.
