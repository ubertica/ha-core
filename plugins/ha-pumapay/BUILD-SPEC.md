# BUILD-SPEC — ha-pumapay (worker must implement ALL)

Contracts already on disk (DO NOT rewrite meaning):

- `skills/ha-pumapay/references/{NORTHSTAR,CONTRACT,AUTONOMY}.md`
- `~/.grok/pumapay-bus/COLLAB.md`
- Mirror pattern: `~/.grok/plugins/ha-hackers/`

## Create every file below (complete, functional — no stubs that say TODO)

### Root
- `PLUGIN.md` — canonical paths (plugin + `~/.grok/agents/pp-*.md` + `~/.grok/skills/ha-pumapay` + workflows)
- `README.md` — how to run `/ha-pumapay`, tick, collab with sentinel

### Agents (`agents/` AND copy identical to `~/.grok/agents/`)
Frontmatter like hack-lead: name, description, prompt_mode: full, model: inherit, permission_mode: default, agents_md: true, mcpInheritance: all.
Body: HA prefix + role + which artifact + touch READY + no nested spawn.
Files: `_ha-law.md` (copy from ha-hackers), `pp-lead.md`, `pp-docs.md`, `pp-pm.md`, `pp-qa.md`, `pp-test.md`, `pp-dev.md`, `pp-repo.md`, `pp-sync.md`, `README.md`

### Skills
- `skills/ha-pumapay/SKILL.md` — triggers: /ha-pumapay, pumapay v2, docs/PM/QA team
- `skills/ha-pumapay-tick/SKILL.md` — periodic tick
- Copy skill trees to `~/.grok/skills/ha-pumapay` and `ha-pumapay-tick` (rsync/cp -R)

### Scripts (`skills/ha-pumapay/scripts/` — executable)
- `ctl.sh` — subcommands: `auto`, `tick`, `watch`, `selftest`, `status`, `bus-append`
- `dispatch.py` — pack router + remainder → writes `OUT/.bus/NEXT.json`
- `verify_board.py` — fail-closed: count READY + required artifacts → `VERIFY.json`
- `watch.sh` — stdout only DONE|FAILED|ACTION_REQUIRED
- `bus_append.py` — append JSONL to `~/.grok/pumapay-bus/`

### Commands
- `commands/ha-pumapay.md`
- `commands/ha-pumapay-tick.md`

### Workflows → `~/.grok/workflows/`
- `ha-pumapay.rhai` — phases per AUTONOMY (preflight → docs∥pm → qa∥test → dev∥repo → sync → lead). Use `agent()` like ha-hackers.rhai. Prefix HA. Skip if READY exists.
- `ha-pumapay-tick.rhai` — remainder + sync + lead only.

### Seed product tree under `~/Desktop/puma/docs/pumapay-v2/`
- `README.md`, `DOCS-INDEX.md`
- dirs: `docs/epics`, `docs/stories`, `docs/tasks`, `docs/bugs`, `pm`, `qa`, `test`, `dev`, `repo`, `sync`, `.bus`
- `pm/JIRA-MODEL.md` skeleton referencing Boldt keys pattern (SITS/SDU style → PPAY)

### Selftest
`ctl.sh selftest` must exit 0 if all agents+scripts+workflows exist.

Return: file count, paths, selftest output.
