---
name: ha-aml
description: >
  AML team for PumaPay v2 fintech: transaction monitoring, investigations, SAR/STR filing, customer risk rating, rule tuning and regulatory reporting. Full HA autonomy, bus collab with fraud/risk/support, selftest PASS. Same structure and quality as ha-hackers and ha-risk. Use when creating a new team, forging a plugin+agents pack, /ha-aml, or "como ha-hackers pero para ha-aml".
---

# ha-aml

Canonical references: `references/{NORTHSTAR,CONTRACT,AUTONOMY}.md`  
Gold: `~/.grok/plugins/ha-hackers/`  
Build checklist: `BUILD-SPEC.md`

## Quick use

```bash
bash ~/.grok/skills/ha-aml/scripts/ctl.sh forge \
  --name ha-aml --prefix aml --mode team --tick 1 \
  --purpose "AML team for PumaPay v2 fintech: transaction monitoring, investigations, SAR/STR filing, customer risk rating, rule tuning and regulatory reporting. Full HA autonomy, bus collab with fraud/risk/support, selftest PASS. Same structure and quality as ha-hackers and ha-risk." \
  --lanes ~/.grok/skills/ha-team-forge/examples/lanes-aml.json
```

Or workflow: `/ha-aml` / `workflow name=ha-team-forge` with args.

## Modes

`team` (default) · `plugin` · `agents` · `tick`

## Conductor rule

Parent writes/approves brief → forge scripts render templates → `selftest` → DONE.  
Volume file gen may use `grok-build` workers; design stays on grok-4.6.
