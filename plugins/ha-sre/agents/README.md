# User agents (`~/.grok/agents/`)

Grok loads `name:` from these `.md` files as `spawn_subagent` types.

## ha-sre team

Skill: `/ha-sre`

| Type | Lane |
|------|------|
| `sre-slo` | SLOs/SLIs, error budgets, dashboards. |
| `sre-deploy` | Deploy pipelines, feature flags, rollback. |
| `sre-oncall` | On-call runbooks, paging, escalation. |
| `sre-change` | Change management checklist; link release team. |
| `sre-dev` | Infra-as-code / tooling changes. |
| `sre-sync` | Collab sentinel/release/pumapay. |
| `sre-lead` | SUMMARY + BOARD for sre. |

Conductor: references/AUTONOMY.md. Parent launches the workflow; do not pick lanes by hand.

Wiring: skill `/ha-sre`, workflow `ha-sre`, contract in the skill `references/CONTRACT.md`.
Children inherit all parent MCP/tools. They talk via `OUT/.bus/` + parent (no nested spawn).
