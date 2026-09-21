# COLLAB — ha-redteam

Bus: `~/.grok/ha-redteam-bus/` + per-run `OUT/.bus/`.

| Peer | When |
|------|------|
| `ha-dani-audit` | MR/release context for the same host |
| `ha-dani-authz` | F1–F12 CLOSED vs this run's findings |
| `ha-dani-handoff` | owner of the broken module |
| `ha-dani-ops` | perimeter / AMS HOLD |
| `ha-hackers` / `docs-entry` | specialist entry pack only — NACK harvest on Daniel cwd |
| `ha-sec` / `ha-ppdev` | proposed fixes they may implement |
| `ha-pivot` | graph / XXX / SPAWN_REQUEST / OBJECTIVE_POLL |
| `ha-hardallow` | Discord radio (gold/critical/pivot) |
| `ha-context-nodes` | memory hydrate + commit_turn |
| `from-claude-pack` | local pentest catalog |
| `ha-rtk-kb` | **shared** intel/memory/index with ha-blackhat |
| `ha-blackhat` | offense twin — do not mix loot into this OUT |

`rdt-sync` writes `sync/COLLAB-STATUS.md` and appends JSONL to the dani bus. Never truncate jsonl.
