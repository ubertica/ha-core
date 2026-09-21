# NORTHSTAR — ha-marketing

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

Secondary gold: `ha-pumapay`, `ha-sentinel` (product + ops variants of the same shape).

## Non-goals

- Not inventing a new orchestration runtime.
- Not replacing `create-skill` / `create-workflow` bundled skills — this **composes** them into a team pack.
- No theater: selftest must pass or HOLD with blocker.

Purpose: Marketing team for PumaPay v2: full growth stack — acquisition campaigns, content & messaging, SEO/SEM/affiliates, analytics & attribution, creative production, brand safety and offer compliance. HA quality matching ha-hackers: agent roster, workflows, bus collab with product/support/risk, selftest PASS, NORTHSTAR ownership of growth KPIs.
