---
name: ha-pumapay-tick
description: Periodic tick for PumaPay v2 (remainder lanes + sync + lead only).
---

For ongoing product maintenance.

```
bash ~/.grok/skills/ha-pumapay/scripts/ctl.sh tick --out OUT
workflow name=ha-pumapay-tick args.out=OUT
```

Uses dispatch remainder. Skips existing READY. Always executes pp-sync then pp-lead.
