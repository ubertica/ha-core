# BUILD-SPEC — implement ha-team-forge skill + workflow + plugin mirror

Parent already wrote: `references/{NORTHSTAR,CONTRACT,AUTONOMY}.md` under `~/.grok/skills/ha-team-forge/`.

Gold to copy patterns from: `~/.grok/plugins/ha-hackers/`
Also read: `~/.grok/plugins/ha-pumapay/BUILD-SPEC.md`, `ha-sentinel/BUILD-SPEC.md` (examples of forged teams).

## Deliver ALL of this

### A. Skill (canonical: `~/.grok/skills/ha-team-forge/`)
1. `SKILL.md` — triggers: create team, forge plugin, scaffold agents, /ha-team-forge, new ha team like ha-hackers
2. Keep existing references/
3. `templates/` complete text templates with `{{NAME}}` `{{PREFIX}}` `{{LANE}}` `{{PURPOSE}}` placeholders:
   - `plugin.json.tmpl`
   - `PLUGIN.md.tmpl`
   - `README.md.tmpl`
   - `agent.md.tmpl`
   - `SKILL.md.tmpl`
   - `SKILL-tick.md.tmpl`
   - `NORTHSTAR.md.tmpl` `CONTRACT.md.tmpl` `AUTONOMY.md.tmpl` `COLLAB.md.tmpl`
   - `command.md.tmpl` `command-tick.md.tmpl`
   - `ctl.sh.tmpl` `dispatch.py.tmpl` `verify_board.py.tmpl` `watch.sh.tmpl`
   - `workflow.rhai.tmpl` `workflow-tick.rhai.tmpl`
4. `scripts/`:
   - `ctl.sh` — `forge`, `selftest`, `from-hackers`, `sync`, `list-templates`
   - `forge.py` — reads lanes JSON + flags; renders templates; writes plugin+skills+workflows; syncs agents
   - `selftest.py` — validates a named team pack exists + scripts executable + rhai present
   - `from_hackers.py` — prints/extracts checklist of files from ha-hackers
5. `examples/lanes-pumapay.json` and `examples/lanes-sentinel.json` and `examples/lanes-minimal.json`

### B. Workflow
`~/.grok/workflows/ha-team-forge.rhai` — phases per AUTONOMY; args: name, prefix, purpose, lanes_json path or inline, mode, tick bool.
Smoke-ready: validate_only should compile.

### C. Plugin mirror
Copy skill into `~/.grok/plugins/ha-team-forge/skills/ha-team-forge/` (same content).
`commands/ha-team-forge.md`
`PLUGIN.md` `README.md`
`agents/forge-lead.md` (optional single agent that runs forge.py when workflow spawns it)

### D. Command
`~/.grok/plugins/ha-team-forge/commands/ha-team-forge.md` and ensure skill documents `/ha-team-forge`.

### E. Prove
```
bash ~/.grok/skills/ha-team-forge/scripts/ctl.sh selftest --name ha-team-forge
# dry-run forge minimal into /tmp or ~/Desktop/puma/docs/pumapay-v2/_forge-smoke/ha-smoke
bash ~/.grok/skills/ha-team-forge/scripts/ctl.sh forge \
  --name ha-smoke --prefix smk --mode team --tick 0 \
  --purpose "smoke team from forge" \
  --lanes ~/.grok/skills/ha-team-forge/examples/lanes-minimal.json \
  --plugin-root /tmp/ha-team-forge-smoke-plugins \
  --skills-root /tmp/ha-team-forge-smoke-skills \
  --agents-root /tmp/ha-team-forge-smoke-agents \
  --workflows-root /tmp/ha-team-forge-smoke-workflows
```
(Use temp roots for smoke so we don't pollute; document how to forge into real ~/.grok).

Return file list + selftest + smoke forge output.

NO nested agents. FINISH complete (no TODO stubs in ctl/forge).
