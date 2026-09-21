# NORTHSTAR — ha-pam

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

Purpose: PAM (Privileged Access Management) team for PumaPay staff-os and platform: access reviews, JIT grants, credential rotation, breakglass, over-privilege detection and audit evidence. Same gold quality as ha-hackers and ha-sec: full agents (pam-audit etc), contracts, autonomy, bus integration with sec/sre/backoffice, selftest.
