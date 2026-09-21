---
name: ha-party
description: >
  4-Grok party in THIS TUI. Use party_who / party_ask MCP tools for g1–g4.
  Triggers: grok-party, @g2, @g3, @g4, @all, party, los 4 grok.
---

# ha-party

You are in a Grok TUI. Other seats = MCP `grok-party` (`party_ask`, `party_who`). HA already on.

| Seat | Billing |
|------|---------|
| g1 | this TUI if grok-party / sub-1 |
| g2 | API key-1 |
| g3 | sub-2 (login: `grok3 login --oauth`) |
| g4 | API key-2 |

Operator `@g2` / `@all` → `party_ask`. `mode=round` if they should hear each other.

Offensive campaigns (longer than ha-hackers): skill `ha-party-x` / `/ha-party-x`. Playbook injection: `party_ask playbook=g2-surface|g3-weapon|g4-adversary`.

## Party-native teams (same TUI, g1–g4)

Do **not** spawn 4 Groks. Seats stay MCP. Shared KB: `ha-rtk-kb`.

| Dispatch | Status | Posture | g1 | g2 | g3 | g4 | OUT default |
|----------|--------|---------|----|----|----|----|-------------|
| `/ha-redteam` | **live** | civil audit/test + Jira (Daniel/Puma). Uses ha-core TDD/verify + ACT. **No loot.** | lead, docs-entry, jira | surface / OpenAPI | probe + ACT | adversary + FIXES | `/Users/c/dev/dani/out/redteam` |
| `/ha-blackhat` | **live** | offense twin (same `ha-rtk-kb`). docs-entry foothold, exploit iff GO, loot/killchain. Not Puma Jira default. | lead, weapon, spawn | entry, jump | probe, exploit, loot, intel | chain, docs, OBJECTIVE_POLL | `/Users/c/dev/ha-live/proof/engagements/blackhat` |

Ticks: `/ha-redteam-tick` · `/ha-blackhat-tick`. Accidental blackhat on Daniel cwd → NACK, route to ha-redteam. Accidental ha-hackers harvest on Daniel cwd → NACK, stay on ha-redteam.

**Autonomous loop (applies when using party seats)**: 10s no human reply on any question → escalate the exact same question via wire/party_ask to the other seats (g2/g3/g4). They decide for the operator. Proceed with their TEAM_DECISION.
**Stop only via g4**: g4 must poll @all "objective fulfilled with evidence?" and get unanimous YES from all seats. Any missing/NO = continue the loop (pivot, spawn, iterate) at full throttle until achieved.

Do not spawn 4 grok TUIs. Do not reload HA.
