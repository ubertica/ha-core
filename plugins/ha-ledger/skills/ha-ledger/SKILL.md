---
name: ha-ledger
description: >
  Dispatch the ha-ledger team. PumaPay ledger: double-entry, holds, recon, settlement.
  Use when /ha-ledger, or parallel domain lanes for this pack.
---

# ha-ledger

Canonical agents: `~/.grok/agents/led-*.md`  
Contract: `references/CONTRACT.md` · Workflow: `~/.grok/workflows/ha-ledger.rhai`

Parent = conductor. Children cannot spawn children.

## Mission

PumaPay ledger: double-entry, holds, recon, settlement.

Implements / documents domain artifacts under `OUT` (default docs tree or team OUT env).  
Business owner for this domain; **`/ha-ppdev`** implements greenfield API/backend code in `~/dev/pumapay`.

## Dispatch

```bash
bash ~/.grok/skills/ha-ledger/scripts/ctl.sh auto --out "$OUT"
# workflow name=ha-ledger
```

## Tick

```bash
bash ~/.grok/skills/ha-ledger/scripts/ctl.sh tick --out "$OUT"
# workflow name=ha-ledger-tick
```

See `references/` for NORTHSTAR / CONTRACT / AUTONOMY.  
Roster: `~/Desktop/puma/docs/pumapay-v2/TEAMS.md`.
