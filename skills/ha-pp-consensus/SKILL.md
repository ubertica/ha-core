---
name: ha-pp-consensus
description: >
  Consensus gate between ha-pumapay docs (pp-docs) and ha-ppdev (ppd-arch).
  Proposal → parallel review → ACK/NACK/REVISE → decision on disk.
  Use when /ha-pp-consensus, wave GO, CORE-SURFACE change, ADR freeze,
  or docs↔dev agreement required. Conductor must not solo-merge scope.
---

# ha-pp-consensus

Protocol: `~/.grok/pumapay-bus/consensus/CONSENSUS.md`  
Workflow: `~/.grok/workflows/ha-pp-consensus.rhai`  
Bus: `~/.grok/pumapay-bus/consensus/`

## Dispatch

```bash
# create or reuse proposal id
PROP=c-20260912-wave0-core
bash ~/.grok/skills/ha-pp-consensus/scripts/ctl.sh propose \
  --id "$PROP" \
  --title "Freeze Wave 0 CORE-SURFACE" \
  --paths "docs/api/CORE-SURFACE.md,docs/plans/DEV-PLAN.md"

bash ~/.grok/skills/ha-pp-consensus/scripts/ctl.sh auto --id "$PROP"
# then: workflow name=ha-pp-consensus args.id=$PROP
```

## Rules

1. Parent spawns only — no nested peer spawn.  
2. Both sides must vote on disk (`proposals/<id>.docs.json` + `.dev.json`).  
3. Decision file required before wave advance.  
4. Models: `pp-docs` + `ppd-arch` = **grok-4.6** (reasoning).  
5. HA profile: FINTECH-BUILD (same as product lanes).

## Verify

```bash
bash ~/.grok/skills/ha-pp-consensus/scripts/ctl.sh verify --id "$PROP"
```
