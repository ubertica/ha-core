# ha-kyc

Grok plugin (xAI marketplace layout): `agents/`, `skills/`, `commands/`.

User-level (not plugin components per xai-org/plugin-marketplace):

- `~/.grok/workflows/ha-kyc.rhai` (+ optional -tick)
- `~/.grok/agents/kyc-*.md`
- `~/.grok/skills/ha-kyc/`

Children inherit the **parent** MCP (chrome-devtools, filesystem, …). This plugin does not ship `.mcp.json`.

Install: copy to `~/.grok/plugins/ha-kyc` (auto-trusted) or `grok plugin install ha-kyc --trust` from the HA marketplace.

Forge command: `bash ~/.grok/skills/ha-team-forge/scripts/ctl.sh forge --name ha-kyc --prefix kyc ...`
Purpose: PumaPay KYC/onboarding; AI recommend human decide.
