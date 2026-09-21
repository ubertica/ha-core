---
name: ha-blackhat
description: Party (g1-g4) BLACKHAT red-team: docs-entry foothold, deep probe, exploit iff GO, loot in engagement OUT, killchain, ha-offense weapon. Layers jump/pivot/radio/intel/memory/spawn/learn. Not ha-dani civil. Not Puma Jira default.. Runs full lanes via workflow or tick.
---

Run the conductor. Do not spawn lanes by hand. Do not nested grok -p.

1. OUT absolute (default from env or ~/Desktop/puma/docs/ha-blackhat or similar)
2. `bash ~/.grok/skills/ha-blackhat/scripts/ctl.sh auto --out OUT [--lanes ...]`
3. Launch `workflow name=ha-blackhat args.out=OUT args.lanes=...`
4. Optional: watch with `ctl.sh watch --out OUT`
5. Tick mode for periodic remainder: `ctl.sh tick --out OUT` then ha-blackhat-tick workflow.

Always runs lead + sync on tick. Skips READY lanes with on-disk artifacts.
