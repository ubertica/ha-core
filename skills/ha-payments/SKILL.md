---
name: ha-payments
description: >
  Dispatch the ha-payments team. PumaPay payments rails: cashin/cashout, PSP, signed webhooks.
  Use when /ha-payments, or parallel domain lanes for this pack.
---

# ha-payments

Canonical agents: `~/.grok/agents/pay-*.md`  
Contract: `references/CONTRACT.md` · Workflow: `~/.grok/workflows/ha-payments.rhai`

Parent = conductor. Children cannot spawn children.

## Mission

PumaPay payments rails: cashin/cashout, PSP, signed webhooks.

Implements / documents domain artifacts under `OUT` (default docs tree or team OUT env).  
Business owner for this domain; **`/ha-ppdev`** implements greenfield API/backend code in `~/dev/pumapay`.

## Dispatch

```bash
bash ~/.grok/skills/ha-payments/scripts/ctl.sh auto --out "$OUT"
# workflow name=ha-payments
```

## Tick

```bash
bash ~/.grok/skills/ha-payments/scripts/ctl.sh tick --out "$OUT"
# workflow name=ha-payments-tick
```

See `references/` for NORTHSTAR / CONTRACT / AUTONOMY.  
Roster: `~/Desktop/puma/docs/pumapay-v2/TEAMS.md`.
