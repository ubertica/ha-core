# NORTHSTAR — ha-release

**DONE** = from a short brief you can mint a full HA team (plugin + agents + skills + contracts + workflows + ctl) that matches the `ha-hackers` operating model and passes `ctl.sh selftest`.

## What “team” means here

A **team** is the whole pack, not one agent file:

| Layer | Paths |
|-------|--------|
| Plugin | `~/.grok/plugins/<name>/` (`plugin.json`, `PLUGIN.md`, `README.md`, `agents/`, `skills/`, `commands/`) |
| User agents | `~/.grok/agents/<prefix>-*.md` + `_ha-law.md` |
| User skills | `~/.grok/skills/<name>/` (+ optional `-tick`) |
| Workflows | `~/.grok/workflows/<name>.rhai` (+ optional `-tick.rhai`) |
| Personas/roles | optional `~/.grok/personas|roles/<prefix>-*.toml` |
| Bus | `OUT/.bus/READY.*` + optional shared `~/.grok/<name>-bus/` |

## Gold template

`~/.grok/plugins/ha-hackers/` — autonomy via scripts+workflow, disk evidence gate, no nested `grok -p`, HA baked into agents.

Secondary gold: `ha-pumapay`, `ha-sentinel` (product + ops variants of the same shape). Cross: release train with sec/sre/pam via bus.

## Non-goals

- Not inventing a new orchestration runtime.
- Not replacing `create-skill` / `create-workflow` bundled skills — this **composes** them into a team pack.
- No theater: selftest must pass or HOLD with blocker.

Purpose: PumaPay release train + go/no-go. Full HA autonomy, bus collab with sec/sre, selftest PASS. Same structure and quality as ha-hackers and ha-risk.

## OUT
docs/pumapay-v2/release

## Conductor
Parent grok-4.6. Volume lanes prefer grok-build (see AGENT-MODELS.md).
