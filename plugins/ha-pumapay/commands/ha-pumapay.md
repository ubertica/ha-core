---
name: ha-pumapay
description: PumaPay v2 product team. Runs full docs∥pm∥qa∥test∥dev∥repo∥sync∥lead via workflow.
---

Run the conductor. Do not spawn lanes by hand. Do not nested grok -p.

1. OUT absolute (default ~/Desktop/puma/docs/pumapay-v2)
2. `bash ~/.grok/skills/ha-pumapay/scripts/ctl.sh auto --out OUT`
3. Launch `workflow name=ha-pumapay args.out=OUT`
4. Optional: watch with `ctl.sh watch --out OUT`
5. Tick mode for periodic remainder: `ctl.sh tick --out OUT` then ha-pumapay-tick workflow.

Always runs lead + sync on tick. Skips READY lanes with on-disk artifacts.
