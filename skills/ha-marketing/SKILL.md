---
name: ha-marketing
description: >
  Marketing team for PumaPay v2: full growth stack — acquisition campaigns, content & messaging, SEO/SEM/affiliates, analytics & attribution, creative production, brand safety and offer compliance. HA quality matching ha-hackers: agent roster, workflows, bus collab with product/support/risk, selftest PASS, NORTHSTAR ownership of growth KPIs. Use when creating a new team, forging a plugin+agents pack, /ha-marketing, or "como ha-hackers pero para ha-marketing".
---

# ha-marketing

Canonical references: `references/{NORTHSTAR,CONTRACT,AUTONOMY}.md`  
Gold: `~/.grok/plugins/ha-hackers/`  
Build checklist: `BUILD-SPEC.md`

## Quick use

```bash
bash ~/.grok/skills/ha-marketing/scripts/ctl.sh forge \
  --name ha-marketing --prefix mkt --mode team --tick 1 \
  --purpose "Marketing team for PumaPay v2: full growth stack — acquisition campaigns, content & messaging, SEO/SEM/affiliates, analytics & attribution, creative production, brand safety and offer compliance. HA quality matching ha-hackers: agent roster, workflows, bus collab with product/support/risk, selftest PASS, NORTHSTAR ownership of growth KPIs." \
  --lanes ~/.grok/skills/ha-team-forge/examples/lanes-marketing.json
```

Or workflow: `/ha-marketing` / `workflow name=ha-team-forge` with args.

## Modes

`team` (default) · `plugin` · `agents` · `tick`

## Conductor rule

Parent writes/approves brief → forge scripts render templates → `selftest` → DONE.  
Volume file gen may use `grok-build` workers; design stays on grok-4.6.
