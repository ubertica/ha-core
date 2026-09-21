---
name: ha-dani
description: >
  Conductor for Daniel / Puma client work after the 2026-09-10/11 BOLA incident.
  Routes to ha-dani-audit | ha-dani-authz | ha-dani-handoff | ha-dani-ops | ha-redteam.
  Civil default. Not ha-hackers. Triggers: /ha-dani, Daniel, reunion, post-incidente Puma, auditoría periódica, redteam party.
---

# ha-dani (conductor)

Read `~/.grok/agents/_ha-dani-law.md` and Drive `dani/docs/DESIGN.md` first.

**SoT = Google Drive** `walterg2924` → `Mi unidad/dani/` (not the Mac).
Nodes tenant **`dani`** (alias `pumapay`) — aparte de `admin`/`root`. HA/admin pueden leer/escribir con `tenant=dani`.

```bash
source ~/.grok/context-nodes/DANI-PATHS.env
python3 ~/.grok/context-nodes/bin/dani-drive.py put --lane redteam --rel probe/PROBE.md --body "..."
python3 ~/.grok/context-nodes/bin/nodes-drive.py search --tenant dani --q "BOLA"
```

## Route

| Signal | Pack | OUT (Drive) |
|--------|------|-------------|
| MR, release, quality, deuda, informe para Daniel | `ha-dani-audit` | `dani/out/10-audit` |
| BOLA, F1–F12, CORS, /docs, owner filter, CLOSED | `ha-dani-authz` | `dani/out/20-authz` |
| 10+ devs, owners, huérfanos, unified-bucket, Staff OS | `ha-dani-handoff` | `dani/out/30-handoff` |
| AMS danielcliente, dash, perímetro, freeze | `ha-dani-ops` | `dani/out/40-ops` |
| Deep tests + proposed fixes + docs + Jira (party g1–g4) | `ha-redteam` | `dani/out/50-redteam` |
| Unclear / whole reunion | run **audit+handoff** first; authz/ops if incident/infra; redteam if TARGET+/docs | `dani/out/00-conductor` |

Then `bash ~/.grok/skills/<pack>/scripts/ctl.sh status --out "$OUT"` and the pack workflow.

## Fallbacks

1. SOCKS `127.0.0.1:1080` or `10808` for third-party. Mac ISP → HOLD.
2. AMS down → disk + HOLD live.
3. No JWT / no staging ACL → `dath-verify` HOLD.
4. Accidental ha-hackers on this work → stop, NACK, continue on `ha-dani-authz`.
5. Volume prose → ExpressAI MCP; conductor stays grok-4.6.
6. Codex/ChatGPT.app: same packs after `sync-pack-to-codex.py`.

## Never

Live money. Live gplaygap patch. Dumping ACCESS.md secrets. Copying `dump/` `hack/` into product repos.
