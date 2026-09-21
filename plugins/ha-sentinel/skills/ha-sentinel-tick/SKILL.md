---
name: ha-sentinel-tick
description: >
  Periodic tick conductor for ha-sentinel. Remainder lanes only + escalate/collab + lead.
  Use for ongoing AMS sentinel protection after initial /ha-sentinel.
---

# ha-sentinel-tick

Canonical same as ha-sentinel.

Runs dispatch remainder: skips READY lanes with on-disk artifacts.

Always: sent-escalate (if high/crit) + sent-collab + sent-lead (SUMMARY).

See `~/.grok/skills/ha-sentinel/SKILL.md` and references/AUTONOMY.md for full dispatch.

Workflow: `ha-sentinel-tick.rhai`

CLI: `ctl.sh tick --out OUT`
