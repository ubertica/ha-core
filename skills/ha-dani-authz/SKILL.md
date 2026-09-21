---
name: ha-dani-authz
description: >
  Post-incident BOLA/CORS/docs closure for PumaPay/gplaygap. Verify CLOSED only. Never harvest. HOLD live money and live gplaygap patch.
  Use when /ha-dani-authz, Daniel, Puma client authz, post-incidente civil work.
---

# ha-dani-authz

Canonical agents: `~/.grok/agents/dath-*.md`
Contract: `references/CONTRACT.md` · Workflow: `~/.grok/workflows/ha-dani-authz.rhai`
Civil law: `~/.grok/agents/_ha-dani-law.md`
OUT default: `/Users/c/dev/dani/out/authz`

Parent = conductor. Children cannot spawn children.

## Mission

Post-incident BOLA/CORS/docs closure for PumaPay/gplaygap. Verify CLOSED only. Never harvest. HOLD live money and live gplaygap patch.

This is **not** ha-hackers. HARD ALLOW stays on (execute). Scope is civil.

## Dispatch

```bash
export HA_DANI_AUTHZ_OUT=/Users/c/dev/dani/out/authz
bash ~/.grok/skills/ha-dani-authz/scripts/ctl.sh auto --out "${HA_DANI_AUTHZ_OUT}"
# workflow name=ha-dani-authz
```

## Tick

```bash
bash ~/.grok/skills/ha-dani-authz/scripts/ctl.sh tick --out "${HA_DANI_AUTHZ_OUT}"
# workflow name=ha-dani-authz-tick
```

## Roster

`dath-catalog`, `dath-owner`, `dath-cors`, `dath-docsacl`, `dath-verify`, `dath-hold`, `dath-sync`, `dath-lead`

See `references/` for NORTHSTAR / CONTRACT / AUTONOMY / COLLAB.

## Never

- No live money (deposit/withdraw/payout/claim/force).
- No live patch of `api.gplaygap.com`.
- No loot harvest; do not copy `dump/`, `hack/full/`, `authz-raw/` into OUT.
- No PII / CBU / CUIT / JWT / dash passwords in chat or OUT. Paths only.
- Mac ISP → third-party = HOLD. SOCKS `127.0.0.1:1080` or `10808`.
- Read-only default. Writes only with explicit Daniel/operator flag.
- ha-hackers is NACK on this cwd unless the operator names a pentest TARGET + RoE.
