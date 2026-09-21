# CONTRACT — ha-fraud

## Inputs (brief)

Required:

- `NAME` — plugin/skill slug (`ha-fraud`, kebab, `ha-` prefix recommended)
- `PREFIX` — agent file prefix (`fraud`)
- `PURPOSE` — one paragraph
- `LANES` — list of `{id, role, artifact, ready}` 

Optional:

- `CATEGORY` — meta
- `TICK` — bool (emit `-tick` skill + workflow)
- `BUS` — path for shared JSONL collab
- `OUT_DEFAULT` — default OUT dir for the team
- `AMS` — bool (SSH ams patterns like sentinel)
- `GOLD` — path to mirror (default ha-hackers plugin)

## Outputs (must exist after forge)

```
~/.grok/plugins/<NAME>/
  plugin.json
  PLUGIN.md
  README.md
  BUILD-SPEC.md          # frozen brief used
  agents/_ha-law.md
  agents/<PREFIX>-*.md
  agents/README.md
  commands/<NAME>.md
  commands/<NAME>-tick.md   # if TICK
  skills/<NAME>/SKILL.md
  skills/<NAME>/references/{NORTHSTAR,CONTRACT,AUTONOMY}.md
  skills/<NAME>/references/COLLAB.md   # if BUS
  skills/<NAME>/scripts/{ctl.sh,dispatch.py,verify_*.py,watch.sh}
  skills/<NAME>-tick/SKILL.md          # if TICK

~/.grok/agents/<PREFIX>-*.md   # synced
~/.grok/skills/<NAME>/         # synced
~/.grok/workflows/<NAME>.rhai
~/.grok/workflows/<NAME>-tick.rhai     # if TICK
```

## Agent frontmatter (mandatory)

```yaml
---
name: <PREFIX>-<lane>
description: >
  <one line>. Team <NAME>.
prompt_mode: full
model: inherit
permission_mode: default
agents_md: true
mcpInheritance: all
---
```

Body starts with HA law. No `tools:` key (restricts). No nested spawn.

## Workflow law

- Starts with pure-literal `let meta = #{ name, description, phases, ... };`
- Phases: Preflight → parallel lanes → verify/gate → lead
- Skip if `OUT/.bus/READY.<lane>` exists
- `ctl.sh selftest` exit 0

## Modes

| Mode | Does |
|------|------|
| `plugin` | full plugin tree only |
| `agents` | agents (+ sync to ~/.grok/agents) from LANES |
| `team` | everything (default) |
| `tick` | add periodic tick skill+workflow onto existing team |

## Fail closed

Missing NORTHSTAR/CONTRACT/AUTONOMY or selftest ≠ 0 ⇒ do not claim DONE.
