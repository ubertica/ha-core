# ha-ppdev

Reusable fintech team. Canonical live copies:

- Agents: `~/.grok/agents/ppd-*.md` (includes `ppd-lead`)
- Skill: `~/.grok/skills/ha-ppdev/`
- Workflow: `~/.grok/workflows/ha-ppdev.rhai`
- Conductor: `~/.grok/skills/ha-ppdev/references/AUTONOMY.md` + `scripts/ctl.sh`

This folder is the marketplace mirror. Sync from those paths.

Purpose: PumaPay Platform Dev: greenfield API+backend monorepo. OpenAPI-first, ledger/wallet core, auth, workers, DB, tests, tooling. Implements contracts from domain teams; does not redefine business rules alone. Conductor grok-4.6; volume grok-build.
