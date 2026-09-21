# User agents (`~/.grok/agents/`)

Grok loads `name:` from these `.md` files as `spawn_subagent` types.

## ha-risk team

Skill: `/ha-risk`

| Type | Lane |
|------|------|
| `rsk-rules` | Fraud/AML rule catalog, velocity, device signals. |
| `rsk-cases` | Case queue schema, severities, SLA. |
| `rsk-score` | Scoring model notes and feature list. |
| `rsk-qa` | Risk QA: false positive/negative gates. |
| `rsk-dev` | Implement risk engine changes. |
| `rsk-sync` | Escalate to support/kyc/compliance bus. |
| `rsk-lead` | SUMMARY + BOARD for risk. |

Conductor: references/AUTONOMY.md. Parent launches the workflow; do not pick lanes by hand.

Wiring: skill `/ha-risk`, workflow `ha-risk`, contract in the skill `references/CONTRACT.md`.
Children inherit all parent MCP/tools. They talk via `OUT/.bus/` + parent (no nested spawn).
