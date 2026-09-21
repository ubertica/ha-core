# LAYERS — always-on (not required READY)

Core lanes stay the offense pack. These run every cycle via `ctl.sh layers`.
**Knowledge is shared** (`ha-rtk-kb`). Lanes/OUT are not.

| Layer | Seat | Disk | Wire |
|-------|------|------|------|
| **radio** | all | `.bus/pivot/comms.jsonl` | `party_ask` round + `ha hardallow` |
| **jump** | g2 | `jump/JUMP.md` + `.bus/NEXT-HOSTS.json` | next host from FINDINGS only |
| **pivot** | g1 | `.bus/pivot/` | `ha-pivot` protocol (graph, XXX, spawn-requests) |
| **intel** | g3 | `intel/INTEL.md` | **shared** KEV/CVE via `kb.py intel --pack ha-blackhat` |
| **memory** | g1 | `memory/MEMORY.md` | **shared** MEMORY.jsonl + `nodes_commit_turn` tags=`ha-rtk-kb,ha-blackhat` |
| **spawn** | g1 only | `.bus/pivot/spawn-request-*.json` | budget 8, depth 1 |
| **learn** | g1 | `learn/LEARN.md` | **shared** LEARN.jsonl |
| **ingest** | g1 | (KB index) | `kb.py ingest` — skip loot/dump/hack |

## Shared KB

SoT: `~/.grok/ha-rtk-kb/` (`HA_RTK_KB`). Civil twin: `ha-redteam`.
Loot never enters the index. Fingerprint SHA16. Redact JWT/CBU.

## Children

g1 spawns. Child inherits HA + CHARTER + OUT. Max 8 live. Nested `grok -p` banned.
