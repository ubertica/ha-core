# AUTONOMY — ha-sentinel

## Default

```
bash ~/.grok/skills/ha-sentinel/scripts/ctl.sh auto \
  --out "${SENTINEL_OUT:-$HOME/Desktop/puma/docs/pumapay-v2/sentinel}"
# workflow name=ha-sentinel
```

Periodic:

```
bash ~/.grok/skills/ha-sentinel/scripts/ctl.sh tick --out "$OUT"
# workflow name=ha-sentinel-tick
```

## Phases (full)

1. **Preflight** — SSH ams reachable; mirror evidence dirs; systemd active?
2. **Watch∥Audit** — perimeter + audit parallel.
3. **Ollama** — warmup/status + optional `ollama-ask` from inbox.
4. **Improve∥Release** — board HOLDs + kit/release notes (no unsafe deploy).
5. **Escalate∥Collab** — high/crit → pumapay-bus; collab digest.
6. **Lead** — SUMMARY always.

## Tick

Pull AMS last.* → refresh OUT → escalate if needed → collab → lead. Skip green READY unless `--force`.

## Repair (operator only)

`ctl.sh repair` may `systemctl restart ha-live-sentinel` / `ollama-start` on AMS — never from silent tick.

## Banned

Nested grok. Money-write. Mutating `/backoffice/tasks`. Truncating AMS jsonl.
