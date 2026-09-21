---
name: ha-pumapay-tick
description: >
  Periodic tick conductor for ha-pumapay. Remainder lanes only + sync + lead.
  Use for ongoing product maintenance after initial /ha-pumapay.
---

# ha-pumapay-tick

Canonical same as ha-pumapay.

Runs dispatch remainder: skips READY lanes with on-disk artifacts.

Always: pp-sync (collab bus) then pp-lead (SUMMARY + BOARD).

See `~/.grok/skills/ha-pumapay/SKILL.md` and references/AUTONOMY.md for full dispatch.

Workflow: `ha-pumapay-tick.rhai`

CLI: `ctl.sh tick --out OUT`
