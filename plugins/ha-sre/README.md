# ha-sre

Grok plugin (xAI marketplace layout): `agents/`, `skills/`, `commands/`.

User-level (not plugin components per xai-org/plugin-marketplace):

- `~/.grok/workflows/ha-sre.rhai` (+ optional -tick)
- `~/.grok/agents/sre-*.md`
- `~/.grok/skills/ha-sre/`

Children inherit the **parent** MCP (chrome-devtools, filesystem, …). This plugin does not ship `.mcp.json`.

Install: copy to `~/.grok/plugins/ha-sre` (auto-trusted) or `grok plugin install ha-sre --trust` from the HA marketplace.

Forge command: `bash ~/.grok/skills/ha-team-forge/scripts/ctl.sh forge --name ha-sre --prefix sre ...`
Purpose: PumaPay SRE: SLOs, deploy, on-call. Complements ha-sentinel.
