# ha-risk

Grok plugin (xAI marketplace layout): `agents/`, `skills/`, `commands/`.

User-level (not plugin components per xai-org/plugin-marketplace):

- `~/.grok/workflows/ha-risk.rhai` (+ optional -tick)
- `~/.grok/agents/rsk-*.md`
- `~/.grok/skills/ha-risk/`

Children inherit the **parent** MCP (chrome-devtools, filesystem, …). This plugin does not ship `.mcp.json`.

Install: copy to `~/.grok/plugins/ha-risk` (auto-trusted) or `grok plugin install ha-risk --trust` from the HA marketplace.

Forge command: `bash ~/.grok/skills/ha-team-forge/scripts/ctl.sh forge --name ha-risk --prefix rsk ...`
Purpose: PumaPay risk/fraud/AML rules, cases, scoring.
