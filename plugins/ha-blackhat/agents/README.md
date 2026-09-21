# User agents (`~/.grok/agents/`)

Grok loads `name:` from these `.md` files as `spawn_subagent` types.

## ha-blackhat team

Skill: `/ha-blackhat`

| Type | Lane |
|------|------|
| `bht-entry` | g2 surface. OpenAPI-as-entry /docs unauth+webhook foothold. Dispatch docs-entry. Write entry/ENTRY.md. |
| `bht-probe` | g3. Deep offense tests. FINDINGS.jsonl. Evidence or not a finding. Write probe/PROBE.md. |
| `bht-exploit` | g3. PoC only if disk go_count>0. Write exploit/EXPLOIT.md + poc/. |
| `bht-loot` | g3. Harvest to engagement OUT only. Never product repos. Write loot/LOOT.md. |
| `bht-chain` | g4. Ordered killchain from disk GOs. Write chain/CHAIN.md. |
| `bht-weapon` | g1. ha-offense delivery if GO+operator. Write weapon/WEAPON.md. |
| `bht-docs` | g4. Operator FINDINGS pack. Redact in chat; full on disk OUT. Write docs/FINDINGS.md. |
| `bht-lead` | g1 conductor. SUMMARY+BOARD. g4 OBJECTIVE_POLL. Write SUMMARY.md. |

Conductor: references/AUTONOMY.md. Parent launches the workflow; do not pick lanes by hand.

Wiring: skill `/ha-blackhat`, workflow `ha-blackhat`, contract in the skill `references/CONTRACT.md`.
Children inherit all parent MCP/tools. They talk via `OUT/.bus/` + parent (no nested spawn).
