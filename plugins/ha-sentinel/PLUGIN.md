# ha-sentinel

Sentinel protection team for live AMS (ha-live-sentinel + ollama-ha). Collaborates with ha-pumapay via shared bus.

Canonical live copies:

- Agents: `~/.grok/agents/sent-*.md` (sent-lead, sent-watch, sent-ollama, sent-audit, sent-improve, sent-release, sent-escalate, sent-collab)
- Skills: `~/.grok/skills/ha-sentinel/` and `~/.grok/skills/ha-sentinel-tick/`
- Workflows: `~/.grok/workflows/ha-sentinel.rhai`, `ha-sentinel-tick.rhai`
- Conductor: `~/.grok/skills/ha-sentinel/scripts/ctl.sh auto|tick|ams-mirror|ollama-ask`
- References: `~/.grok/skills/ha-sentinel/references/{NORTHSTAR,CONTRACT,AUTONOMY}.md`
- Shared bus: `~/.grok/pumapay-bus/` (see COLLAB.md)
- OUT: `~/Desktop/puma/docs/pumapay-v2/sentinel/` (or $SENTINEL_OUT)

This folder is the source mirror. Agents duplicated under plugin/agents/ and ~/.grok/agents/. Skills mirrored under ~/.grok/skills/.

Children inherit full parent MCP + tools. No nested spawn. Disk bus is source of truth.

AMS: ssh ams ; /opt/ha-live/scripts/ctl.sh sentinel|ollama|ollama-ask
