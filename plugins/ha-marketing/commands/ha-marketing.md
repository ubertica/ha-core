---
name: ha-marketing
description: Marketing team for PumaPay v2: full growth stack — acquisition campaigns, content & messaging, SEO/SEM/affiliates, analytics & attribution, creative production, brand safety and offer compliance. HA quality matching ha-hackers: agent roster, workflows, bus collab with product/support/risk, selftest PASS, NORTHSTAR ownership of growth KPIs.. Runs full lanes via workflow or tick.
---

Run the conductor. Do not spawn lanes by hand. Do not nested grok -p.

1. OUT absolute (default from env or ~/Desktop/puma/docs/ha-marketing or similar)
2. `bash ~/.grok/skills/ha-marketing/scripts/ctl.sh auto --out OUT [--lanes ...]`
3. Launch `workflow name=ha-marketing args.out=OUT args.lanes=...`
4. Optional: watch with `ctl.sh watch --out OUT`
5. Tick mode for periodic remainder: `ctl.sh tick --out OUT` then ha-marketing-tick workflow.

Always runs lead + sync on tick. Skips READY lanes with on-disk artifacts.
