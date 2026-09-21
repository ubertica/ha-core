---
name: ha-fraud
description: Fraud Prevention team for PumaPay: velocity/device/behavioral detection, fraud rules, case management, scoring integration, chargeback defense and loss prevention. Matches ha-hackers operating model, NORTHSTAR/CONTRACT/AUTONOMY, full agent roster, bus sync to AML/ledger/payments. Selftest required.. Runs full lanes via workflow or tick.
---

Run the conductor. Do not spawn lanes by hand. Do not nested grok -p.

1. OUT absolute (default from env or ~/Desktop/puma/docs/ha-fraud or similar)
2. `bash ~/.grok/skills/ha-fraud/scripts/ctl.sh auto --out OUT [--lanes ...]`
3. Launch `workflow name=ha-fraud args.out=OUT args.lanes=...`
4. Optional: watch with `ctl.sh watch --out OUT`
5. Tick mode for periodic remainder: `ctl.sh tick --out OUT` then ha-fraud-tick workflow.

Always runs lead + sync on tick. Skips READY lanes with on-disk artifacts.
