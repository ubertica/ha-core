---
name: ha-sentinel-tick
description: Periodic sentinel tick. Remainder + escalate∥collab + lead. Idempotent.
---

Periodic protection tick for AMS sentinel-god + ollama-ha.

`bash ~/.grok/skills/ha-sentinel/scripts/ctl.sh tick --out OUT`
workflow name=ha-sentinel-tick args.out=OUT

Pulls latest evidence via ams-mirror, runs remainder lanes, escalates high/crit to pumapay-bus, updates collab + SUMMARY.
