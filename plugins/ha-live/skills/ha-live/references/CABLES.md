# Cables (already in the machine)

Do not re-invent these. Use them.

| Cable | How |
|-------|-----|
| HA | `GROK_HARD_ALLOW_ACTIVE=1` · `SECOPS_HARD_ALLOW_TOKEN` · grants in `~/.grok/hard-allow/grants/` · operate-law `~/.grok/rules/22-ha-operate-organism.md` · organism grant `ha-operate-organism-nuclear.md` |
| Mac SOCKS | `socks5h://127.0.0.1:10808` (`HA_PROXY`) — **Mac only** (preflight 2026-09-11: up) |
| AMS SSH | `Host ams` → root@51.15.18.106 · `~/.ssh/id_ed25519` · fallback `ams-alt` |
| AMS remainder | `/opt/ha-live` · systemd `ha-live.service` · bus `/opt/ha-live/bus/{events,work,board}.jsonl` · python3 **3.6.9** |
| AMS board | `python3 /opt/ha-live/runtime/board.py` · Mac `scripts/board.sh` / `ctl board` |
| AMS proxy | **10808 down.** xray LISTEN `127.0.0.1:18082` (`/usr/bin/xray -config /etc/xray/config.json` — file missing on disk). SOCKS vs HTTP **unconfirmed** (curl both SSL_ERROR_SYSCALL). Set `HA_AMS_PROXY` only after a working probe. Remainder fail-closes until then. |
| Mac orch (optional) | pm2 `ha-orch-grok` `ha-orch-watchdog` `ha-wire-v3` — queue/wire, **not** the AMS remainder |
| Grok TUI | `permission_mode = always-approve` · `inherit_ha_on_subagent = true` · default model `grok-4.6` · plugin `ha-live` |
| Nested Grok | **banned** (`grok -p` from a child) |
| Kimi | down; do not route |
| Skill / command | `~/.grok/skills/ha-live` · `/ha-live` · workflow `ha-live-boot` |
| Agents | `ha-live-builder` · `ha-live-runtime` |
| Trusted folder | `/Users/c/dev/ha-live` and parent `/Users/c/dev` |

HA token onto AMS: write `/opt/ha-live/runtime/ha.env` (mode 600) from the Mac session env. `ssh SendEnv` is not enough. See skill `ams-remote-ha-integration` for the rsync pattern; **do not** revive autonomy-core while using it.
