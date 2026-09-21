---
name: ha-ppdev-tick
description: >
  Periodic tick for ha-ppdev. Remainder lanes only + sync + lead.
  Use for ongoing monorepo maintenance after initial /ha-ppdev.
---

# ha-ppdev-tick

Runs `ha-ppdev-tick` workflow: skip READY lanes, always `ppd-sync` + `ppd-lead`.

```bash
export PPDEV_OUT="${PPDEV_OUT:-$HOME/dev/pumapay}"
bash ~/.grok/skills/ha-ppdev/scripts/ctl.sh tick --out "$PPDEV_OUT"
# workflow name=ha-ppdev-tick
```

See `/ha-ppdev` for full mission and contract.
