---
name: ha-ledger-tick
description: >
  Periodic tick for ha-ledger. Remainder lanes + sync + lead. Use for maintenance.
---

# ha-ledger-tick

Tick conductor for the ha-ledger team.

```bash
bash ~/.grok/skills/ha-ledger/scripts/ctl.sh tick --out "$OUT"
# then workflow name=ha-ledger-tick
```

Skips lanes that have READY.* + on-disk artifact. Always runs sync/lead equivalents.
See `references/AUTONOMY.md` and main `SKILL.md`.
