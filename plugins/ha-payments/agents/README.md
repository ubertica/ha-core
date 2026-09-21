# User agents (`$GROK_HOME/agents/`)

Grok loads `name:` from these `.md` files as `spawn_subagent` types.

## ha-payments team

Skill: `/ha-payments`

| Type | Lane / artifact |
|------|------------------|
| `pay-rails` | `rails` / `RAILS.md` |
| `pay-psp` | `psp` / `PSP.md` |
| `pay-webhooks` | `webhooks` / `WEBHOOKS.md` |
| `pay-qa` | `qa` / `GATES.md` |
| `pay-test` | `test` / `TEST-REPORT.md` |
| `pay-dev` | `dev` / `CHANGES.md` |
| `pay-sync` | `sync` / `COLLAB-STATUS.md` |
| `pay-lead` | `lead` / `SUMMARY.md` |

Conductor: `references/AUTONOMY.md` (runtime auto/tick/selftest). Parent launches the workflow.
Wiring: skill `/ha-payments`, workflow `ha-payments`, contract in skill `references/CONTRACT.md`.
OUT: `$PUMAPAY_OUT/payments/` (artifacts at that root).
Children inherit parent MCP. Talk via `OUT/.bus/` + parent (no nested spawn).
FINTECH-BUILD. No infection/drainer.
