# Party-x contract

Parent passes: `TARGET`, `OUT` (absolute), optional `TOKEN_FILE`, `PROXY`, `PIPELINE`, `allow_money_write`.

## Who has tools

| Seat | Tools | Job |
|------|-------|-----|
| **g1** (this TUI) | all (shell, MCP, kali, chrome, files) | conductor. Executes probes. Writes disk. Never impersonates peers. |
| **g2/g3/g4** | **none** (chat/completions via `party_ask` / `party_brain.mjs`) | brains. Design, hypothesize, refute. They do **not** curl. |

A seat claiming `GO` in prose is **untrusted**. Only `verify_evidence.py` (ha-hackers) or `scripts/run.py verify` may set GO.

## Interconnect

1. Disk bus `OUT/.bus/` — source of truth
   - `READY.<wave-id>` empty flag when the wave artifact is on disk
   - `notes.jsonl` append-only `{from,to,type,wave,path,msg}`
   - `party/<wave-id>.json` raw seat replies
   - `PLAN.json` / `NEXT.json` / `VERIFY.json`
2. Pipeline JSON under `pipelines/*.json` — wave order is **host**, not prompt
3. `party_ask` with `playbook=` **or** `node scripts/party_brain.mjs`
4. Reuse ha-hackers `session_guard.py` + `verify_evidence.py` + `workstream.py`
5. No nested `grok -p`. No 4 TUIs. No reload HA.

## Finding block (same as ha-hackers)

```
## [critical|high|medium|low|info] title
- Asset:
- Request:
- Evidence:
- Impact:
- Next:
```

Evidence path on disk or it is not a finding. No invented GO.

## OPSEC

PROXY on every g1 curl (`socks5h://127.0.0.1:10808` unless operator set another). No Mac ISP → TARGET. Dummy ids. No dump uids. No live money unless `allow_money_write` and operator resumed.

## g3 offline

g3 needs `grok3 login --oauth`. Fallback: g4 loads **both** `g3-weapon` and `g4-adversary` in sequential rounds (weapon first, adversary second). Do not invent g3's voice.
