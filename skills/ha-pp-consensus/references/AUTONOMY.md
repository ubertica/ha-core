# AUTONOMY — ha-pp-consensus

Parent does **not** pick lanes by taste. `consensus.py` + workflows do.

## Default

```
bash ~/.grok/skills/ha-pp-consensus/scripts/ctl.sh propose --id <proposal-id>
bash ~/.grok/skills/ha-pp-consensus/scripts/ctl.sh auto --id <proposal-id>
# then workflow name=ha-pp-consensus
```

Status / verify never votes (tick mode).

## Phases (full)

1. **Preflight** — load proposal from bus, ensure pp-docs + ppd-arch agents.
2. **Parallel review** — pp-docs (spec) ∥ ppd-arch (impl).
3. **Gate** — ACK×2 → decision, else HOLD/REVISE.
4. **Sync** — write decisions/ + consensus.jsonl + board.
5. **Lead** — note in COLLAB / domain-events.

Conductor **must not** solo-ACK both sides.
