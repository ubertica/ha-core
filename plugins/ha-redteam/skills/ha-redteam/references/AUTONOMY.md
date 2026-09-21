# AUTONOMY — ha-redteam

## Default (g1 conductor)

1. `party_who`. Offline g3 → g4 dual. Do not invent seats.
2. `ctl.sh auto --target T --out O --proxy P`
3. Workflow `ha-redteam` **or** remainder loop below. Do not hand-spawn lanes unless workflow down.
4. Brains: `party_ask` with playbooks (`g2-surface`, `g3-weapon`, `g4-adversary`). g1 executes tools.
5. `/docs` TARGET → `python3 ~/.grok/skills/ha-hackers/scripts/dispatch.py plan --pack docs-entry` then workflow `docs-entry`. Feed artifacts into `entry/`.
6. Probe failures → ACT (`ha-correction-loops`): max 5 attempts / 3 auto-fixes then HOLD.
7. `verify_board.py` (fail-closed on missing artifacts; `go_count` from FINDINGS.jsonl).
8. `ctl.sh jira-sync --out O` unless `HA_JIRA_DISABLE=1`.
9. `ctl.sh layers` every cycle (memory → radio → jump → intel).
10. g1 honors SPAWN_REQUEST (depth 1, max 8). Child writes another request — does not spawn.
11. `rdt-lead` writes SUMMARY+BOARD. g4 OBJECTIVE_POLL; unanimous YES+evidence = stop.

## Remainder (tick)

Skip `OUT/.bus/READY.<lane>` + artifact on disk. Always run **sync, jira, lead, radio, memory** + `ctl.sh layers`.

## Bend vs HOLD

`ctl.sh charter --text "…"` → UNBREAKABLE=HOLD else GO-bend. See CHARTER.md.

## ha-core

Use KEEP_CORE: ralph-loop for long runs, SDD for independent lane work, TDD before probe code, verification-before-completion, verify-subagent-file-output-on-disk. Do not claim READY if the file is missing.

## Banned

Nested `grok -p`. Four Grok TUIs. Claiming GO from `ready_count`. Live patch. Loot in OUT.
