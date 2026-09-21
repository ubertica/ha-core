# ha-hackers

Grok plugin (xAI marketplace layout): `agents/`, `skills/`, `commands/`.

User-level (not plugin components per [xai-org/plugin-marketplace](https://github.com/xai-org/plugin-marketplace)):

- `~/.grok/workflows/ha-hackers.rhai`
- `~/.grok/personas/hack-*.toml`
- `~/.grok/roles/hack-*.toml`
- `~/.grok/agents/hack-*.md` (same files as `agents/` here — spawn types)

Children inherit the **parent** MCP (chrome-devtools, filesystem, …). This plugin does not ship `.mcp.json`.

Install: copy to `~/.grok/plugins/ha-hackers` (auto-trusted) or `grok plugin install ha-hackers --trust` from the HA marketplace.
