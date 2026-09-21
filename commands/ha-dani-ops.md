---
name: ha-dani-ops
description: Daniel infra ops: AMS danielcliente, dash, perimeter hosts. Read-only health. HOLD live patch and money-write. Runs full lanes via workflow or tick. Civil.
---

Run the conductor. Do not spawn lanes by hand. Do not nested grok -p.
Read `~/.grok/agents/_ha-dani-law.md` first.

1. OUT absolute (default `/Users/c/dev/dani/out/ops`)
2. `bash ~/.grok/skills/ha-dani-ops/scripts/ctl.sh auto --out OUT`
3. Launch `workflow name=ha-dani-ops args.out=OUT`
4. Optional: `ctl.sh watch --out OUT`
5. Tick: `ctl.sh tick --out OUT` then `ha-dani-ops-tick` workflow.

Always runs lead + sync on tick. Skips READY lanes with on-disk artifacts.
Never loot. Never live money. Never live gplaygap patch.
