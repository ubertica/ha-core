---
name: ha-ledger
description: PumaPay ledger: double-entry, holds, recon, settlement.. Runs full lanes via workflow or tick.
---

Run the conductor. Do not spawn lanes by hand. Do not nested grok -p.

1. OUT absolute (default from env or ~/Desktop/puma/docs/ha-ledger or similar)
2. `bash ~/.grok/skills/ha-ledger/scripts/ctl.sh auto --out OUT [--lanes ...]`
3. Launch `workflow name=ha-ledger args.out=OUT args.lanes=...`
4. Optional: watch with `ctl.sh watch --out OUT`
5. Tick mode for periodic remainder: `ctl.sh tick --out OUT` then ha-ledger-tick workflow.

Always runs lead + sync on tick. Skips READY lanes with on-disk artifacts.
