# NORTHSTAR — ha-dani-audit

**Client:** Daniel (PumaPay + aggregator + other gaming already in production).
**Ask:** periodic auditor that coexists. He decides. We do not take the repo.

**DONE** = Daniel can open `$OUT/report/DANIEL.md` and know, in human language:
1. what changed since last cadence (MR/release),
2. what handoff-debt still hurts,
3. what we recommend — as **proposals**, never as silent commits.

This pack exists because the 2026-09-10/11 incident trained the mesh to *harvest*.
Daniel asked for the opposite: **Phase 0 baseline → Phase 1 periodic review**.
See proposal SoT. Phase 2 (enhancement PRs) is **off** until he flags it.

## What “team” means

Plugin + user agents `daud-*` + skill + tick + rhai + disk bus + ctl.
Gold shape: `~/.grok/plugins/ha-hackers/` (operating model only — not the offense lanes).

## Not this pack

| That | Belongs to |
|------|------------|
| Prove F1–F12 CLOSED | `ha-dani-authz` |
| 10+ owner/orphan map | `ha-dani-handoff` |
| AMS danielcliente / dash / perimeter | `ha-dani-ops` |
| Greenfield Fastify | `ha-ppdev` |
| Product docs of THIS instance | `ha-pumapay` |
| Named pentest TARGET | `ha-hackers` (NACK here) |

## Acceptance

1. `ctl.sh selftest` exit 0.
2. OUT never contains loot images, JWTs, ACCESS.md copies.
3. No invented GO. Missing repo access → HOLD + blocker, still ship a baseline from disk SoT.
4. Daniel-facing report has **zero** technical loot and **zero** PII.
