# CONTRACT — ha-rtk-kb

Shared brain for `ha-redteam` (civil) and `ha-blackhat` (offense).

## Split (product, not a flag)

| Shared (this KB) | Per-pack OUT |
|------------------|--------------|
| CISA KEV cache | `intel/INTEL.md` projection |
| MEMORY.jsonl LEARN.jsonl | `memory/MEMORY.md` pointer |
| FINDINGS-INDEX.jsonl (redacted + sha16) | full FINDINGS / GO only in that pack OUT |
| nodes tags=`ha-rtk-kb` | engagement artifacts, loot, killchain |

## MUST

- Both packs call `scripts/kb.py`, never a private KEV copy.
- Redact JWT / CBU / email / HA token / bearer.
- Skip `loot/` `dump/` `hack/` on ingest.
- Fingerprint by SHA256-16 of the raw line (dedup).
- Fail-open if a feed is down.
- SOCKS AMS when hitting third-party HTTP (`HA_PROXY`).
- Node bodies live on Drive (`walterg2924`). Mac keeps INDEX placeholders; expand via `nodes-drive.py`.

## MUST NOT

- Store loot blobs, JWT, CBU, cookie jars, HAR bodies.
- Mix blackhat loot into civil OUT.
- Push blackhat killchains to Puma Jira by default.
- Invent GO from KB hits (cite feed ≠ disk evidence).
- Merge boards / READY flags across packs.

## CLI

```bash
python3 ~/.grok/skills/ha-rtk-kb/scripts/kb.py status
python3 ~/.grok/skills/ha-rtk-kb/scripts/kb.py intel  --pack ha-redteam|ha-blackhat --out OUT
python3 ~/.grok/skills/ha-rtk-kb/scripts/kb.py memory --pack … --out OUT --op hydrate|commit
python3 ~/.grok/skills/ha-rtk-kb/scripts/kb.py ingest --pack … --out OUT
python3 ~/.grok/skills/ha-rtk-kb/scripts/kb.py query  --q "jwt fastify"
python3 ~/.grok/skills/ha-rtk-kb/scripts/kb.py learn  --pack … --note "…"
```
