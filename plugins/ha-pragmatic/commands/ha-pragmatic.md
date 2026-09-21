---
name: ha-pragmatic
description: iGaming team specialized in Pragmatic Play Integration API v3.233 (July 2025 PDF): Seamless Wallet vs Balance Transfer, CasinoGameAPI, MD5 hash, Free Spins/Chips, history/datafeeds, PP Live BO. Spec-first. Staging default. IP whitelist. Never invent GO. No live money without operator flag.. Runs full lanes via workflow or tick.
---

Run the conductor. Do not spawn lanes by hand. Do not nested grok -p.

1. OUT absolute (default from env or ~/Desktop/puma/docs/ha-pragmatic or similar)
2. `bash ~/.grok/skills/ha-pragmatic/scripts/ctl.sh auto --out OUT [--lanes ...]`
3. Launch `workflow name=ha-pragmatic args.out=OUT args.lanes=...`
4. Optional: watch with `ctl.sh watch --out OUT`
5. Tick mode for periodic remainder: `ctl.sh tick --out OUT` then ha-pragmatic-tick workflow.

Always runs lead + sync on tick. Skips READY lanes with on-disk artifacts.
