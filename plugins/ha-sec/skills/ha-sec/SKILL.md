---
name: ha-sec
description: >
  Dispatch the ha-sec team. PumaPay AppSec+SecOps. Distinct from AMS sentinel.
  Use when /ha-sec, or parallel domain lanes for this pack.
---

# ha-sec

Canonical agents: `~/.grok/agents/sec-*.md`  
Contract: `references/CONTRACT.md` · Workflow: `~/.grok/workflows/ha-sec.rhai`

Parent = conductor. Children cannot spawn children.

## Mission

PumaPay AppSec+SecOps. Distinct from AMS sentinel.

Implements / documents domain artifacts under `OUT` (default docs tree or team OUT env).  
Business owner for this domain; **`/ha-ppdev`** implements greenfield API/backend code in `~/dev/pumapay`.

## Dispatch

```bash
bash ~/.grok/skills/ha-sec/scripts/ctl.sh auto --out "$OUT"
# workflow name=ha-sec
```

## Tick

```bash
bash ~/.grok/skills/ha-sec/scripts/ctl.sh tick --out "$OUT"
# workflow name=ha-sec-tick
```

See `references/` for NORTHSTAR / CONTRACT / AUTONOMY.  
Roster: `~/Desktop/puma/docs/pumapay-v2/TEAMS.md`.
