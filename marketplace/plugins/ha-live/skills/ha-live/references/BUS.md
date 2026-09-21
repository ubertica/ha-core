# Bus

Source of truth: **AMS** `/opt/ha-live/bus/`. Mac `proof/from-ams/bus/` is a pull mirror.

## Files

| File | Role |
|------|------|
| `events.jsonl` | append-only heartbeat / ping / fail-closed / errors |
| `work.jsonl` | append-only work items (findings, pivots, next hosts) |
| `board.jsonl` | **work board** workers actually use (HF shape). `id` + `status` + `goal`. Last line per `id` wins. See `BOARD.md` |
| `evidence/` | files `evidence` fields point at. Paths must exist |

Do not rewrite history. Rotate later if a file exceeds ~100MB (`mv` to `events.jsonl.<utc>` and continue).

## Line schema (every line)

JSON object, one per line, UTF-8, no pretty-print.

```json
{
  "ts": "2026-09-11T12:00:00+00:00",
  "from": "remainder|ctl|ha-live-builder|<worker-id>",
  "type": "start|heartbeat|ping|pivot|blocked|empty|finding|poc|fail|fail-closed|error|claim",
  "host": "hostname or target host",
  "next": "third-party|null|a host|a path",
  "evidence": "absolute path or null",
  "msg": "short human line"
}
```

Extra keys are allowed. Those seven are required (use JSON `null` not omitted).

## Invariants

- A worker on AMS must be able to `echo '{...}' >> /opt/ha-live/bus/events.jsonl` **and** `board.jsonl` **without** the Mac TUI. Helper: `python3 /opt/ha-live/runtime/board.py`.
- `type=done` is forbidden as the reaction to an empty/blocked `next`. Use `pivot`.
- `evidence` is a path that exists, or null. Never a prose claim.
- Do not log `SECOPS_HARD_ALLOW_TOKEN` or raw JWTs.

## Types the remainder emits

| type | when |
|------|------|
| `start` | process boot |
| `heartbeat` | each tick |
| `pivot` | last work blocked/empty → opened next-host item |
| `fail-closed` | AMS proxy down; no egress that tick |
| `error` | exception in the loop |
| `ping` | `ctl ping` / `remainder.py --ping` |
