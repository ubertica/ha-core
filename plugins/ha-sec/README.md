# ha-sec

Grok plugin (xAI marketplace layout): `agents/`, `skills/`, `commands/`.

User-level (not plugin components per xai-org/plugin-marketplace):

- `~/.grok/workflows/ha-sec.rhai` (+ optional -tick)
- `~/.grok/agents/sec-*.md`
- `~/.grok/skills/ha-sec/`

Children inherit the **parent** MCP (chrome-devtools, filesystem, …). This plugin does not ship `.mcp.json`.

Install: copy to `~/.grok/plugins/ha-sec` (auto-trusted) or `grok plugin install ha-sec --trust` from the HA marketplace.

Forge command: `bash ~/.grok/skills/ha-team-forge/scripts/ctl.sh forge --name ha-sec --prefix sec ...`
Purpose: PumaPay AppSec+SecOps. Distinct from AMS sentinel.
