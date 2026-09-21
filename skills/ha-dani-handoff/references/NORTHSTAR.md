# NORTHSTAR — ha-dani-handoff

**Pain Daniel named:** more than ten developers contributed with little/no handoff.
The codebase is chaotic: missing docs, inconsistent patterns, orphaned modules, unclear ownership.

**DONE** = a human (Daniel, a new hire, a future agent) can resume from
`$OUT/docs/HANDOFF.md` + `owners/MAP.md` without reading loot trees.

Our HA teams in `docs/pumapay-v2/TEAMS.md` are the **overlay we built after the incident**.
They are **not** the 10+ legacy authors. Do not pretend `ppd-auth` wrote production gplaygap.

Unknown owner stays `unknown`. Inventing people is a lie.

## Not this pack

Rewriting the product. Committing refactors. Mixing `exfil-loot/` into the handoff.
Staff OS live PAM writes.

## Acceptance

1. Every module row is `owned-by-HA-overlay` | `legacy-unknown` | `orphan`.
2. Bucket labels exist; `exfil-loot/` is quarantined (path only).
3. HANDOFF.md is readable in one sitting. No secrets.
