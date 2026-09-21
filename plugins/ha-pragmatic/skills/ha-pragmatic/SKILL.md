---
name: ha-pragmatic
description: >
  iGaming team specialized in Pragmatic Play Integration API v3.233 (July 2025 PDF): Seamless Wallet vs Balance Transfer, CasinoGameAPI, MD5 hash, Free Spins/Chips, history/datafeeds, PP Live BO. Spec-first. Staging default. IP whitelist. Never invent GO. No live money without operator flag. Use when creating a new team, forging a plugin+agents pack, /ha-pragmatic, or "como ha-hackers pero para ha-pragmatic".
---

# ha-pragmatic

Canonical references: `references/{NORTHSTAR,CONTRACT,AUTONOMY}.md`  
Gold: `~/.grok/plugins/ha-hackers/`  
Build checklist: `BUILD-SPEC.md`

## Quick use

```bash
bash ~/.grok/skills/ha-pragmatic/scripts/ctl.sh forge \
  --name ha-pragmatic --prefix pra --mode team --tick 1 \
  --purpose "iGaming team specialized in Pragmatic Play Integration API v3.233 (July 2025 PDF): Seamless Wallet vs Balance Transfer, CasinoGameAPI, MD5 hash, Free Spins/Chips, history/datafeeds, PP Live BO. Spec-first. Staging default. IP whitelist. Never invent GO. No live money without operator flag." \
  --lanes ~/.grok/skills/ha-team-forge/examples/lanes-pragmatic.json
```

Or workflow: `/ha-pragmatic` / `workflow name=ha-team-forge` with args.

## Modes

`team` (default) · `plugin` · `agents` · `tick`

## Conductor rule

Parent writes/approves brief → forge scripts render templates → `selftest` → DONE.  
Volume file gen may use `grok-build` workers; design stays on grok-4.6.
