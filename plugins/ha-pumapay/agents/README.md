# User agents (`~/.grok/agents/`)

Grok loads `name:` from these `.md` files as `spawn_subagent` types.

## PumaPay v2 team (reusable)

Skill: `/ha-pumapay` · `~/.grok/skills/ha-pumapay/SKILL.md`

| Type | Lane |
|------|------|
| `pp-lead` | SUMMARY.md + BOARD.md |
| `pp-docs` | docs/** + DOCS-INDEX.md |
| `pp-pm` | pm/JIRA-MODEL.md + pm/BACKLOG.md |
| `pp-qa` | qa/QA-PLAN.md + qa/GATES.md |
| `pp-test` | test/TEST-REPORT.md + evidence |
| `pp-dev` | dev/CHANGES.md + patches |
| `pp-repo` | repo/REPO-STATUS.md |
| `pp-sync` | sync/COLLAB-STATUS.md + bus |

Conductor: `/ha-pumapay` and tick via `ha-pumapay-tick`. Parent launches the workflow; do not pick lanes by hand.

Shared bus with ha-sentinel per COLLAB.md. Children inherit all parent MCP/tools. Talk via OUT/.bus/ + shared ~/.grok/pumapay-bus/ (no nested spawn).

See PLUGIN.md for canonical paths.
