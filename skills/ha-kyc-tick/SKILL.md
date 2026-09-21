---
name: ha-kyc-tick
description: >
  Periodic tick for ha-kyc. Remainder lanes + sync + lead. Use for maintenance.
---

# ha-kyc-tick

Tick conductor for the ha-kyc team.

```bash
bash ~/.grok/skills/ha-kyc/scripts/ctl.sh tick --out "$OUT"
# then workflow name=ha-kyc-tick
```

Skips lanes that have READY.* + on-disk artifact. Always runs sync/lead equivalents.
See `references/AUTONOMY.md` and main `SKILL.md`.
