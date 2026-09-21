---
name: ha-dani-authz
description: Post-incident BOLA/CORS/docs closure for PumaPay/gplaygap. Verify CLOSED only. Never harvest. HOLD live money and live gplaygap patch. Runs full lanes via workflow or tick. Civil.
---

Run the conductor. Do not spawn lanes by hand. Do not nested grok -p.
Read `~/.grok/agents/_ha-dani-law.md` first.

1. OUT absolute (default `/Users/c/dev/dani/out/authz`)
2. `bash ~/.grok/skills/ha-dani-authz/scripts/ctl.sh auto --out OUT`
3. Launch `workflow name=ha-dani-authz args.out=OUT`
4. Optional: `ctl.sh watch --out OUT`
5. Tick: `ctl.sh tick --out OUT` then `ha-dani-authz-tick` workflow.

Always runs lead + sync on tick. Skips READY lanes with on-disk artifacts.
Never loot. Never live money. Never live gplaygap patch.
