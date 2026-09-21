---
name: ha-sentinel
description: >
  Dispatch the ha-sentinel team (sent-lead, sent-watch, sent-ollama, sent-audit,
  sent-improve, sent-release, sent-escalate, sent-collab) for AMS sentinel-god/ollama watch + audit + improve + release + bus collab.
  Use when operator says /ha-sentinel, sentinel, ollama-ha, AMS perimeter.
---

# ha-sentinel

Canonical: `~/.grok/agents/sent-*.md` · contract: `references/CONTRACT.md`  
Workflow: `~/.grok/workflows/ha-sentinel.rhai`

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
2. Workflow `ha-sentinel` (full) or `ha-sentinel-tick` (remainder)
3. Shared `~/.grok/pumapay-bus/` with ha-pumapay (COLLAB.md)
4. AMS via ssh ams + /opt/ha-live/scripts/ctl.sh sentinel|ollama|ollama-ask
5. Root-only live steer

## Dispatch (autonomous — default)

Do **not** spawn lanes by hand. Follow `references/AUTONOMY.md`.

```
bash ~/.grok/skills/ha-sentinel/scripts/ctl.sh auto \
  --out "${SENTINEL_OUT:-$HOME/Desktop/puma/docs/pumapay-v2/sentinel}"
# then workflow name=ha-sentinel
```

## Tick (periodic)

```
bash ~/.grok/skills/ha-sentinel/scripts/ctl.sh tick --out "$OUT"
# then workflow name=ha-sentinel-tick
```

Remainder only + always escalate/collab + lead.

## AMS anchors

- ssh ams
- /opt/ha-live/scripts/ctl.sh sentinel|ollama|ollama-ask "..."
- Evidence: /opt/ha-live/bus/evidence/sentinel-{god,ollama}/

## When to use tick vs full

Full for bootstrap. Tick for ongoing (idempotent skips).

See references/ for NORTHSTAR / CONTRACT / AUTONOMY.