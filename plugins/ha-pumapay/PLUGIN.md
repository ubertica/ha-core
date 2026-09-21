# ha-pumapay

PumaPay v2 product team (docs, PM, QA, dev, repo, sync, lead). Collaborates with ha-sentinel via shared bus.

Canonical live copies:

- Agents: `~/.grok/agents/pp-*.md` (pp-lead, pp-docs, pp-pm, pp-qa, pp-test, pp-dev, pp-repo, pp-sync)
- Skills: `~/.grok/skills/ha-pumapay/` and `~/.grok/skills/ha-pumapay-tick/`
- Workflows: `~/.grok/workflows/ha-pumapay.rhai`, `ha-pumapay-tick.rhai`
- Conductor: `~/.grok/skills/ha-pumapay/scripts/ctl.sh auto|tick`
- References: `~/.grok/skills/ha-pumapay/references/{NORTHSTAR,CONTRACT,AUTONOMY}.md`
- Shared bus: `~/.grok/pumapay-bus/` (see COLLAB.md)
- Product tree: `~/Desktop/puma/docs/pumapay-v2/` (or $PUMAPAY_OUT)

This folder is the source mirror. Agents duplicated under plugin/agents/ and ~/.grok/agents/. Skills mirrored under ~/.grok/skills/.

Children inherit full parent MCP + tools. No nested spawn. Disk bus is source of truth.
