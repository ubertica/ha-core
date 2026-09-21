---
name: ha-team-forge
description: >
  Factory for HA teams: scaffold plugins, agent rosters, skills, NORTHSTAR/CONTRACT/AUTONOMY,
  ctl/dispatch/verify, and workflows in the ha-hackers shape. Use when creating a new team,
  forging a plugin+agents pack, /ha-team-forge, or "como ha-hackers pero para X".
---

# ha-team-forge

Canonical references: `references/{NORTHSTAR,CONTRACT,AUTONOMY}.md`  
Gold: `~/.grok/plugins/ha-hackers/`  
Build checklist: `BUILD-SPEC.md`

## Quick use

```bash
bash ~/.grok/skills/ha-team-forge/scripts/ctl.sh forge \
  --name ha-foo --prefix foo --mode team --tick 1 \
  --purpose "one paragraph" \
  --lanes ~/.grok/skills/ha-team-forge/examples/lanes-minimal.json
```

Or workflow: `/ha-team-forge` / `workflow name=ha-team-forge` with args.

## Modes

`team` (default) · `plugin` · `agents` · `tick`

## Conductor rule

Parent writes/approves brief → forge scripts render templates → `selftest` → DONE.  
Volume file gen may use `grok-build` workers; design stays on grok-4.6.
