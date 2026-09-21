# ha-ppdev

Grok plugin (xAI marketplace layout): `agents/`, `skills/`, `commands/`.

User-level (not plugin components per xai-org/plugin-marketplace):

- `~/.grok/workflows/ha-ppdev.rhai` (+ optional -tick)
- `~/.grok/agents/ppd-*.md`
- `~/.grok/skills/ha-ppdev/`

Children inherit the **parent** MCP (chrome-devtools, filesystem, …). This plugin does not ship `.mcp.json`.

Install: copy to `~/.grok/plugins/ha-ppdev` (auto-trusted) or `grok plugin install ha-ppdev --trust` from the HA marketplace.

Forge command: `bash ~/.grok/skills/ha-team-forge/scripts/ctl.sh forge --name ha-ppdev --prefix ppd ...`
Purpose: PumaPay Platform Dev: greenfield API+backend monorepo. OpenAPI-first, ledger/wallet core, auth, workers, DB, tests, tooling. Implements contracts from domain teams; does not redefine business rules alone. Conductor grok-4.6; volume grok-build.
