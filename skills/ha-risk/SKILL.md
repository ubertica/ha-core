---
name: ha-risk
description: >
  Dispatch the ha-risk team. PumaPay risk/fraud/AML rules, cases, scoring.
  Use when /ha-risk, or parallel domain lanes for this pack.
---

# ha-risk

Canonical agents: `~/.grok/agents/rsk-*.md`  
Contract: `references/CONTRACT.md` · Workflow: `~/.grok/workflows/ha-risk.rhai`

Parent = conductor. Children cannot spawn children.

## Mission

PumaPay risk/fraud/AML rules, cases, scoring.

Implements / documents domain artifacts under `OUT` (default docs tree or team OUT env).  
Business owner for this domain; **`/ha-ppdev`** implements greenfield API/backend code in `~/dev/pumapay`.

## Dispatch

```bash
bash ~/.grok/skills/ha-risk/scripts/ctl.sh auto --out "$OUT"
# workflow name=ha-risk
```

## Tick

```bash
bash ~/.grok/skills/ha-risk/scripts/ctl.sh tick --out "$OUT"
# workflow name=ha-risk-tick
```

See `references/` for NORTHSTAR / CONTRACT / AUTONOMY.  
Roster: `~/Desktop/puma/docs/pumapay-v2/TEAMS.md`.
