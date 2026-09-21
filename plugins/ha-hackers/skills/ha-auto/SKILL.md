---
name: ha-auto
description: >
  Autonomous conductor for the hacker team. Routes /docs vs host-map,
  runs preflight (proxy/JWT), launches the matching workflow, gates
  exploit on disk evidence, skips READY lanes. Use when the operator
  says autónomo, agéntico, hacelo solo el pentest, /ha-auto, or wants
  the team to run without picking lanes by hand.
---

# ha-auto

Scripts: `~/.grok/skills/ha-hackers/scripts/` (`ctl.sh`, `dispatch.py`, `session_guard.py`, `verify_evidence.py`, `watch.sh`)  
Law: `~/.grok/skills/ha-hackers/references/AUTONOMY.md`  
Workflow: `~/.grok/workflows/ha-auto.rhai`

You are the parent conductor. Children cannot spawn children. No nested `grok -p`.

## Do this, in order

1. Resolve `TARGET`, `OUT` (absolute). Default proxy `socks5h://127.0.0.1:10808`. Optional `TOKEN_FILE`.
2. Plan + print launch line:

```
bash ~/.grok/skills/ha-hackers/scripts/ctl.sh auto \
  --target TARGET --out OUT --pack auto --proxy PROXY [--token-file TOKEN]
```

3. Launch workflow **`ha-auto`** with the same args (`workflow` tool, `name=ha-auto`). It skips READY lanes and only remainder-spawns.
4. Optional: `ctl.sh watch --out OUT --pack <pack>` (monitor). Wake only on DONE/FAILED/ACTION_REQUIRED.
5. On `ACTION_REQUIRED: spawn A,B` — `spawn_subagent` those types in this TUI. Do **not** nested grok.
6. Do **not** pick `hack-recon` / `hack-entry` yourself unless the workflow tool is down.

## Pack router

| TARGET looks like | Pack |
|-------------------|------|
| `/docs`, `/swagger`, `openapi`, `/api-docs` | `docs-entry` |
| anything else | `ha-hackers` |

Override: `args.pack`.

## Money

Do not pass `allow_money_write: true` unless the operator named a deposit/payout/approve test. The workflow will pause for resume if that flag is set.
