---
name: ha-hackers
description: Autonomous offensive team. Routes /docs vs host-map, then runs the matching workflow.
---

Run the conductor (`/ha-auto`). Do not spawn the five lanes by hand. Do not nested grok -p.

1. Need TARGET + OUT. Default PROXY `socks5h://127.0.0.1:10808`. TOKEN_FILE if the pack is ha-hackers.
2. `python3 ~/.grok/skills/ha-hackers/scripts/dispatch.py plan --target TARGET --out OUT --pack auto --proxy PROXY [--token-file TOKEN]`
3. Launch the workflow named in `OUT/.bus/PLAN.json` (`docs-entry` or `ha-hackers`).
4. Exploit only after disk `go_count > 0`. Money-write only if the operator set `allow_money_write` and resumed the pause.
