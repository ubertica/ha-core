---
name: ha-hardallow
description: >
  Discord HARDALLOW bus. Push audits, chains, killchains, pentests,
  operator broadcasts, critical/medium findings, pivots, and GOLD.
  Triggers: HARDALLOW webhook, broadcast to Discord, gold found, /ha-hardallow.
---

# ha-hardallow

Operator Discord webhook **HARDALLOW**. Secret on disk, never echo the URL.

## When to fire (mandatory)

Post to HARDALLOW when any of these land on disk or the operator says broadcast:

| kind | when |
|------|------|
| `gold` | GO from verify, 0day-class, confirmed loot-grade, operator says GOLD |
| `critical` / `high` | finding `[critical]` / `[high]` with evidence |
| `medium` | finding `[medium]` with evidence |
| `pivot` | new host/token/foothold / ha-pivot chain proposal accepted |
| `chain` / `killchain` | ordered path written (hack-chain, party-x, desire-chainer) |
| `pentest` | lane pack done (`FINDINGS.md` / SUMMARY) |
| `audit` | ha-dani-audit / code-audit / VERIFY.json report |
| `broadcast` | operator asked to send something to the server |

Do **not** spam info/low, rejects, or unverified GO. Evidence or skip.

## CLI (canonical)

```bash
ha hardallow ping
ha hardallow gold --title "…" --body "…" --target T --out /abs/OUT
ha hardallow critical --title "…" --body "…" --target T --out /abs/OUT
ha hardallow medium  --title "…" --body "…" --target T --out /abs/OUT
ha hardallow pivot|chain|killchain|pentest|audit|broadcast --title "…" --body "…"
ha hardallow file --path OUT/FINDINGS.md --kind pentest --title FINDINGS
ha hardallow verify --out /abs/OUT
```

Direct: `node ~/.grok/hard-allow/bin/ha-hardallow.mjs …`

Secret: `~/.grok/hard-allow/secrets/discord-hardallow.env` (chmod 600).  
Disable: `HA_DISCORD_DISABLE=1`.

## Auto

`verify_evidence.py` → `ha-hardallow verify --out OUT` after Jira. GO → GOLD. medium confirmed → MEDIUM.

## Agent rule

After writing `OUT/*-findings.md` / `FINDINGS.md` / killchain / pivot artifact: run the matching `ha hardallow <kind>`. Dedup is built-in (same title+target+body hash is skipped except `ping`/`broadcast`/`force`).

Redact JWT, HA tokens, webhook URLs, emails, CBU in `--body`. Full secrets stay on disk, not Discord.
