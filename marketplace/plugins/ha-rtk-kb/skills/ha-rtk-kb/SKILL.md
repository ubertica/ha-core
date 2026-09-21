---
name: ha-rtk-kb
description: >
  Shared knowledge base for ha-redteam (civil) and ha-blackhat (offense).
  CVE/KEV/OSV cache, redacted findings index, MEMORY.jsonl, LEARN.jsonl, context-nodes tags.
  Lanes stay separate. Knowledge is one. Triggers: rtk-kb, shared intel, KB redteam blackhat.
---

# ha-rtk-kb

Disk: `~/.grok/ha-rtk-kb/`  
Scripts: `~/.grok/skills/ha-rtk-kb/scripts/kb.py`  
Feeds: `references/INTEL.md`

Both packs **must** call this, not a private copy:

```bash
python3 ~/.grok/skills/ha-rtk-kb/scripts/kb.py intel  --pack ha-redteam|ha-blackhat --out OUT
python3 ~/.grok/skills/ha-rtk-kb/scripts/kb.py memory --pack … --out OUT --op hydrate|commit
python3 ~/.grok/skills/ha-rtk-kb/scripts/kb.py ingest --pack … --out OUT
python3 ~/.grok/skills/ha-rtk-kb/scripts/kb.py query  --q "jwt fastify"
```

## Split

| Shared (this KB) | Per-pack OUT |
|------------------|--------------|
| KEV cache, CVE hits | `intel/INTEL.md` (projection) |
| MEMORY.jsonl, LEARN.jsonl | `memory/MEMORY.md` pointer |
| FINDINGS-INDEX.jsonl (redacted fps) | full FINDINGS / loot only in that pack’s OUT |
| `nodes_commit_turn` tags=`ha-rtk-kb` | engagement artifacts |

No JWT/CBU/loot bodies in the shared store. Blackhat loot stays in engagement OUT. Civil pack never reads loot files — only the index.

## Nodes

Hydrate: `nodes_search` q=TARGET + `ha-rtk-kb`.  
Commit: `nodes_commit_turn` source=grok tags=`[ha-rtk-kb, ha-redteam|ha-blackhat]`.
