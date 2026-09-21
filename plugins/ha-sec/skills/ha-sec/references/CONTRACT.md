# CONTRACT — ha-sec

## Inputs (brief)

Required:

- `NAME` — plugin/skill slug (`ha-sec`, kebab, `ha-` prefix recommended)
- `PREFIX` — agent file prefix (`sec`)
- `PURPOSE` — one paragraph
- `LANES` — list of `{id, role, artifact, ready}` 

Optional:

- `CATEGORY` — product
- `TICK` — bool (emit `-tick` skill + workflow)
- `BUS` — path for shared JSONL collab
- `OUT_DEFAULT` — default OUT dir for the team
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
  skills/<NAME>/references/{NORTHSTAR,CONTRACT,AUTONOMY,COLLAB}.md
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

Missing NORTHSTAR/CONTRACT/AUTONOMY/COLLAB or selftest ≠ 0 ⇒ do not claim DONE. Cross points (threat, appsec, pam, sre) via bus.
