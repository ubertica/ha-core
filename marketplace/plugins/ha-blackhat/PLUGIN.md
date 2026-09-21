# ha-blackhat

Party (g1–g4) **BLACKHAT** twin of `ha-redteam`. Same knowledge (`ha-rtk-kb`). Separate lanes/OUT.

Canonical live copies:

- Skill: `~/.grok/skills/ha-blackhat/`
- Tick: `~/.grok/skills/ha-blackhat-tick/`
- Agents: `~/.grok/agents/bht-*.md`
- Personas / roles: `~/.grok/personas|roles/bht-*.toml`
- Workflows: `~/.grok/workflows/ha-blackhat.rhai` · `ha-blackhat-tick.rhai`
- Shared KB: `ha-rtk-kb`
- OUT default: `/Users/c/dev/ha-live/proof/engagements/blackhat`

This folder is the marketplace mirror. Sync from those paths.

## Party seats

| Seat | Core lanes |
|------|------------|
| g1 | lead, weapon, spawn |
| g2 | entry, jump |
| g3 | probe, exploit, loot, intel |
| g4 | chain, docs, OBJECTIVE_POLL |

No 4 TUIs. Nested `grok -p` banned. HARDALLOW radio, not Puma Jira default.

## Dispatch

```bash
bash ~/.grok/skills/ha-blackhat/scripts/ctl.sh auto --target "$TARGET" --out "$HA_BLACKHAT_OUT"
# workflow name=ha-blackhat
bash ~/.grok/skills/ha-blackhat/scripts/ctl.sh layers --out "$OUT"
```

Exploit/loot/weapon only if disk `go_count>0`. Accidental run on Daniel cwd → NACK, route to `ha-redteam`. Loot never into product repos.

## Layers

jump · pivot · radio · intel · memory · spawn · learn (shared scripts via KB).
