# ha-pragmatic

Grok plugin (xAI marketplace layout): `agents/`, `skills/`, `commands/`.

User-level (not plugin components per xai-org/plugin-marketplace):

- `~/.grok/workflows/ha-pragmatic.rhai` (+ optional -tick)
- `~/.grok/agents/pra-*.md`
- `~/.grok/skills/ha-pragmatic/`

Children inherit the **parent** MCP (chrome-devtools, filesystem, …). This plugin does not ship `.mcp.json`.

Install: copy to `~/.grok/plugins/ha-pragmatic` (auto-trusted) or `grok plugin install ha-pragmatic --trust` from the HA marketplace.

Forge command: `bash ~/.grok/skills/ha-team-forge/scripts/ctl.sh forge --name ha-pragmatic --prefix pra ...`
Purpose: iGaming team specialized in Pragmatic Play Integration API v3.233 (July 2025 PDF): Seamless Wallet vs Balance Transfer, CasinoGameAPI, MD5 hash, Free Spins/Chips, history/datafeeds, PP Live BO. Spec-first. Staging default. IP whitelist. Never invent GO. No live money without operator flag.
