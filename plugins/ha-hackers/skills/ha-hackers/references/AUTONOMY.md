# Conductor law (ha-hackers + docs-entry)

North star (HF-bar): `references/NORTHSTAR.md`. `DONE` is no open workstream, not merely empty READY remainder.

Parent Grok does **not** pick lanes by taste. Scripts + workflows do.

There is **no extra LLM orchestrator**. Nested `grok -p` is banned. The conductor is:

1. `dispatch.py` — pack router + remainder (`NEXT.json`)
2. `session_guard.py` — SOCKS + JWT TTL / 401
3. `verify_evidence.py` — fail-closed disk GO (`VERIFY.json`)
4. Workflow `ha-auto` (or pack-specific `docs-entry` / `ha-hackers`) — skip READY, spawn remainder
5. `watch.sh` — stdout only `DONE` | `FAILED` | `ACTION_REQUIRED: spawn <lanes>`
6. Human gate: `allow_money_write` only

## Default dispatch

```
python3 ~/.grok/skills/ha-hackers/scripts/ctl.sh auto \
  --target "$TARGET" --out "$OUT" --pack auto \
  --token-file "$TOKEN_FILE" --proxy "${HA_PROXY:-socks5h://127.0.0.1:10808}"
```

Then launch **workflow `ha-auto`** with those args. Do not spawn `hack-*` by hand unless the workflow tool is down. Do not nested `grok -p`.

`/docs` / swagger / openapi in TARGET → pack `docs-entry`. Else `ha-hackers`.

## Invariants (host, not prompt)

| Check | Script | Fail |
|-------|--------|------|
| SOCKS up | `session_guard.py --proxy` | exit 3 → `await_user` / ACTION_REQUIRED |
| JWT TTL (if `--need-token`) | same, Chrome refresh best-effort; `--probe-url` 401 | exit 2 → `TOKEN.stale` |
| GO / exploit | `verify_evidence.py` → `VERIFY.json` `go_count` | missing = 0 (fail closed) |
| Remainder | `dispatch.py remainder` → `NEXT.json` | skip any `READY.<lane>` |

docs-entry does **not** need a JWT. ha-hackers does.

Pack isolation: docs-entry only reads `OUT/docs-entry/*-findings.md` (never `ENTRY.md` / `FINDINGS.md` / root BOLA `authz-findings.md`). GO is unique by path.

docs-entry exploit/lead flags are **namespaced**: `READY.docs-exploit` / `READY.docs-lead`. `READY.exploit` from the other pack must not short-circuit.

## Money

`allow_money_write` default false. Workflow `await_user` if true. Lanes never POST deposit/withdraw/payout/approve unless that flag is on **and** the operator resumed. Unsigned webhook PoC uses dummy ids only — never dump uids.

## Watcher

```
bash ~/.grok/skills/ha-hackers/scripts/ctl.sh watch --out "$OUT" --pack docs-entry|ha-hackers
```

Stdout only: `DONE` | `FAILED` | `ACTION_REQUIRED`. On `spawn hack-exploit,hack-lead` the **parent TUI** `spawn_subagent` those types (or resume the workflow). Never nested Grok.

## Remainder / idempotent re-run

`dispatch.py remainder` lists `next` from READY + `go_count`. Re-running `ha-auto` skips lanes that already touched READY. Do not re-spray.

## Tests

```
python3 ~/.grok/skills/ha-hackers/scripts/ctl.sh selftest
```
