# COLLAB — ha-release

Shared bus for cross-team collab (e.g. with ha-pumapay / ha-sentinel).

Bus root: `~/.grok/ha-release-bus/` or `~/.grok/ha-release-bus/`

Use `bus_append.py` or ctl `bus-append` to append JSONL notes.

Lanes coordinate via OUT/.bus/READY.* inside per-run OUT, and shared bus for inter-team.

See CONTRACT.md for bus wiring.
