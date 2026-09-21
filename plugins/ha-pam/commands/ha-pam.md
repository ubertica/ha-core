---
name: ha-pam
description: PAM (Privileged Access Management) team for PumaPay staff-os and platform: access reviews, JIT grants, credential rotation, breakglass, over-privilege detection and audit evidence. Same gold quality as ha-hackers and ha-sec: full agents (pam-audit etc), contracts, autonomy, bus integration with sec/sre/backoffice, selftest.. Runs full lanes via workflow or tick.
---

Run the conductor. Do not spawn lanes by hand. Do not nested grok -p.

1. OUT absolute (default from env or ~/Desktop/puma/docs/ha-pam or similar)
2. `bash ~/.grok/skills/ha-pam/scripts/ctl.sh auto --out OUT [--lanes ...]`
3. Launch `workflow name=ha-pam args.out=OUT args.lanes=...`
4. Optional: watch with `ctl.sh watch --out OUT`
5. Tick mode for periodic remainder: `ctl.sh tick --out OUT` then ha-pam-tick workflow.

Always runs lead + sync on tick. Skips READY lanes with on-disk artifacts.
