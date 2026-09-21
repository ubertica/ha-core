---
name: ha-pumapay
description: >
  Dispatch the PumaPay v2 product team (pp-lead, pp-docs, pp-pm, pp-qa,
  pp-test, pp-dev, pp-repo, pp-sync) for docs, PM, QA, dev, repo hygiene.
  Use when the operator says /ha-pumapay, pumapay v2, product board, or
  wants parallel docs+pm+qa+test+dev+repo+sync+lead.
---

# ha-pumapay

Canonical: `~/.grok/agents/pp-*.md` · contract: `references/CONTRACT.md`  
Workflow: `~/.grok/workflows/ha-pumapay.rhai`

Parent = conductor. Children **cannot** spawn children (Grok depth 1).

## What each child actually gets

| Layer | How |
|-------|-----|
| Tools | Omit `tools:` in agent md → inherit **all** parent tools |
| MCP | `mcpInheritance: all` |
| Perms | `permission_mode: default` + parent always-approve |
| HA | Prefix from _ha-law + nuclear grants when live |
| Skills | Read CONTRACT + this skill |
| Isolation | none (shared OUT dir — required for the bus) |

Do **not** set `tools:`. Children inherit full.

## Interconnect

1. Disk bus under `OUT/.bus/` (READY flags + notes.jsonl + NEXT.json) — source of truth
2. Workflow `ha-pumapay` (full) or `ha-pumapay-tick` (remainder)
3. Shared `~/.grok/pumapay-bus/` with ha-sentinel (COLLAB.md)
4. Root-only live steer

## Dispatch (autonomous — default)

Do **not** spawn lanes by hand. Follow `references/AUTONOMY.md`.

```
bash ~/.grok/skills/ha-pumapay/scripts/ctl.sh auto \
  --out "${PUMAPAY_OUT:-$HOME/Desktop/puma/docs/pumapay-v2}"
# then workflow name=ha-pumapay
```

## Tick (periodic)

```
bash ~/.grok/skills/ha-pumapay/scripts/ctl.sh tick --out "$OUT"
# then workflow name=ha-pumapay-tick
```

Remainder only + always pp-sync + pp-lead.

## When to use tick vs full

Full for initial product tree bootstrap. Tick for ongoing maintenance (idempotent skips).

## Finding / work item block (all lanes)

See CONTRACT.md:

```
## [epic|story|task|bug|chore] TITLE
- Key: PPAY-???
- Component:
- Status:
- Evidence:
- Next:
```


## Peer: platform engineering

Code monorepo = **`/ha-ppdev`** (`ppd-*`, OUT `~/dev/pumapay`).  
Product docs/Jira stay here (`/ha-pumapay`). Domain specs = `/ha-ledger` etc.  
Do not put API/backend source under `Desktop/puma` loot root.

## Official model (xAI)

Parent MCP inherited. No nested grok -p. Bus is law.

See references/ for NORTHSTAR / CONTRACT / AUTONOMY.
