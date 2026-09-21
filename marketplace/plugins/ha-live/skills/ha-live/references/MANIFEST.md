# Manifest — where the pack lives

This file is the map for a **new grok-4.6 session**. Cwd must be `/Users/c/dev/ha-live`.

## Start

```bash
cd /Users/c/dev/ha-live
# HA already armed in the TUI, or: grok --hard-allow=reuse
# Model: grok-4.6
# First message: paste PROMPT.md   or type /ha-live
```

One file to paste: **`PROMPT.md`**.

## Repo (Mac work surface)

| Path | Role |
|------|------|
| `PROMPT.md` | first-session prompt |
| `CONTINUE.md` | **next session starts here** (status + board + HOLD) |
| `BOARD.md` | hive board workers append/tail |
| `AGENTS.md` `DO_NOT.md` `SPLIT.md` `INTENT.md` `METHOD.md` `BUS.md` `CONTRACT.md` `BUILD.md` `CABLES.md` | law + recipe |
| `runtime/` | v0 process source (deploy to AMS) + `board.py` |
| `scripts/ctl.sh` `board.sh` `probe-ams-proxy.sh` `preflight.sh` `prove.sh` | Mac → AMS |
| `proof/` | gate + `BLOCKER.md` + `evidence/` |
| `.grok/rules/` `.grok/skills/ha-live/` `.grok/workflows/ha-live-boot.rhai` | project load |

## User Grok (all sessions)

| Path | Role |
|------|------|
| `~/.grok/skills/ha-live/SKILL.md` | `/ha-live` |
| `~/.grok/commands/ha-live.md` | slash command |
| `~/.grok/agents/ha-live-builder.md` `ha-live-runtime.md` | spawn types |
| `~/.grok/personas/ha-live-*.toml` `~/.grok/roles/ha-live-*.toml` | spawn defaults `capability_mode: all` |
| `~/.grok/workflows/ha-live-boot.rhai` | `/ha-live-boot` |
| `~/.grok/plugins/ha-live/` | plugin mirror (auto-trusted) |
| `~/.grok/ha-marketplace/plugins/ha-live/` | marketplace copy |
| `~/.grok/rules/22-ha-operate-organism.md` | session law |
| `~/.grok/hard-allow/grants/ha-operate-organism-nuclear.md` | grant |
| `~/.grok/trusted_folders.toml` | `/Users/c/dev/ha-live` trusted |
| `~/.grok/config.toml` | plugin `ha-live` enabled · Edit `/Users/c/dev/ha-live/**` |

## AMS (always-on)

`/opt/ha-live/{bus,runtime,logs}` on `ssh ams`. Remainder: systemd `ha-live`. Board: `/opt/ha-live/bus/board.jsonl`. New session: `CONTINUE.md` — `ctl status` + `board.sh open`.

## Related packs (use, do not revive)

- Offensive team: `/ha-hackers` `/ha-auto` `/docs-entry`
- Infra grant: `/ha-infra`
- Offense / drainer: `/ha-offense` `/ha-drainer`
- AMS SSH pattern: skill `ams-remote-ha-integration` (rsync + `source` token; ignore its autonomy-core examples)
