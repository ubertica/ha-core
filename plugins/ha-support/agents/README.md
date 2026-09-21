# User agents (`~/.grok/agents/`)

Grok loads `name:` from these `.md` files as `spawn_subagent` types.

## ha-support team

Skill: `/ha-support`

| Type | Lane |
|------|------|
| `sup-triage` | SDPPAY triage macros, intents, routing. |
| `sup-macros` | Reply templates; no secrets; escalate rules. |
| `sup-queue` | Ticket queue SLAs mapped to SDPPAY. |
| `sup-qa` | Support quality gates / CSAT samples. |
| `sup-dev` | Bot/automation code changes. |
| `sup-sync` | Escalate to risk/kyc/payments via bus. |
| `sup-lead` | SUMMARY + BOARD for support. |

Conductor: references/AUTONOMY.md. Parent launches the workflow; do not pick lanes by hand.

Wiring: skill `/ha-support`, workflow `ha-support`, contract in the skill `references/CONTRACT.md`.
Children inherit all parent MCP/tools. They talk via `OUT/.bus/` + parent (no nested spawn).
