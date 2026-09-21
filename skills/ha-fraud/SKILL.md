---
name: ha-fraud
description: >
  Fraud Prevention team for PumaPay: velocity/device/behavioral detection, fraud rules, case management, scoring integration, chargeback defense and loss prevention. Matches ha-hackers operating model, NORTHSTAR/CONTRACT/AUTONOMY, full agent roster, bus sync to AML/ledger/payments. Selftest required. Use when creating a new team, forging a plugin+agents pack, /ha-fraud, or "como ha-hackers pero para ha-fraud".
---

# ha-fraud

Canonical references: `references/{NORTHSTAR,CONTRACT,AUTONOMY}.md`  
Gold: `~/.grok/plugins/ha-hackers/`  
Build checklist: `BUILD-SPEC.md`

## Quick use

```bash
bash ~/.grok/skills/ha-fraud/scripts/ctl.sh forge \
  --name ha-fraud --prefix fraud --mode team --tick 1 \
  --purpose "Fraud Prevention team for PumaPay: velocity/device/behavioral detection, fraud rules, case management, scoring integration, chargeback defense and loss prevention. Matches ha-hackers operating model, NORTHSTAR/CONTRACT/AUTONOMY, full agent roster, bus sync to AML/ledger/payments. Selftest required." \
  --lanes ~/.grok/skills/ha-team-forge/examples/lanes-fraud.json
```

Or workflow: `/ha-fraud` / `workflow name=ha-team-forge` with args.

## Modes

`team` (default) · `plugin` · `agents` · `tick`

## Conductor rule

Parent writes/approves brief → forge scripts render templates → `selftest` → DONE.  
Volume file gen may use `grok-build` workers; design stays on grok-4.6.
