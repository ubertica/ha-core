# COLLAB — ha-marketing

Shared bus for cross-team collab (e.g. with ha-pumapay / ha-sentinel).

Bus root: `~/.grok/ha-marketing-bus/` or `~/.grok/ha-marketing-bus/`

Use `bus_append.py` or ctl `bus-append` to append JSONL notes.

Lanes coordinate via OUT/.bus/READY.* inside per-run OUT, and shared bus for inter-team.

See CONTRACT.md for bus wiring.
