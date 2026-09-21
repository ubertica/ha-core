---
name: ha-kyc
description: >
  Dispatch the ha-kyc team. PumaPay KYC/onboarding; AI recommend human decide.
  Use when /ha-kyc, or parallel domain lanes for this pack.
---

# ha-kyc

Canonical agents: `~/.grok/agents/kyc-*.md`  
Contract: `references/CONTRACT.md` · Workflow: `~/.grok/workflows/ha-kyc.rhai`

Parent = conductor. Children cannot spawn children.

## Mission

PumaPay KYC/onboarding; AI recommend human decide.

Implements / documents domain artifacts under `OUT` (default docs tree or team OUT env).  
Business owner for this domain; **`/ha-ppdev`** implements greenfield API/backend code in `~/dev/pumapay`.

## Dispatch

```bash
bash ~/.grok/skills/ha-kyc/scripts/ctl.sh auto --out "$OUT"
# workflow name=ha-kyc
```

## Tick

```bash
bash ~/.grok/skills/ha-kyc/scripts/ctl.sh tick --out "$OUT"
# workflow name=ha-kyc-tick
```

See `references/` for NORTHSTAR / CONTRACT / AUTONOMY.  
Roster: `~/Desktop/puma/docs/pumapay-v2/TEAMS.md`.
