---
name: ha-orch
description: In a HA TUI session, orch is natural language. Do the work here (or EA sidecar, or background queue). Guard nested Grok spend. Never dump ha orch CLI flags unless the operator asked for the daemon.
---

# HA orch — the TUI is the UI

Operator is in `grok --hard-allow`. They talk. You route. No `--engine`, no PM2 lecture.

Spend law: this session already burns Grok. Nested `agent -p` burns **another** Grok + Mac RAM. Do not spawn it from here.

Caps live in `~/.grok/hard-allow/orch/CONTEXT.md`.

## Route (this turn)

| They said roughly | You do |
|---|---|
| Just the task | Do it **here** (Grok tools). No nested grok. |
| “EA”, rápido, enclave, privado, comprimí, título, extraé JSON | ExpressAI this turn: `node` `expressai-tui` `fast`. Stay on grok-4.6. |
| “dejalo corriendo”, background, cuando cierre el chat, overnight | Enqueue internally (`ha-orch.mjs add --engine auto --order "…"`). One line: quedó en cola. |
| está corriendo / se trabó / pará el fondo | Read `orch/health.json` or run watchdog `--once`. Report heartbeat / reclaimed. Not a CLI tutorial. |
| Claude / Kimi | No. Grok or EA only until those planes work. |

Do **not** tell them to type `ha orch add --engine ea`. You type that internally if needed.

## Guard (you already have this)

Worker: one job at a time, `--max-turns 6`, 180s, heartbeat.
Watchdog: stall 45s / TTL 4min / orphan nested Grok kill / never TUI.
Daily: 12 nested Grok jobs. Cap → EA for auto, fail for explicit grok.
Result stub (`[sync] OK`, empty, “I'll do it”) = **failed**.

## EA from this session (no MCP required)

```
cd /Users/c/dev/expressai-tui && node bin/expressai.mjs fast transform -i "…"
```

Cookie: `~/.expressai/cookie` (Mac PWA). If 401, say “reabrí la app ExpressAI”.

## Daemon (only if they ask “está el worker?”)

`ha orch status` — worker `ha-orch-grok` + watchdog `ha-orch-watchdog`. Not the product surface.
