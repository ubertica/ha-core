---
name: ha-live-engage
description: Bridge a board id to ha-hackers (fail-closed on AMS proxy HOLD).
---

Cwd `/Users/c/dev/ha-live`.

```bash
bash scripts/engage.sh <board-id>
```

If it prints `ENGAGE_OK`, launch workflow `ha-hackers` with the printed `target` and `out`. If exit 2, stay on the board (HOLD) — do not curl the host from the Mac.
