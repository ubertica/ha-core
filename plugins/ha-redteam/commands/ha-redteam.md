---
name: ha-redteam
description: Party civil red-team. Deep audits/tests, propose fixes, document, Jira. Do not spawn 4 TUIs.
---

Run the conductor. Do not spawn lanes by hand. Do not nested grok -p.

1. TARGET + OUT absolute (default `/Users/c/dev/dani/out/redteam`). PROXY AMS SOCKS.
2. `bash ~/.grok/skills/ha-redteam/scripts/ctl.sh auto --target TARGET --out OUT`
3. Launch `workflow name=ha-redteam` with those args.
4. Party brains: `party_ask` g2-surface / g3-weapon / g4-adversary. g1 executes.
5. `/docs` → docs-entry pack into `entry/`.
6. After VERIFY: `ctl.sh jira-sync --out OUT` (skip `HA_JIRA_DISABLE=1`).
7. Tick: `ctl.sh tick --out OUT` then workflow `ha-redteam-tick`.
