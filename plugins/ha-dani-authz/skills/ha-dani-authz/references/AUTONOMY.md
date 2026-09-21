# AUTONOMY — ha-dani-authz

North star: `references/NORTHSTAR.md`. `DONE` is honest board + civil-clean OUT, not a fake GO.

Parent Grok does **not** pick lanes by taste. Scripts + workflows do.
There is **no extra LLM orchestrator**. Nested `grok -p` is banned.

Conductor:

1. `dispatch.py` — pack router + remainder (`NEXT.json`)
2. `verify_board.py` + `civil_scan.py` — fail-closed (`VERIFY.json`, `CIVIL.json`)
3. Workflow `ha-dani-authz` (or `ha-dani-authz-tick`) — skip READY, spawn remainder, then lead
4. `watch.sh` — stdout only `DONE` | `FAILED` | `ACTION_REQUIRED`
5. Human gate: Daniel/operator flag for any write; money-write remains HOLD

## Default dispatch

```
export HA_DANI_AUTHZ_OUT=/Users/c/dev/dani/out/authz
bash ~/.grok/skills/ha-dani-authz/scripts/ctl.sh auto --out "${HA_DANI_AUTHZ_OUT}"
# then: workflow name=ha-dani-authz args.out=$OUT
```

Do not spawn `dath-*` by hand unless the workflow tool is down.

## Invariants

| Check | Script | Fail |
|-------|--------|------|
| Remainder | `dispatch.py remainder` | skip READY+artifact |
| Civil OUT | `civil_scan.py` | JWT/loot/image/CBU dump → not ok |
| Board | `verify_board.py` | missing artifact → not ready |
| Money / live patch | `HOLD.md` (authz+ops required) | never lift without operator |

## Watcher

```
bash ~/.grok/skills/ha-dani-authz/scripts/ctl.sh watch --out "$OUT"
```

## Tests

```
bash ~/.grok/skills/ha-dani-authz/scripts/ctl.sh selftest
bash ~/.grok/skills/ha-dani-authz/scripts/ctl.sh verify --out "$OUT"
```

## Banned

Nested `grok -p`. Claiming CLOSED without denial evidence. Copying loot into OUT.
Defaulting to `~/Desktop/hack-out`. Routing Daniel work to ha-hackers.
