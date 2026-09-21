# Work board (HF shape, not 700 agents)

Source of truth: **AMS** `/opt/ha-live/bus/board.jsonl` (append-only).
Mac mirror after `ctl pull`: `proof/from-ams/bus/board.jsonl`.

Hive = this file + `events.jsonl` + `work.jsonl`. Workers talk here, not via the parent chat.

## Without this TUI

On AMS:

```bash
echo '{"ts":"...","from":"worker","type":"finding","host":"…","next":"…","evidence":"/opt/ha-live/bus/evidence/…","msg":"…","id":"g-1","status":"open"}' >> /opt/ha-live/bus/board.jsonl
python3 /opt/ha-live/runtime/board.py tail
python3 /opt/ha-live/runtime/board.py open
python3 /opt/ha-live/runtime/board.py claim g-1 --by ha-live-runtime
```

From Mac:

```bash
bash scripts/board.sh status
bash scripts/board.sh open
bash scripts/ctl.sh board open
```

## Schema

`BUS.md` seven keys **plus**:

| extra | meaning |
|-------|---------|
| `id` | stable goal id (last line wins) |
| `status` | `open` `claimed` `blocked` `pivot` `finding` `fail` |
| `goal` | one-line next action |
| `claimed_by` | worker id |

`type=done` is forbidden as the reaction to empty/blocked next. Use `pivot`.

## P1

Remainder still writes `work.jsonl` `type=pivot` `host=next-host` when last work is blocked/empty.
A **Grok worker** must replace that placeholder from **evidence** (this board or `bus/evidence/`). Do not leave `next-host` as the live goal.

## OPSEC / money

Third-party only via proven AMS SOCKS (`HA_AMS_PROXY`). If HOLD: work first-party (AMS xray) or harvest disk evidence — never Mac ISP.
Money-write only if the operator named it **this run**.
