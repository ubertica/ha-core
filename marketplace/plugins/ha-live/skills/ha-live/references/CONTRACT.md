# Build contract (this repo)

The **build session** (new Grok 4.6 + HA, cwd `/Users/c/dev/ha-live`, paste `PROMPT.md`) ships a **working runtime**, not docs about a runtime.

Recipe: `BUILD.md`. Source already in `runtime/` + `scripts/`. Deploy + prove; do not replace the architecture.

## doneWhen (all must be true)

1. **`ssh ams` has `/opt/ha-live`** with `bus/`, `runtime/`, `logs/` and a process that stays up if the Mac sleeps (systemd `ha-live.service` — fallback in BUILD.md). Prove with `systemctl is-active ha-live` or `pgrep` after start.
2. **Bus** on AMS: append-only jsonl that a worker can write and another can read **without** the Mac TUI. Schema: `BUS.md` (`{ts, from, type, host, next, evidence, msg}`).
3. **Ctl on Mac:** `scripts/ctl.sh status|start|stop|push|pull|ping` talks to AMS. `status` prints process + last bus line. No nested `grok -p`.
4. **Pivot default:** a blocked/empty next on the bus opens a **third-party / next-host** work item (not `DONE`). Code in `runtime/remainder.py`, not a comment.
5. **Egress:** workers that touch non-localhost use SOCKS **on the host that egresses**. Fail closed if that proxy is down (exit non-zero + bus line). Helper: `runtime/egress.py`.
6. **One live proof:** `bash scripts/prove.sh`. Disk evidence in `proof/` (commands + stdout). That is the gate. Not a diagram.
7. **HA inherit:** AMS process sees `GROK_HARD_ALLOW_ACTIVE` / token if the operator’s env can be forwarded into `/opt/ha-live/runtime/ha.env` (mode 600). If not, HOLD + exact missing secret in `proof/HA-INHERIT.md` — do not fake HA on AMS; still start the process.
8. Money-write still gated unless the operator named it **in that run**.

## HOLD is allowed

If SSH to AMS fails, proxy is down, or token cannot be forwarded: **HOLD** in `proof/BLOCKER.md` with the command that failed. Do not invent a local-only “daemon” and call it AMS.

## Out of scope for v0 (do not fake)

- 700 agents, ExploitGym leaderboard, Kimi hive, autonomy-core tick, 754 capabilities.
- A full pentest of a random host (Puma is not this project).
- A second HA ceremony on AMS.
