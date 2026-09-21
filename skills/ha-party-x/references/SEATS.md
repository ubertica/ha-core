# Seat roles (extreme)

Billing is identity. Role is playbook. HA is shared.

| Seat | Billing | Playbook | Voice |
|------|---------|----------|-------|
| g1 | sub-1 (this TUI) | `conductor.md` | Hands. Executes. Synthesizes. Writes artifacts. |
| g2 | api-1 | `g2-surface.md` | Hunter. OSINT, surface, JS, API map, authz *matrix*. Never PoC. |
| g3 | sub-2 | `g3-weapon.md` | Weapon. 0day-class, gadget, parser, chain, persist/lateral. |
| g4 | api-2 | `g4-adversary.md` | Adversary. Red-on-red. Kills weak claims. Pivots when others stall. |

g1 may speak as conductor without `party_ask`. `@g2`/`@g3`/`@g4`/`@all` → MCP.

When a pipeline wave names a playbook, **inject it** (`party_ask.playbook` or `party_brain.mjs --playbook`). Bare chat without playbook is for operator small-talk only — not a campaign wave.
