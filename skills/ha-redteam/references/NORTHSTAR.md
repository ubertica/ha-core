# NORTHSTAR — ha-redteam

**DONE** = a named TARGET has a disk pack Daniel (or the operator) can open:

1. what was tested (entry + probe + ACT loops),
2. what is confirmed on disk (no invented GO),
3. **proposed** fixes (not silent prod patches),
4. human audit doc,
5. Jira keys for each finding+fix (`jira/JIRA.md` + `.bus/JIRA-SYNC.json`).

Party 4 seats in **this** TUI. Gold shape: `ha-hackers` operating model + `ha-dani` civil overlay + `docs-entry` for `/docs`.

Personas + roles for every `rdt-*` lane **and layer** are **required** (I/O closed).

Always-on layers (jump/pivot/radio/intel/memory/spawn/learn) do not block core VERIFY. CHARTER UNBREAKABLE stays unbreakable; everything else non-destructive may be bent to hit OBJECTIVE.

## Not this pack

| That | Belongs to |
|------|------------|
| 5-lane harvest pentest | `ha-hackers` |
| Party extreme APT/0day | `ha-party-x` |
| Prove F1–F12 CLOSED only | `ha-dani-authz` |
| MR/release prose for Daniel | `ha-dani-audit` |
| Live money / live gplaygap patch | HOLD (all packs) |

## Acceptance

1. `ctl.sh selftest` exit 0.
2. OUT never contains loot images, JWTs, ACCESS.md copies.
3. `go_count` from `probe/FINDINGS.jsonl` / disk evidence only — never `ready_count`.
4. Jira push is fail-open (never fail verify). Missing Atlassian secrets → `JIRA-SYNC.json` skipped reason.
5. Fixes are proposals in `fix/FIXES.md` until Daniel/operator flags a write.
