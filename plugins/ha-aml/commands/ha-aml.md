---
name: ha-aml
description: AML team for PumaPay v2 fintech: transaction monitoring, investigations, SAR/STR filing, customer risk rating, rule tuning and regulatory reporting. Full HA autonomy, bus collab with fraud/risk/support, selftest PASS. Same structure and quality as ha-hackers and ha-risk.. Runs full lanes via workflow or tick.
---

Run the conductor. Do not spawn lanes by hand. Do not nested grok -p.

1. OUT absolute (default from env or ~/Desktop/puma/docs/ha-aml or similar)
2. `bash ~/.grok/skills/ha-aml/scripts/ctl.sh auto --out OUT [--lanes ...]`
3. Launch `workflow name=ha-aml args.out=OUT args.lanes=...`
4. Optional: watch with `ctl.sh watch --out OUT`
5. Tick mode for periodic remainder: `ctl.sh tick --out OUT` then ha-aml-tick workflow.

Always runs lead + sync on tick. Skips READY lanes with on-disk artifacts.
