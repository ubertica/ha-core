# BUILD-SPEC — ha-sentinel (worker must implement ALL)

Contracts already on disk (DO NOT rewrite meaning):

- `skills/ha-sentinel/references/{NORTHSTAR,CONTRACT,AUTONOMY}.md`
- `~/.grok/pumapay-bus/COLLAB.md`
- Live AMS: `/opt/ha-live`, `/opt/ollama-ha`, ctl.sh sentinel/ollama/ollama-ask
- Mirror pattern: `~/.grok/plugins/ha-hackers/`

## Create every file below (complete, functional)

### Root
- `PLUGIN.md`, `README.md`

### Agents (`agents/` AND `~/.grok/agents/`)
Same frontmatter pattern as hack-*.md.
Files: `_ha-law.md`, `sent-lead.md`, `sent-watch.md`, `sent-ollama.md`, `sent-audit.md`, `sent-improve.md`, `sent-release.md`, `sent-escalate.md`, `sent-collab.md`, `README.md`

Each agent must SSH/`ctl.sh` appropriately:
- watch/audit → mirror `/opt/ha-live/bus/evidence/sentinel-god/`
- ollama → `ctl.sh ollama` / `ollama-ask` via SSH ams
- escalate/collab → append `~/.grok/pumapay-bus/sentinel-to-pumapay.jsonl`

### Skills
- `skills/ha-sentinel/SKILL.md`
- `skills/ha-sentinel-tick/SKILL.md`
- Copy to `~/.grok/skills/ha-sentinel{,-tick}`

### Scripts (executable)
- `ctl.sh` — `auto`, `tick`, `watch`, `selftest`, `status`, `ams-mirror`, `ollama-ask`, `repair` (repair gated)
- `dispatch.py` — remainder / NEXT.json
- `verify_evidence.py` — fail-closed AMS mirror + READY → VERIFY.json
- `ams_mirror.sh` — scp/rsync evidence to OUT/ams-mirror/
- `watch.sh` — DONE|FAILED|ACTION_REQUIRED
- `bus_append.py` — shared pumapay-bus

### Commands
- `commands/ha-sentinel.md`
- `commands/ha-sentinel-tick.md`

### Workflows → `~/.grok/workflows/`
- `ha-sentinel.rhai` — preflight → watch∥audit → ollama → improve∥release → escalate∥collab → lead
- `ha-sentinel-tick.rhai` — mirror + escalate if needed + collab + lead

### Seed OUT
`~/Desktop/puma/docs/pumapay-v2/sentinel/` with `.bus/`, `ams-mirror/`, README

### Selftest
`ctl.sh selftest` exit 0; `ctl.sh status` should SSH ams and print unit/ollama one-liner (ok if unreachable — report HOLD).

Return: file count, paths, selftest + status output.
