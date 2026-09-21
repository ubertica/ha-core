---
name: ha-support
description: >
  Dispatch the ha-support team. PumaPay support AI for SDPPAY.
  Use when /ha-support, or parallel domain lanes for this pack.
---

# ha-support

Canonical agents: `~/.grok/agents/sup-*.md`  
Contract: `references/CONTRACT.md` · Workflow: `~/.grok/workflows/ha-support.rhai`

Parent = conductor. Children cannot spawn children.

## Mission

PumaPay support AI for SDPPAY.

Implements / documents domain artifacts under `OUT` (default docs tree or team OUT env).  
Business owner for this domain; **`/ha-ppdev`** implements greenfield API/backend code in `~/dev/pumapay`.

## Dispatch

```bash
bash ~/.grok/skills/ha-support/scripts/ctl.sh auto --out "$OUT"
# workflow name=ha-support
```

## Tick

```bash
bash ~/.grok/skills/ha-support/scripts/ctl.sh tick --out "$OUT"
# workflow name=ha-support-tick
```

See `references/` for NORTHSTAR / CONTRACT / AUTONOMY.  
Roster: `~/Desktop/puma/docs/pumapay-v2/TEAMS.md`.
