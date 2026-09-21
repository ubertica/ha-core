---
name: ha-ppdev
description: PumaPay Platform Dev: greenfield API+backend monorepo. OpenAPI-first, ledger/wallet core, auth, workers, DB, tests, tooling. Implements contracts from domain teams; does not redefine business rules alone. Conductor grok-4.6; volume grok-build.. Runs full lanes via workflow or tick.
---

Run the conductor. Do not spawn lanes by hand. Do not nested grok -p.

1. OUT absolute (default from env or ~/Desktop/puma/docs/ha-ppdev or similar)
2. `bash ~/.grok/skills/ha-ppdev/scripts/ctl.sh auto --out OUT [--lanes ...]`
3. Launch `workflow name=ha-ppdev args.out=OUT args.lanes=...`
4. Optional: watch with `ctl.sh watch --out OUT`
5. Tick mode for periodic remainder: `ctl.sh tick --out OUT` then ha-ppdev-tick workflow.

Always runs lead + sync on tick. Skips READY lanes with on-disk artifacts.
