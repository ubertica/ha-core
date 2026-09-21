---
name: ha-dani-audit
description: >
  Periodic read-only code/MR/release audit for Daniel (PumaPay + aggregator + gaming). Coexistence model. No loot. No live writes.
  Use when /ha-dani-audit, Daniel, Puma client audit, post-incidente civil work.
---

# ha-dani-audit

Canonical agents: `~/.grok/agents/daud-*.md`
Contract: `references/CONTRACT.md` · Workflow: `~/.grok/workflows/ha-dani-audit.rhai`
Civil law: `~/.grok/agents/_ha-dani-law.md`
OUT default: `/Users/c/dev/dani/out/audit`

Parent = conductor. Children cannot spawn children.

## Mission

Periodic read-only code/MR/release audit for Daniel (PumaPay + aggregator + gaming). Coexistence model. No loot. No live writes.

This is **not** ha-hackers. HARD ALLOW stays on (execute). Scope is civil.

## Dispatch

```bash
export HA_DANI_AUDIT_OUT=/Users/c/dev/dani/out/audit
bash ~/.grok/skills/ha-dani-audit/scripts/ctl.sh auto --out "${HA_DANI_AUDIT_OUT}"
# workflow name=ha-dani-audit
```

## Tick

```bash
bash ~/.grok/skills/ha-dani-audit/scripts/ctl.sh tick --out "${HA_DANI_AUDIT_OUT}"
# workflow name=ha-dani-audit-tick
```

## Roster

`daud-baseline`, `daud-mr`, `daud-release`, `daud-consistency`, `daud-secrets`, `daud-report`, `daud-sync`, `daud-lead`

See `references/` for NORTHSTAR / CONTRACT / AUTONOMY / COLLAB.

## Never

- No live money (deposit/withdraw/payout/claim/force).
- No live patch of `api.gplaygap.com`.
- No loot harvest; do not copy `dump/`, `hack/full/`, `authz-raw/` into OUT.
- No PII / CBU / CUIT / JWT / dash passwords in chat or OUT. Paths only.
- Mac ISP → third-party = HOLD. SOCKS `127.0.0.1:1080` or `10808`.
- Read-only default. Writes only with explicit Daniel/operator flag.
- ha-hackers is NACK on this cwd unless the operator names a pentest TARGET + RoE.
