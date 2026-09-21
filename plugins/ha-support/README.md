# ha-support

Grok plugin (xAI marketplace layout): `agents/`, `skills/`, `commands/`.

User-level (not plugin components per xai-org/plugin-marketplace):

- `~/.grok/workflows/ha-support.rhai` (+ optional -tick)
- `~/.grok/agents/sup-*.md`
- `~/.grok/skills/ha-support/`

Children inherit the **parent** MCP (chrome-devtools, filesystem, …). This plugin does not ship `.mcp.json`.

Install: copy to `~/.grok/plugins/ha-support` (auto-trusted) or `grok plugin install ha-support --trust` from the HA marketplace.

Forge command: `bash ~/.grok/skills/ha-team-forge/scripts/ctl.sh forge --name ha-support --prefix sup ...`
Purpose: PumaPay support AI for SDPPAY.
