---
name: ha-redteam
description: >
  Party (g1–g4) civil red-team: deep audits/tests (docs-entry, ha-core TDD/verify-on-disk, ACT loops).
  Propose fixes, document, Jira. Layers: jump/pivot, realtime radio, intel (CVE/KEV),
  context-nodes memory, g1 children, self-learn. Triggers: /ha-redteam, redteam party.
---

# ha-redteam

Canonical agents: `~/.grok/agents/rdt-*.md`  
Personas: `~/.grok/personas/rdt-*.toml` · Roles: `~/.grok/roles/rdt-*.toml`  
Contract: `references/CONTRACT.md` · Autonomy: `references/AUTONOMY.md`  
Civil law: `~/.grok/agents/_ha-dani-law.md`  
Party: this TUI + MCP `grok-party` (`party_who` / `party_ask`). **No 4 TUIs.**  
OUT default: `/Users/c/dev/dani/out/redteam`  
**Shared KB with ha-blackhat:** `ha-rtk-kb` (`~/.grok/ha-rtk-kb/`). Lanes separate; intel/memory/findings-index/learn are one.

Parent = conductor (g1). Children cannot spawn children. Nested `grok -p` banned.

## What this is

Authorized **deep audit + test** red-team in **party**, then **fixes + docs + Jira**.

| Piece | Job |
|-------|-----|
| Party g1 | this TUI: tools, docs-entry dispatch, jira_sync, lead |
| Party g2 | surface brains (`playbook=g2-surface`) — OpenAPI /docs |
| Party g3 | test brains (`playbook=g3-weapon`) — probe + ACT loops |
| Party g4 | adversary/fix (`playbook=g4-adversary`) — refute, FIXES, AUDIT |
| `docs-entry` | live `/docs`/swagger unauth+webhook pack (not 5-lane harvest) |
| `ha-core` | ralph / SDD / TDD / verify-on-disk |
| `ha-correction-loops` | ACT: Attempt → Check → Try-fix (bounded) |
| `ha-dani` | civil overlay: no loot, no live money, Daniel decides writes |
| **layers** | jump · pivot (ha-pivot bus) · radio · intel (KEV/CVE) · memory (nodes) · spawn · learn |
| **CHARTER** | UNBREAKABLE vs BENDABLE — bend the rest to hit OBJECTIVE |

This is **not** ha-hackers loot. HARD ALLOW stays on (execute). Scope is civil red-team.

Always-on: `ctl.sh layers --out OUT` (every auto/tick). Radio = `comms.jsonl` + `party_ask` + `ha hardallow`. Memory = `nodes_search` / `nodes_commit_turn`. Children = g1 only, budget 8.

## Dispatch

```bash
export HA_REDTEAM_OUT=/Users/c/dev/dani/out/redteam
bash ~/.grok/skills/ha-redteam/scripts/ctl.sh auto \
  --target "$TARGET" --out "$HA_REDTEAM_OUT" \
  --proxy "${HA_PROXY:-socks5h://127.0.0.1:10808}"
# then workflow name=ha-redteam
```

`/docs` / swagger / openapi → entry lane runs **docs-entry** (preflight → entry∥webhook → disk verify). Exploit/weapon only if disk `go_count>0` **and** operator did not HOLD live.

## Party

Do not spawn extra Groks. `@g2`/`@g3`/`@g4`/`@all` via `party_ask`. `mode=round` when seats must hear each other.

g3 oauth hole → skip; g4 dual (tests then adversary). Do not invent g3's voice.

## Jira

After disk `VERIFY.json`: `ctl.sh jira-sync --out OUT` (wraps ha-hackers `jira_sync.py`). Auto via `ha-jira-watch`. Skip `HA_JIRA_DISABLE=1`. Redact JWT/PII/CBU. Labels `HOLD-prod` `pack-ha-redteam`. PumaPay board only.

## Tick

```bash
bash ~/.grok/skills/ha-redteam/scripts/ctl.sh tick --out "$HA_REDTEAM_OUT"
# workflow name=ha-redteam-tick
```

Remainder + always sync/jira/lead.

## Never

- No live money. No live patch `api.gplaygap.com`.
- No loot harvest; do not copy `dump/` `hack/` into OUT.
- No PII / CBU / JWT / dash passwords in chat or OUT. Paths only.
- Mac ISP → third-party = HOLD. SOCKS AMS.
- No invented GO. Missing evidence → HOLD.
- Accidental ha-hackers harvest on Daniel cwd → NACK, continue here or `ha-dani-authz`.
