---
name: ha-live-tick
description: >
  USE THIS if two /ha-live-tick appear (the Command). One organism tick:
  snapshot AMS board, spawn P3 scout∥pivot∥learn, verify board.
  Not /ha-live-boot. Not prove.sh. Triggers: /ha-live-tick, hive cycle, successors.
---

# ha-live-tick

Cwd `/Users/c/dev/ha-live`. Model grok-4.6. Nested `grok -p` no.

If cwd is wrong: tell the operator to open the ha-live TUI (or `bash /Users/c/dev/ha-live/GO.sh`). Do not tick from Puma.

1. Read `CONTINUE.md` `BOARD.md` `proof/BLOCKER.md` `EMPOWER.md`.
2. Launch workflow **`ha-live-tick`** (user `~/.grok/workflows/ha-live-tick.rhai`).
3. After the tick: if `probe-ams-proxy.sh` is GO and a board id has a real host, parent may `bash scripts/engage.sh <id>` then `/ha-hackers` with that TARGET/OUT. Workflows cannot nest.

Do not redo `prove.sh` if `ctl status` shows active.

Board `evidence` must be AMS-canonical (`/opt/ha-live/bus/evidence/…`). Never `/Users/c/dev/ha-live/proof/…` — `verify_board.py` fail-closes on missing AMS files.
