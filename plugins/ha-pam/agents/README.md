# User agents (`~/.grok/agents/`)

Grok loads `name:` from these `.md` files as `spawn_subagent` types.

## ha-pam team

Skill: `/ha-pam`

| Type | Lane |
|------|------|
| `pam-audit` | Privileged access reviews, entitlement audits, access certification. |
| `pam-jit` | Just-in-time access, time-bound grants, approval workflows. |
| `pam-rotation` | Credential rotation, secrets management, breakglass procedures. |
| `pam-breakglass` | Emergency access, incident response elevated privileges, logging. |
| `pam-qa` | PAM QA: coverage, over-priv detection, compliance evidence. |
| `pam-dev` | PAM platform integrations, automation, connectors. |
| `pam-sync` | Sync with sec, sre, backoffice, release for access policies. |
| `pam-lead` | PAM SUMMARY + BOARD, least-privilege enforcement ownership. |

Conductor: references/AUTONOMY.md. Parent launches the workflow; do not pick lanes by hand.

Wiring: skill `/ha-pam`, workflow `ha-pam`, contract in the skill `references/CONTRACT.md`.
Children inherit all parent MCP/tools. They talk via `OUT/.bus/` + parent (no nested spawn).
