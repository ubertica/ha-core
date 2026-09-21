# ha-release

Grok plugin (xAI marketplace layout): `agents/`, `skills/`, `commands/`.

User-level (not plugin components per xai-org/plugin-marketplace):

- `~/.grok/workflows/ha-release.rhai` (+ optional -tick)
- `~/.grok/agents/rel-*.md`
- `~/.grok/skills/ha-release/`

Children inherit the **parent** MCP (chrome-devtools, filesystem, …). This plugin does not ship `.mcp.json`.

Install: copy to `~/.grok/plugins/ha-release` (auto-trusted) or `grok plugin install ha-release --trust` from the HA marketplace.

Forge command: `bash ~/.grok/skills/ha-team-forge/scripts/ctl.sh forge --name ha-release --prefix rel ...`
Purpose: PumaPay release train go/no-go.
