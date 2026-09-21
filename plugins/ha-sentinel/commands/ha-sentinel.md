---
name: ha-sentinel
description: Sentinel team. Runs full watch∥ollama∥audit∥improve∥release∥escalate∥collab∥lead via workflow for AMS + Ollama protection.
---

Run the conductor. Do not spawn lanes by hand. Do not nested grok -p.

1. OUT absolute (default ~/Desktop/puma/docs/pumapay-v2/sentinel)
2. `bash ~/.grok/skills/ha-sentinel/scripts/ctl.sh auto --out OUT`
3. Launch `workflow name=ha-sentinel args.out=OUT`
4. Optional: watch with `ctl.sh watch --out OUT`
5. Tick mode: `ctl.sh tick --out OUT` then ha-sentinel-tick workflow.
6. AMS ops: `ctl.sh ams-mirror --out OUT` ; `ctl.sh ollama-ask "..."`

Always runs lead + collab/escalate on tick. Skips READY lanes with on-disk artifacts.
