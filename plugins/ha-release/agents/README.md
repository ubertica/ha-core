# User agents (`~/.grok/agents/`)

Grok loads `name:` from these `.md` files as `spawn_subagent` types.

## ha-release team

Skill: `/ha-release`

| Type | Lane |
|------|------|
| `rel-train` | Version trains, Fix Versions, calendars. |
| `rel-gonogo` | Go/no-go checklist: risk+sre+sentinel+sec. |
| `rel-notes` | Release notes and customer comms drafts. |
| `rel-qa` | Release QA evidence pack. |
| `rel-dev` | Release tooling/scripts changes. |
| `rel-sync` | Coordinate all teams on bus board. |
| `rel-lead` | SUMMARY + BOARD for release. |

Conductor: references/AUTONOMY.md. Parent launches the workflow; do not pick lanes by hand.

Wiring: skill `/ha-release`, workflow `ha-release`, contract in the skill `references/CONTRACT.md`.
Children inherit all parent MCP/tools. They talk via `OUT/.bus/` + parent (no nested spawn).
