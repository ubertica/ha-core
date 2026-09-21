---
name: ha-release
description: >
  Dispatch the ha-release team. PumaPay release train go/no-go.
  Use when /ha-release, or parallel domain lanes for this pack.
---

# ha-release

Canonical agents: `~/.grok/agents/rel-*.md`  
Contract: `references/CONTRACT.md` · Workflow: `~/.grok/workflows/ha-release.rhai`

Parent = conductor. Children cannot spawn children.

## Mission

PumaPay release train go/no-go.

Implements / documents domain artifacts under `OUT` (default docs tree or team OUT env).  
Business owner for this domain; **`/ha-ppdev`** implements greenfield API/backend code in `~/dev/pumapay`.

## Dispatch

```bash
bash ~/.grok/skills/ha-release/scripts/ctl.sh auto --out "$OUT"
# workflow name=ha-release
```

## Tick

```bash
bash ~/.grok/skills/ha-release/scripts/ctl.sh tick --out "$OUT"
# workflow name=ha-release-tick
```

See `references/` for NORTHSTAR / CONTRACT / AUTONOMY.  
Roster: `~/Desktop/puma/docs/pumapay-v2/TEAMS.md`.
