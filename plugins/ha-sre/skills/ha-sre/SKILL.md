---
name: ha-sre
description: >
  Dispatch the ha-sre team. PumaPay SRE: SLOs, deploy, on-call. Complements ha-sentinel.
  Use when /ha-sre, or parallel domain lanes for this pack.
---

# ha-sre

Canonical agents: `~/.grok/agents/sre-*.md`  
Contract: `references/CONTRACT.md` · Workflow: `~/.grok/workflows/ha-sre.rhai`

Parent = conductor. Children cannot spawn children.

## Mission

PumaPay SRE: SLOs, deploy, on-call. Complements ha-sentinel.

Implements / documents domain artifacts under `OUT` (default docs tree or team OUT env).  
Business owner for this domain; **`/ha-ppdev`** implements greenfield API/backend code in `~/dev/pumapay`.

## Dispatch

```bash
bash ~/.grok/skills/ha-sre/scripts/ctl.sh auto --out "$OUT"
# workflow name=ha-sre
```

## Tick

```bash
bash ~/.grok/skills/ha-sre/scripts/ctl.sh tick --out "$OUT"
# workflow name=ha-sre-tick
```

See `references/` for NORTHSTAR / CONTRACT / AUTONOMY.  
Roster: `~/Desktop/puma/docs/pumapay-v2/TEAMS.md`.
