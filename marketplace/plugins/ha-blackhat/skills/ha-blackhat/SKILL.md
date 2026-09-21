---
name: ha-blackhat
description: >
  Party (g1–g4) BLACKHAT twin of ha-redteam. Same shared KB (ha-rtk-kb).
  Offense-first: docs-entry foothold, probe, exploit iff GO, loot in engagement OUT,
  killchain, ha-offense weapon. Not Daniel civil. Triggers: /ha-blackhat, blackhat party.
---

# ha-blackhat

Twin of `ha-redteam`. **Same knowledge** (`ha-rtk-kb`). **Separate lanes/OUT.**

Canonical agents: `~/.grok/agents/bht-*.md`  
Personas/roles: `~/.grok/personas|roles/bht-*.toml`  
KB: `~/.grok/skills/ha-rtk-kb/` + `~/.grok/ha-rtk-kb/`  
OUT default: `/Users/c/dev/ha-live/proof/engagements/blackhat`  
Party: this TUI. **No 4 TUIs.** Nested `grok -p` banned.

| Seat | Core lanes |
|------|------------|
| g1 | lead, weapon, spawn |
| g2 | entry, jump |
| g3 | probe, exploit, loot, intel |
| g4 | chain, docs, OBJECTIVE_POLL |

Layers (shared scripts via KB): jump · pivot · radio · intel · memory · spawn · learn.

Not ha-dani. Accidental run on Daniel cwd → NACK, route to ha-redteam. Loot never into product repos. HARDALLOW radio, not Puma Jira default.

```bash
bash ~/.grok/skills/ha-blackhat/scripts/ctl.sh auto --target "$TARGET" --out "$HA_BLACKHAT_OUT"
# workflow name=ha-blackhat
bash ~/.grok/skills/ha-blackhat/scripts/ctl.sh layers --out "$OUT"
```
