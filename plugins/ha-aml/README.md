# ha-aml

Grok plugin (xAI marketplace layout): `agents/`, `skills/`, `commands/`.

User-level (not plugin components per xai-org/plugin-marketplace):

- `~/.grok/workflows/ha-aml.rhai` (+ optional -tick)
- `~/.grok/agents/aml-*.md`
- `~/.grok/skills/ha-aml/`

Children inherit the **parent** MCP (chrome-devtools, filesystem, …). This plugin does not ship `.mcp.json`.

Install: copy to `~/.grok/plugins/ha-aml` (auto-trusted) or `grok plugin install ha-aml --trust` from the HA marketplace.

Forge command: `bash ~/.grok/skills/ha-team-forge/scripts/ctl.sh forge --name ha-aml --prefix aml ...`
Purpose: AML team for PumaPay v2 fintech: transaction monitoring, investigations, SAR/STR filing, customer risk rating, rule tuning and regulatory reporting. Full HA autonomy, bus collab with fraud/risk/support, selftest PASS. Same structure and quality as ha-hackers and ha-risk.
