# CONTRACT — ha-dani-authz

Parent passes: `OUT` (absolute dir, default `/Users/c/dev/dani/out/authz`).
Optional: repo paths Daniel authorized, MR URL, JWT **path** (never paste), `HA_PROXY`.

## Access (what children inherit)

- Tools: full set (do **not** set `tools:` on agent md — that *restricts*).
- MCP: `mcpInheritance: all` from parent.
- Permissions: parent always-approve + inherit HA.
- HARD ALLOW: baked. Also `~/.grok/agents/_ha-law.md`.
- **Civil overlay (mandatory first read):** `~/.grok/agents/_ha-dani-law.md`
- Skills: this pack, `ha-dani` conductor. **Not** `ha-offense` / `ha-hackers` unless operator named a pentest TARGET.
- Autonomy: finish the lane without asking. Missing evidence → HOLD in the artifact. No nested spawn (Grok depth 1).

## Interconnect (children cannot spawn children)

1. **Disk bus (source of truth)**
   - Artifacts under `$OUT/` as in the lane table
   - Ready flags: `$OUT/.bus/READY.<lane>` when artifact is honest and complete
   - Notes: append-only `$OUT/.bus/notes.jsonl`
   - Cross-pack: `~/.grok/ha-dani-bus/domain-events.jsonl`
2. **Workflow** `~/.grok/workflows/ha-dani-authz.rhai` — preflight → parallel remainder → verify/civil → lead
3. **Tick** `ha-dani-authz-tick` skips READY+artifact; always remainder + sync + lead
4. **Live steer** — only the root session. Not peer-to-peer.
5. **verify_board.py + civil_scan.py** — fail-closed. Civil hit ⇒ not ok. `go_count` stays 0.

## Lane table

| id | agent | artifact | ready |
|----|-------|----------|-------|
| `catalog` | `dath-catalog` | `catalog/F-MAP.md` | `READY.catalog` |
| `owner` | `dath-owner` | `owner/FILTERS.md` | `READY.owner` |
| `cors` | `dath-cors` | `cors/POLICY.md` | `READY.cors` |
| `docsacl` | `dath-docsacl` | `docsacl/PLAN.md` | `READY.docsacl` |
| `verify` | `dath-verify` | `verify/CLOSED.md` | `READY.verify` |
| `hold` | `dath-hold` | `HOLD.md` | `READY.hold` |
| `sync` | `dath-sync` | `sync/COLLAB.md` | `READY.sync` |
| `lead` | `dath-lead` | `SUMMARY.md` | `READY.lead` |

## HOLDs

- No live money (deposit/withdraw/payout/claim/force).
- No live patch of `api.gplaygap.com`.
- No loot harvest; do not copy `dump/`, `hack/full/`, `authz-raw/` into OUT.
- No PII / CBU / CUIT / JWT / dash passwords in chat or OUT. Paths only.
- Mac ISP → third-party = HOLD. SOCKS `127.0.0.1:1080` or `10808`.
- Read-only default. Writes only with explicit Daniel/operator flag.
- ha-hackers is NACK on this cwd unless the operator names a pentest TARGET + RoE.

## Fallbacks

1. SOCKS `127.0.0.1:1080`/`10808` for third-party. Mac ISP → HOLD live.
2. AMS / dash down → disk SoT + HOLD live.
3. No JWT / no staging ACL → `dath-verify` HOLD (authz pack).
4. Accidental ha-hackers on this work → stop, NACK, continue on the matching dani pack.
5. Volume prose → ExpressAI sidecar; conductor stays grok-4.6.
6. Codex/ChatGPT.app: adapter copies via `sync-pack-to-codex.py` (Grok originals untouched).

## Finding / status block (authz + audit)

```
## [critical|high|medium|low|info|hold] title
- Asset:
- Evidence path (not body):
- Impact:
- Next:
- Status: OPEN | HOLD | CLOSED
```

No invented CLOSED. No invented GO. Evidence or it is not a finding.

## Fail closed

Missing NORTHSTAR/CONTRACT/AUTONOMY or `ctl.sh selftest` ≠ 0 ⇒ do not claim DONE.
Civil scan hits ⇒ do not claim READY for the run.
