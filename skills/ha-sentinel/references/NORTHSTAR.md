# NORTHSTAR — ha-sentinel

**DONE** = AMS is watched forever by local Ollama + systemd sentinel; Grok HA is conductor; ha-pumapay gets actionable escalations; no theater.

## Product

Plugin face for the **already-live** AMS stack:

| Piece | AMS path |
|-------|----------|
| Loop | `/opt/ha-live/runtime/sentinel_god.py --loop` |
| Unit | `ha-live-sentinel.service` |
| Ollama | docker `ollama-ha` `127.0.0.1:11434` model `ha-sentinel` |
| Evidence | `/opt/ha-live/bus/evidence/sentinel-{god,ollama}/` |
| Ctl | `/opt/ha-live/scripts/ctl.sh` (`sentinel`, `ollama`, `ollama-ask`) |

Grok HA (Mac TUI) = conductor. Ollama = perpetual watcher/judgment. This plugin = team + workflows + Mac-side ctl that SSH to AMS.

## Non-goals

- Not replacing Grok as conductor.
- No nested `grok -p` from AMS.
- No money-write / backoffice mutate.
- Not a product PM pack (that is `ha-pumapay`) — we **feed** them via bus.

## Success predicates

1. `/ha-sentinel` and `/ha-sentinel-tick` dispatch.
2. Tick pulls AMS evidence + can `ollama-ask` + writes Mac OUT + shared bus.
3. Escalate high/crit → board note for grok-ha **and** `pp-sync` channel.
4. Coexists with ha-pumapay (COLLAB.md).
5. Idempotent READY / remainder.
