---
name: ha-pam
description: >
  PAM (Privileged Access Management) team for PumaPay staff-os and platform: access reviews, JIT grants, credential rotation, breakglass, over-privilege detection and audit evidence. Same gold quality as ha-hackers and ha-sec: full agents (pam-audit etc), contracts, autonomy, bus integration with sec/sre/backoffice, selftest. Use when creating a new team, forging a plugin+agents pack, /ha-pam, or "como ha-hackers pero para ha-pam".
---

# ha-pam

Canonical references: `references/{NORTHSTAR,CONTRACT,AUTONOMY}.md`  
Gold: `~/.grok/plugins/ha-hackers/`  
Build checklist: `BUILD-SPEC.md`

## Quick use

```bash
bash ~/.grok/skills/ha-pam/scripts/ctl.sh forge \
  --name ha-pam --prefix pam --mode team --tick 1 \
  --purpose "PAM (Privileged Access Management) team for PumaPay staff-os and platform: access reviews, JIT grants, credential rotation, breakglass, over-privilege detection and audit evidence. Same gold quality as ha-hackers and ha-sec: full agents (pam-audit etc), contracts, autonomy, bus integration with sec/sre/backoffice, selftest." \
  --lanes ~/.grok/skills/ha-team-forge/examples/lanes-pam.json
```

Or workflow: `/ha-pam` / `workflow name=ha-team-forge` with args.

## Modes

`team` (default) · `plugin` · `agents` · `tick`

## Conductor rule

Parent writes/approves brief → forge scripts render templates → `selftest` → DONE.  
Volume file gen may use `grok-build` workers; design stays on grok-4.6.
