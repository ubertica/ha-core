# BUILD — v0 recipe

Do **not** invent a different architecture. Deploy this. Prove it. HOLD if a cable is dead.

## Order

1. `bash scripts/preflight.sh` — HA shell (warn), Mac SOCKS, `ssh ams` mkdir, AMS SOCKS probe, docs present.
2. Confirm `runtime/remainder.py` `runtime/egress.py` `runtime/ha-live.service` exist (they should). Edit only to fix a real AMS path (`python3`, systemd vs nohup).
3. `bash scripts/ctl.sh push`
4. `bash scripts/ctl.sh start` — rsync runtime, write `ha.env` mode 600, install unit, enable --now.
5. `bash scripts/prove.sh` — ping + status saved under `proof/`.
6. If any step fails: `proof/BLOCKER.md` with the **exact** command and stdout. Do not declare AMS live from a Mac-only loop.

## Layout after start

```
Mac  /Users/c/dev/ha-live/
  runtime/remainder.py      # source of truth
  runtime/egress.py
  runtime/ha-live.service
  scripts/ctl.sh preflight|status|start|stop|push|pull|ping
  scripts/prove.sh
  proof/                    # gate artifacts

AMS  /opt/ha-live/
  runtime/remainder.py
  runtime/egress.py
  runtime/ha-live.service
  runtime/ha.env            # GROK_HARD_ALLOW_ACTIVE, token, HA_PROXY, HA_LIVE_ROOT  mode 600
  bus/events.jsonl
  bus/work.jsonl
  logs/
```

systemd: `/etc/systemd/system/ha-live.service` copied from `runtime/ha-live.service`.

## Remainder (what the process does)

Every `HA_LIVE_TICK` seconds (default 15):

- append `heartbeat` to `events.jsonl`
- read last line of `work.jsonl`
- if missing / `next` empty / `type` in `{blocked,empty}` → append `pivot` work item (`host=next-host`, `next=third-party`) and a `pivot` event
- if AMS proxy down → `fail-closed` event, **no** non-localhost fetch that tick

`--once` one tick. `--ping` one ping event. `--status` prints last 5 events. Default: loop.

No money-write. No nested grok. No autonomy-core import.

## systemd vs nohup

AMS `/usr/bin/python3` is **3.6.9**. Keep `runtime/*.py` 3.6-compatible (no `from __future__ import annotations`, no `list[str]`). Prefer a newer python if `python3.8`/`python3.11` exists on PATH — only then change `ExecStart`. Default: 3.6.

Prefer systemd. If `systemctl` is missing or permission fails, fallback:

```bash
ssh ams 'nohup python3 /opt/ha-live/runtime/remainder.py >> /opt/ha-live/logs/remainder.out 2>> /opt/ha-live/logs/remainder.err & echo $! > /opt/ha-live/runtime/remainder.pid'
```

Document which one you wired in `proof/UNIT.md` (`systemd` or `nohup`). `ctl stop` must match.

## HA inherit

`ctl start` writes `/opt/ha-live/runtime/ha.env` from the **Mac process env**. Do not print the token. Mode 600.

If `GROK_HARD_ALLOW_ACTIVE` is not `1` in that shell: still start; write `proof/HA-INHERIT.md` with HOLD + “token not in this shell — TUI may still have it; re-run ctl start from a HA session”.

## SOCKS

See `SPLIT.md`. `egress.require_proxy()` uses `HA_PROXY` **on the host running the code**.

Preflight 2026-09-11: AMS `10808` down. xray listens `127.0.0.1:18082`; protocol unconfirmed. Do **not** copy Mac `HA_PROXY` onto AMS.

`ctl start` writes AMS `ha.env` `HA_PROXY` from `HA_AMS_PROXY` if set, else leaves a value that will fail-closed. After you prove a working AMS SOCKS:

```bash
HA_AMS_PROXY=socks5h://127.0.0.1:PORT ./scripts/ctl.sh start
```

If no AMS SOCKS works: HOLD third-party egress in `proof/BLOCKER.md`. Still start the remainder (heartbeat + pivot-on-block do not need egress).

## Proof gate

`scripts/prove.sh` must leave:

- `proof/prove.txt` — commands + stdout
- `proof/UNIT.md` — systemd or nohup
- last ping line visible in `ctl status`

Pass = process active AND a `type=ping` line on AMS `events.jsonl` from this run.

## What “done” looks like (print this)

```
ctl:     /Users/c/dev/ha-live/scripts/ctl.sh
unit:    ha-live.service  (or nohup pid file)
bus:     ams:/opt/ha-live/bus/events.jsonl
proof:   /Users/c/dev/ha-live/proof/prove.txt
```

## Out of scope (do not start)

ExploitGym, 700 agents, Kimi, cloning Terminaitor ticks, pentesting cwd, money-write, a second ceremony.
