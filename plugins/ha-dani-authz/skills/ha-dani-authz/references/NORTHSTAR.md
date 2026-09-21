# NORTHSTAR — ha-dani-authz

**Incident:** 2026-09-10/11 customer JWT (`role=customer`) became a **platform super-reader**
because unsuffixed `/backoffice/*` GET handlers lacked object-level owner filters.
JWT alg:none / weak-secret / header-spoof **failed**. CORS `Origin` reflection + `credentials: true`
amplified browser exfil. RoE was GET-only; no money-write succeeded.

**DONE** = each of F1–F12 is either:
- **CLOSED** with a negative test (foreign userid → 401/403, not 200 with foreign rows), or
- **HOLD** with a named blocker (no JWT, no SOCKS, no staging ACL, live-patch forbidden).

`CLOSED` is an artifact in `verify/CLOSED.md`. It is **not** a pentest GO and **not** loot.

Root-cause (from incident review, do not re-derive by re-exfil):
missing mandatory owner filters on `:id` and unsuffixed list handlers.
`/list` and `/my-*` were correctly scoped. Align the rest.

## F-cluster (IDs only — full text in incident SoT)

CRITICAL: F1 payment unsuffixed · F2 user/:id · F3 wallet txs/:id
HIGH: F4 supreme-parent banks · F5 agent-bank-account list · F6 FX list
      F7 stats aggregates · F8 pending KYC · F9 support audit · F10 CORS+credentials
MED/LOW: F11 public /docs · F12 cluster (settings, verbose 500s, alg:none→500)

## Not this pack

Re-running harvest, copying `dump/`, expanding IDOR, money-write PoCs, live patch gplaygap.
Those are how the mesh got the offensive default. Stop.

## Acceptance

1. `catalog/F-MAP.md` cites the incident review, not new loot.
2. `verify/CLOSED.md` never says CLOSED without HTTP evidence of **denial**.
3. `HOLD.md` exists whenever live verify is impossible.
4. Civil scan clean. `go_count` stays 0 in VERIFY.json.
