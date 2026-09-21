# docs-entry contract (hack-entry + hack-webhook)

Extends `~/.grok/skills/ha-hackers/references/CONTRACT.md`. Same access, interconnect, finding block. Additional law for the OpenAPI-as-entry lanes.

Parent passes: `TARGET` (spec URL, e.g. `https://api.example/docs`), `OUT` (absolute dir), optional `TOKEN_FILE` (dual-run only), optional `PROXY`.

## When this pack vs standard 5

| Question | Pack |
|----------|------|
| Map a host/app from zero (JS, sockets, SPA) | `ha-hackers` (5 lanes) |
| Spec is already public; is anything callable **without** a session? | **this pack** (`hack-entry` + `hack-webhook`) |
| JWT/IDOR on already-mapped wallet API | `hack-authz` only, not recon |
| Confirmed unauth/webhook GO needs a PoC | then `hack-exploit` + `hack-lead` |

Do not spawn `hack-recon` / `hack-exploit` / `hack-lead` “because the team has 5”. Spawn them when the question needs them.

## Probe law

- GET/HEAD/OPTIONS default. Empty POST only on `auth_entry` and webhook buckets.
- Never POST `money_write` (deposit, withdraw, transfer, payout, add-balance, force-approve) unless parent named the exact call.
- No invented GO. 400 missing-field ≠ GO. 200 public CMS ≠ GO. 200 + pending money / PII / secrets / unsigned mutating webhook = GO.
- Reuse jsonl already on disk. Do not re-spray completed (method, spec_path) pairs.
- Cap 150 paths / 400 jobs unless parent raises it.
- SOCKS/AMS when OPSEC applies.

## Artifacts

| Lane | Writes | Ready |
|------|--------|-------|
| hack-entry | `OUT/docs-entry/ENTRY.md`, `buckets.json`, `unauth-findings.md`, `unauth-probes.jsonl` | `READY.entry` |
| hack-webhook | `OUT/docs-entry/WEBHOOK.md`, `webhook-findings.md`, `webhook-probes.jsonl` | `READY.webhook` |
| none GO | `OUT/docs-entry/NEGATIVE.md` | (no exploit flag) |

## Interconnect

Children cannot spawn children. Workflow `docs-entry.rhai` is the conductor:

preflight (proxy) → entry ∥ webhook → **disk** `verify_evidence.py` → exploit+lead **only if** `OUT/.bus/VERIFY.json` `go_count > 0`.

Prober `confirmed_count` is untrusted. Missing VERIFY.json = 0.

Live steer: root session only. Parent launches the workflow (`/docs-entry` / `/ha-auto`). Do not spawn lanes by hand. Do not nested `grok -p`.

Proxy default: `socks5h://127.0.0.1:10808`. JWT optional. Money-write: `await_user` if `allow_money_write`.
