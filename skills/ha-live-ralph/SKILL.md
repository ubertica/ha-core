---
name: ha-live-ralph
description: >
  Keep running ha-live-tick in THIS TUI until the board is dry of first-party work or HOLD is explicit.
  Use when: /ha-live-ralph, keep going, overnight hive, until the board is quiet.
---

# ha-live-ralph

Cwd `/Users/c/dev/ha-live`. Nested `grok -p` no. Workflows cannot nest — **you** (parent) loop:

1. Launch workflow `ha-live-tick`.
2. `bash scripts/board.sh open` and `python3 runtime/verify_board.py --root /opt/ha-live` via ssh if needed.
3. If there is still an **open first-party** item (`egress-ams-*`) or a learn with missing evidence: run `ha-live-tick` again.
4. Stop when: two ticks in a row add no new board id, or operator said `cancelá`. Named DEST = GO (ha-live); do not stop on money-write when dest is named.
5. Third-party: only after `probe-ams-proxy.sh` GO **or** operator set `HA_AMS_PROXY=direct` (AMS IP visible). Then `/ha-live-engage <id>`.

Do not pick `/ha-live-boot`.
