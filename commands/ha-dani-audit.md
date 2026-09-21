---
name: ha-dani-audit
description: Periodic read-only code/MR/release audit for Daniel (PumaPay + aggregator + gaming). Coexistence model. No loot. No live writes. Runs full lanes via workflow or tick. Civil.
---

Run the conductor. Do not spawn lanes by hand. Do not nested grok -p.
Read `~/.grok/agents/_ha-dani-law.md` first.

1. OUT absolute (default `/Users/c/dev/dani/out/audit`)
2. `bash ~/.grok/skills/ha-dani-audit/scripts/ctl.sh auto --out OUT`
3. Launch `workflow name=ha-dani-audit args.out=OUT`
4. Optional: `ctl.sh watch --out OUT`
5. Tick: `ctl.sh tick --out OUT` then `ha-dani-audit-tick` workflow.

Always runs lead + sync on tick. Skips READY lanes with on-disk artifacts.
Never loot. Never live money. Never live gplaygap patch.
