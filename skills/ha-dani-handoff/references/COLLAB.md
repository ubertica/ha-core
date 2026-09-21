# COLLAB — ha-dani-handoff

Per-run bus: `$OUT/.bus/` (READY.*, PLAN.json, NEXT.json, VERIFY.json, CIVIL.json, notes.jsonl).

Shared Daniel bus: `~/.grok/ha-dani-bus/`
- `domain-events.jsonl` (append-only; never truncate)
- `teams/ha-dani-handoff.jsonl`

Peer packs: `ha-dani-audit`, `ha-dani-authz`, `ha-dani-ops`
Conductor: `ha-dani`
Product overlay (do not impersonate as legacy owners): `ha-pumapay` `ha-ppdev` `ha-sec` `ha-sre` `ha-sentinel`

Escalate:
- Authz closure tickets → `ha-sec` / `ha-ppdev` (not ha-hackers)
- Infra down → `ha-sentinel` / `ha-sre`
- Daniel-facing wording → `ha-dani-audit` report lane

No nested grok. No PII on the bus.
