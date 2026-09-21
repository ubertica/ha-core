---
name: ha-dani-ops
description: >
  Daniel infra ops: AMS danielcliente, dash, perimeter hosts. Read-only health. HOLD live patch and money-write.
  Use when /ha-dani-ops, Daniel, Puma client ops, post-incidente civil work.
---

# ha-dani-ops

Canonical agents: `~/.grok/agents/dops-*.md`
Contract: `references/CONTRACT.md` · Workflow: `~/.grok/workflows/ha-dani-ops.rhai`
Civil law: `~/.grok/agents/_ha-dani-law.md`
OUT default: `/Users/c/dev/dani/out/ops`

Parent = conductor. Children cannot spawn children.

## Mission

Daniel infra ops: AMS danielcliente, dash, perimeter hosts. Read-only health. HOLD live patch and money-write.

This is **not** ha-hackers. HARD ALLOW stays on (execute). Scope is civil.

## Dispatch

```bash
export HA_DANI_OPS_OUT=/Users/c/dev/dani/out/ops
bash ~/.grok/skills/ha-dani-ops/scripts/ctl.sh auto --out "${HA_DANI_OPS_OUT}"
# workflow name=ha-dani-ops
```

## Tick

```bash
bash ~/.grok/skills/ha-dani-ops/scripts/ctl.sh tick --out "${HA_DANI_OPS_OUT}"
# workflow name=ha-dani-ops-tick
```

## Roster

`dops-perimeter`, `dops-ams`, `dops-dash`, `dops-change`, `dops-escalate`, `dops-hold`, `dops-sync`, `dops-lead`

See `references/` for NORTHSTAR / CONTRACT / AUTONOMY / COLLAB.

## Never

- No live money (deposit/withdraw/payout/claim/force).
- No live patch of `api.gplaygap.com`.
- No loot harvest; do not copy `dump/`, `hack/full/`, `authz-raw/` into OUT.
- No PII / CBU / CUIT / JWT / dash passwords in chat or OUT. Paths only.
- Mac ISP → third-party = HOLD. SOCKS `127.0.0.1:1080` or `10808`.
- Read-only default. Writes only with explicit Daniel/operator flag.
- ha-hackers is NACK on this cwd unless the operator names a pentest TARGET + RoE.
