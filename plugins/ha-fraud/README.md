# ha-fraud

Grok plugin (xAI marketplace layout): `agents/`, `skills/`, `commands/`.

User-level (not plugin components per xai-org/plugin-marketplace):

- `~/.grok/workflows/ha-fraud.rhai` (+ optional -tick)
- `~/.grok/agents/fraud-*.md`
- `~/.grok/skills/ha-fraud/`

Children inherit the **parent** MCP (chrome-devtools, filesystem, …). This plugin does not ship `.mcp.json`.

Install: copy to `~/.grok/plugins/ha-fraud` (auto-trusted) or `grok plugin install ha-fraud --trust` from the HA marketplace.

Forge command: `bash ~/.grok/skills/ha-team-forge/scripts/ctl.sh forge --name ha-fraud --prefix fraud ...`
Purpose: Fraud Prevention team for PumaPay: velocity/device/behavioral detection, fraud rules, case management, scoring integration, chargeback defense and loss prevention. Matches ha-hackers operating model, NORTHSTAR/CONTRACT/AUTONOMY, full agent roster, bus sync to AML/ledger/payments. Selftest required.
