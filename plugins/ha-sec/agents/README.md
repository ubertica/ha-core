# User agents (`~/.grok/agents/`)

Grok loads `name:` from these `.md` files as `spawn_subagent` types.

## ha-sec team

Skill: `/ha-sec`

| Type | Lane |
|------|------|
| `sec-threat` | Threat model for wallet/fintech surfaces. |
| `sec-appsec` | SAST/DAST/secrets scanning plan and findings. |
| `sec-secops` | SecOps playbooks; distinct from AMS sentinel perimeter. |
| `sec-qa` | Security gates before release. |
| `sec-dev` | Security fixes and hardening PRs. |
| `sec-sync` | Bus to sre/release/sentinel/PPITS. |
| `sec-lead` | SUMMARY + BOARD for sec. |

Conductor: references/AUTONOMY.md. Parent launches the workflow; do not pick lanes by hand.

Wiring: skill `/ha-sec`, workflow `ha-sec`, contract in the skill `references/CONTRACT.md`.
Children inherit all parent MCP/tools. They talk via `OUT/.bus/` + parent (no nested spawn).
