# User agents (`~/.grok/agents/`)

Grok loads `name:` from these `.md` files as `spawn_subagent` types.

## ha-kyc team

Skill: `/ha-kyc`

| Type | Lane |
|------|------|
| `kyc-flows` | Onboarding/re-KYC flows and vendor matrix. |
| `kyc-review` | Manual review queue; AI recommend / human decide. |
| `kyc-docs` | Document types, retention, redaction rules. |
| `kyc-qa` | KYC acceptance gates and vendor sandbox. |
| `kyc-dev` | Implement KYC integrations. |
| `kyc-sync` | Bus to risk/compliance/support. |
| `kyc-lead` | SUMMARY + BOARD for kyc. |

Conductor: references/AUTONOMY.md. Parent launches the workflow; do not pick lanes by hand.

Wiring: skill `/ha-kyc`, workflow `ha-kyc`, contract in the skill `references/CONTRACT.md`.
Children inherit all parent MCP/tools. They talk via `OUT/.bus/` + parent (no nested spawn).
