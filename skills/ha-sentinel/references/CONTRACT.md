# CONTRACT — ha-sentinel (all lanes)

Parent passes: `OUT` (absolute, default `~/Desktop/puma/docs/pumapay-v2/sentinel`), `AMS=ams`, optional `TICK=0|1`.

## Access

- Tools: full. MCP: `mcpInheritance: all`.
- HA + infra-ops-comms nuclear inherited.
- SSH host alias `ams`. Prefer `ctl.sh` wrappers over raw ad-hoc.
- No nested spawn. No money-write.

## Roster

| Agent | Artifact | READY |
|-------|----------|-------|
| `sent-lead` | `OUT/SUMMARY.md` | `READY.lead` |
| `sent-watch` | `OUT/perimeter.md` + copy of AMS last | `READY.watch` |
| `sent-ollama` | `OUT/ollama.md` + ask/response | `READY.ollama` |
| `sent-audit` | `OUT/audit.md` | `READY.audit` |
| `sent-improve` | `OUT/improve.md` | `READY.improve` |
| `sent-release` | `OUT/release.md` | `READY.release` |
| `sent-escalate` | `OUT/escalations.md` + bus append | `READY.escalate` |
| `sent-collab` | `OUT/collab.md` + pumapay-bus | `READY.collab` |

## AMS anchors (do not invent)

- `/opt/ha-live/runtime/sentinel_god.py`
- `/opt/ha-live/runtime/sentinel_ollama.py`
- `/opt/ha-live/runtime/ha-live-sentinel.service`
- `/opt/ollama-ha/` + model `ha-sentinel`
- Evidence dirs under `/opt/ha-live/bus/evidence/`
- `bash /opt/ha-live/scripts/ctl.sh sentinel|ollama|ollama-ask "..."`

## Interconnect

1. Mac `OUT/.bus/` READY + notes.
2. Pull AMS evidence via SSH into `OUT/ams-mirror/`.
3. Shared `~/.grok/pumapay-bus/` (COLLAB.md).
4. Workflows `ha-sentinel.rhai`, `ha-sentinel-tick.rhai`.
5. Escalate severity high/crit → `sentinel-to-pumapay.jsonl` + board.jsonl.

## Invariants

- Grok HA = conductor; Ollama = watcher.
- Tick does not restart units unless operator `--repair`.
- Redact secrets from CREDS.json / HA env in chat.
