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
python3 ~/.grok/skills/ha-rtk-kb/scripts/kb.py status
python3 ~/.grok/skills/ha-rtk-kb/scripts/kb.py intel  --pack ha-redteam|ha-blackhat --out OUT
python3 ~/.grok/skills/ha-rtk-kb/scripts/kb.py memory --pack … --out OUT --op hydrate|commit
python3 ~/.grok/skills/ha-rtk-kb/scripts/kb.py ingest --pack … --out OUT
python3 ~/.grok/skills/ha-rtk-kb/scripts/kb.py query  --q "jwt fastify"
python3 ~/.grok/skills/ha-rtk-kb/scripts/kb.py learn  --pack … --note "…"
bash ~/.grok/skills/ha-rtk-kb/scripts/ctl.sh selftest
```

Alias: `~/.grok/hard-allow/kb/rtk` → `~/.grok/ha-rtk-kb`.

## Split

| Shared (this KB) | Per-pack OUT |
|------------------|--------------|
| KEV cache, CVE hits | `intel/INTEL.md` (projection) |
| MEMORY.jsonl, LEARN.jsonl | `memory/MEMORY.md` pointer |
| FINDINGS-INDEX.jsonl (redacted fps) | full FINDINGS / loot only in that pack’s OUT |
| `nodes_commit_turn` tags=`ha-rtk-kb` | engagement artifacts |

No JWT/CBU/loot bodies in the shared store. Blackhat loot stays in engagement OUT. Civil pack never reads loot files — only the index.

## Nodes (Drive SoT)

Bodies live on **Google Drive `walterg2924@gmail.com`**:
`Mi unidad/ha-context-nodes/tenants/<admin|root>/`

Mac holds **INDEX placeholders only** (`~/.grok/context-nodes/INDEX.jsonl`). Expand on demand:

```bash
python3 ~/.grok/context-nodes/bin/nodes-drive.py search --q "dedibox"
python3 ~/.grok/context-nodes/bin/nodes-drive.py get --id knowledge.infra.scaleway-dedibox-connect
python3 ~/.grok/skills/ha-rtk-kb/scripts/nodes-bridge.py status
```

Do not copy `state.json` / `ledger.jsonl` back onto the Mac. Cache of expanded nodes: `~/.grok/context-nodes/cache/expanded/`.
