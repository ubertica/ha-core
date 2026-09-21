# AUTONOMY — ha-pumapay

Parent does **not** pick lanes by taste. `dispatch.py` + workflows do.

## Default

```
bash ~/.grok/skills/ha-pumapay/scripts/ctl.sh auto \
  --out "${PUMAPAY_OUT:-$HOME/Desktop/puma/docs/pumapay-v2}"
# then workflow name=ha-pumapay
```

Periodic:

```
bash ~/.grok/skills/ha-pumapay/scripts/ctl.sh tick --out "$OUT"
# then workflow name=ha-pumapay-tick
```

## Phases (full)

1. **Preflight** — mkdir OUT/.bus + pumapay-bus; copy COLLAB; optional sentinel status peek.
2. **Docs∥PM** — structure + backlog (parallel).
3. **QA∥Test** — plan + run/report (parallel when REPO set).
4. **Dev∥Repo** — changes + repo status (parallel).
5. **Sync** — read sentinel bus, write jira/repo events, READY.sync.
6. **Lead** — SUMMARY + BOARD always.

## Tick (periodic)

Remainder only: `dispatch.py remainder` → skip READY → run missing + always `pp-sync` + `pp-lead`.

## Watcher stdout

Only: `DONE` | `FAILED` | `ACTION_REQUIRED: spawn <lanes>`

## Banned

Nested `grok -p`. Peer spawn. Inventing Jira keys without writing BACKLOG evidence.
