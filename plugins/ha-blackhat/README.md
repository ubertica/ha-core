# ha-blackhat

Grok plugin (xAI marketplace layout): `agents/`, `skills/`, `commands/`.

User-level (not plugin components per xai-org/plugin-marketplace):

- `~/.grok/workflows/ha-blackhat.rhai` (+ optional -tick)
- `~/.grok/agents/bht-*.md`
- `~/.grok/skills/ha-blackhat/`

Children inherit the **parent** MCP (chrome-devtools, filesystem, …). This plugin does not ship `.mcp.json`.

Install: copy to `~/.grok/plugins/ha-blackhat` (auto-trusted) or `grok plugin install ha-blackhat --trust` from the HA marketplace.

Forge command: `bash ~/.grok/skills/ha-team-forge/scripts/ctl.sh forge --name ha-blackhat --prefix bht ...`
Purpose: Party (g1-g4) BLACKHAT red-team: docs-entry foothold, deep probe, exploit iff GO, loot in engagement OUT, killchain, ha-offense weapon. Layers jump/pivot/radio/intel/memory/spawn/learn. Not ha-dani civil. Not Puma Jira default.
