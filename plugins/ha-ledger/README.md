# ha-ledger

Grok plugin (xAI marketplace layout): `agents/`, `skills/`, `commands/`.

User-level (not plugin components per xai-org/plugin-marketplace):

- `~/.grok/workflows/ha-ledger.rhai` (+ optional -tick)
- `~/.grok/agents/led-*.md`
- `~/.grok/skills/ha-ledger/`

Children inherit the **parent** MCP (chrome-devtools, filesystem, …). This plugin does not ship `.mcp.json`.

Install: copy to `~/.grok/plugins/ha-ledger` (auto-trusted) or `grok plugin install ha-ledger --trust` from the HA marketplace.

Forge command: `bash ~/.grok/skills/ha-team-forge/scripts/ctl.sh forge --name ha-ledger --prefix led ...`
Purpose: PumaPay ledger: double-entry, holds, recon, settlement.
