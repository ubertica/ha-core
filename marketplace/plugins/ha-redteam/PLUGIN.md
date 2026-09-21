# ha-redteam

Party (g1–g4) **civil** red-team. Deep audit + test in **this** TUI, then fixes + docs + Jira.

Canonical live copies:

- Skill: `~/.grok/skills/ha-redteam/`
- Tick: `~/.grok/skills/ha-redteam-tick/`
- Agents: `~/.grok/agents/rdt-*.md`
- Personas / roles: `~/.grok/personas|roles/rdt-*.toml`
- Workflows: `~/.grok/workflows/ha-redteam.rhai` · `ha-redteam-tick.rhai`
- Shared KB: `ha-rtk-kb` (`~/.grok/ha-rtk-kb/`)
- OUT default: `/Users/c/dev/dani/out/redteam`

This folder is the marketplace mirror. Sync from those paths.

## Party seats

| Seat | Job |
|------|-----|
| g1 | this TUI: tools, docs-entry dispatch, jira_sync, lead |
| g2 | surface brains (`playbook=g2-surface`) — OpenAPI /docs |
| g3 | test brains (`playbook=g3-weapon`) — probe + ACT loops |
| g4 | adversary/fix (`playbook=g4-adversary`) — refute, FIXES, AUDIT |

No 4 TUIs. Nested `grok -p` banned.

## Toolkit

- `docs-entry` — live `/docs`/swagger unauth+webhook pack
- `ha-core` — ralph / SDD / TDD / verify-on-disk
- `ha-correction-loops` — ACT (Attempt → Check → Try-fix)
- `ha-dani` civil overlay — no loot, no live money
- layers: jump · pivot · radio · intel · memory · spawn · learn

## Dispatch

```bash
export HA_REDTEAM_OUT=/Users/c/dev/dani/out/redteam
bash ~/.grok/skills/ha-redteam/scripts/ctl.sh auto \
  --target "$TARGET" --out "$HA_REDTEAM_OUT" \
  --proxy "${HA_PROXY:-socks5h://127.0.0.1:10808}"
# workflow name=ha-redteam
```

Exploit/weapon only if disk `go_count>0` **and** operator did not HOLD live.

## Never

- No live money. No live patch `api.gplaygap.com`.
- No loot harvest. No PII / CBU / JWT in chat or OUT.
- Mac ISP → third-party = HOLD. SOCKS AMS.
- No invented GO. Missing evidence → HOLD.
