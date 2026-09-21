# User agents (`~/.grok/agents/`)

Grok loads `name:` from these `.md` files as `spawn_subagent` types.

## ha-dani-handoff team

Skill: `/ha-dani-handoff` · Civil overlay: `_ha-dani-law.md`

| Type | Lane |
|------|------|
| `dhan-owners` | Module-to-owner map from docs/pumapay-v2 ORG/TEAMS + git history. Unknown = unknown, do not invent people. |
| `dhan-orphans` | Orphaned modules, missing docs, undocumented decisions from 10+ contributor chaos. |
| `dhan-bucket` | unified-bucket hygiene: incidents/code-audit/handoff-debt/authz-bola labels. Locks before write. |
| `dhan-staffos` | Staff OS as operational control plane notes. No live PAM writes. |
| `dhan-docs` | Handoff artifacts a human can resume from. No secrets. |
| `dhan-sync` | Bus to audit/authz/ops. |
| `dhan-lead` | Handoff debt SUMMARY + BOARD for Daniel reunion. |

Conductor: references/AUTONOMY.md. Parent launches the workflow; do not pick lanes by hand.
Default OUT: `/Users/c/dev/dani/out/handoff`
Children inherit all parent MCP/tools. They talk via `OUT/.bus/` + parent (no nested spawn).
