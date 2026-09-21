# LAYERS — always-on (not required READY)

Core lanes stay the audit pack. These run every cycle via `ctl.sh layers`.

| Layer | Seat | Disk | Wire |
|-------|------|------|------|
| **radio** | all | `.bus/pivot/comms.jsonl` | `party_ask` round + `ha hardallow` + session-wire if MCP |
| **jump** | g2 | `jump/JUMP.md` + `.bus/NEXT-HOSTS.json` | next host from FINDINGS only |
| **pivot** | g1 | `.bus/pivot/` | reuse `ha-pivot` protocol (graph, XXX, spawn-requests) |
| **intel** | g3 | `intel/INTEL.md` | NVD / CISA KEV / OSV / GHSA / local catalogs |
| **memory** | g1 | `.bus/MEMORY.jsonl` | `ha-context-nodes` search + `nodes_commit_turn` |
| **spawn** | g1 only | `.bus/pivot/spawn-request-*.json` | `request-subagent.mjs` then `spawn_subagent` |
| **learn** | g1 | `learn/LEARN.md` | self-improve from disk flaws (ha-live-learn shape) |

## Real-time radio

Every significant write: append comms.jsonl (`HEARTBEAT|PROGRESS|BLOCKER|JUMP|PIVOT|SPAWN_REQUEST|OBJECTIVE_*`) **and** `party_ask` if seats must hear each other **and** `ha hardallow <kind>` for gold/critical/pivot.

## Jump vs pivot

- **Jump** = next TARGET from evidence (host/path already on disk).
- **Pivot** = horizontal graph (ha-pivot mesh/swarm). Proposal in `.bus/pivot/chain-proposals/`.

Jump invalidates stale READY on the old host (keep artifacts, set `.bus/STALE.<lane>`).

## Children

g1 spawns. Child inherits HA + CHARTER + OUT. Child writes SPAWN_REQUEST if it needs help — does **not** spawn. Max 8 live. Theater spawn = NACK.

## Memory

Hydrate at start: `nodes_search` / `query_nodes` for TARGET + prior findings. End of cycle: `nodes_commit_turn` (source=grok, tags=ha-redteam) + MEMORY.jsonl. Do not dump secrets into nodes.
