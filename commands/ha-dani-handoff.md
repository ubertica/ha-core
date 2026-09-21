---
name: ha-dani-handoff
description: Handoff-debt map after 10+ developers: owners, orphans, unified-bucket, Staff OS notes. Human-readable. No secrets. Runs full lanes via workflow or tick. Civil.
---

Run the conductor. Do not spawn lanes by hand. Do not nested grok -p.
Read `~/.grok/agents/_ha-dani-law.md` first.

1. OUT absolute (default `/Users/c/dev/dani/out/handoff`)
2. `bash ~/.grok/skills/ha-dani-handoff/scripts/ctl.sh auto --out OUT`
3. Launch `workflow name=ha-dani-handoff args.out=OUT`
4. Optional: `ctl.sh watch --out OUT`
5. Tick: `ctl.sh tick --out OUT` then `ha-dani-handoff-tick` workflow.

Always runs lead + sync on tick. Skips READY lanes with on-disk artifacts.
Never loot. Never live money. Never live gplaygap patch.
