---
name: ha-dani-handoff
description: >
  Handoff-debt map after 10+ developers: owners, orphans, unified-bucket, Staff OS notes. Human-readable. No secrets.
  Use when /ha-dani-handoff, Daniel, Puma client handoff, post-incidente civil work.
---

# ha-dani-handoff

Canonical agents: `~/.grok/agents/dhan-*.md`
Contract: `references/CONTRACT.md` · Workflow: `~/.grok/workflows/ha-dani-handoff.rhai`
Civil law: `~/.grok/agents/_ha-dani-law.md`
OUT default: `/Users/c/dev/dani/out/handoff`

Parent = conductor. Children cannot spawn children.

## Mission

Handoff-debt map after 10+ developers: owners, orphans, unified-bucket, Staff OS notes. Human-readable. No secrets.

This is **not** ha-hackers. HARD ALLOW stays on (execute). Scope is civil.

## Dispatch

```bash
export HA_DANI_HANDOFF_OUT=/Users/c/dev/dani/out/handoff
bash ~/.grok/skills/ha-dani-handoff/scripts/ctl.sh auto --out "${HA_DANI_HANDOFF_OUT}"
# workflow name=ha-dani-handoff
```

## Tick

```bash
bash ~/.grok/skills/ha-dani-handoff/scripts/ctl.sh tick --out "${HA_DANI_HANDOFF_OUT}"
# workflow name=ha-dani-handoff-tick
```

## Roster

`dhan-owners`, `dhan-orphans`, `dhan-bucket`, `dhan-staffos`, `dhan-docs`, `dhan-sync`, `dhan-lead`

See `references/` for NORTHSTAR / CONTRACT / AUTONOMY / COLLAB.

## Never

- No live money (deposit/withdraw/payout/claim/force).
- No live patch of `api.gplaygap.com`.
- No loot harvest; do not copy `dump/`, `hack/full/`, `authz-raw/` into OUT.
- No PII / CBU / CUIT / JWT / dash passwords in chat or OUT. Paths only.
- Mac ISP → third-party = HOLD. SOCKS `127.0.0.1:1080` or `10808`.
- Read-only default. Writes only with explicit Daniel/operator flag.
- ha-hackers is NACK on this cwd unless the operator names a pentest TARGET + RoE.
