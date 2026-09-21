# ha-pam

Grok plugin (xAI marketplace layout): `agents/`, `skills/`, `commands/`.

User-level (not plugin components per xai-org/plugin-marketplace):

- `~/.grok/workflows/ha-pam.rhai` (+ optional -tick)
- `~/.grok/agents/pam-*.md`
- `~/.grok/skills/ha-pam/`

Children inherit the **parent** MCP (chrome-devtools, filesystem, …). This plugin does not ship `.mcp.json`.

Install: copy to `~/.grok/plugins/ha-pam` (auto-trusted) or `grok plugin install ha-pam --trust` from the HA marketplace.

Forge command: `bash ~/.grok/skills/ha-team-forge/scripts/ctl.sh forge --name ha-pam --prefix pam ...`
Purpose: PAM (Privileged Access Management) team for PumaPay staff-os and platform: access reviews, JIT grants, credential rotation, breakglass, over-privilege detection and audit evidence. Same gold quality as ha-hackers and ha-sec: full agents (pam-audit etc), contracts, autonomy, bus integration with sec/sre/backoffice, selftest.
