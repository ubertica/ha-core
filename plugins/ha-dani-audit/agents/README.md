# User agents (`~/.grok/agents/`)

Grok loads `name:` from these `.md` files as `spawn_subagent` types.

## ha-dani-audit team

Skill: `/ha-dani-audit` · Civil overlay: `_ha-dani-law.md`

| Type | Lane |
|------|------|
| `daud-baseline` | Read-only baseline of repos Daniel authorized. Inventory handoff debt. No loot copy. |
| `daud-mr` | Review merge requests: quality, consistency, maintainability, secret hygiene. Findings for humans. |
| `daud-release` | Pre/post release audit vs previous version. Regressions only with evidence. |
| `daud-consistency` | Map inconsistent patterns left by 10+ developers. Do not rewrite; propose. |
| `daud-secrets` | Static secret/token hygiene in source (not live drain). Paths only in OUT. |
| `daud-report` | Daniel-facing periodic report. No technical loot, no PII, no CBUs. |
| `daud-sync` | Bus to authz/handoff/ops. No nested grok -p. |
| `daud-lead` | SUMMARY + BOARD for audit stream. Honest HOLD if evidence missing. |

Conductor: references/AUTONOMY.md. Parent launches the workflow; do not pick lanes by hand.
Default OUT: `/Users/c/dev/dani/out/audit`
Children inherit all parent MCP/tools. They talk via `OUT/.bus/` + parent (no nested spawn).
