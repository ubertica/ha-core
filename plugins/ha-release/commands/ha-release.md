---
name: ha-release
description: PumaPay release train go/no-go.. Runs full lanes via workflow or tick.
---

Run the conductor. Do not spawn lanes by hand. Do not nested grok -p.

1. OUT absolute (default from env or ~/Desktop/puma/docs/ha-release or similar)
2. `bash ~/.grok/skills/ha-release/scripts/ctl.sh auto --out OUT [--lanes ...]`
3. Launch `workflow name=ha-release args.out=OUT args.lanes=...`
4. Optional: watch with `ctl.sh watch --out OUT`
5. Tick mode for periodic remainder: `ctl.sh tick --out OUT` then ha-release-tick workflow.

Always runs lead + sync on tick. Skips READY lanes with on-disk artifacts.
