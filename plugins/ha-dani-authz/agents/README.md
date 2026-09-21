# User agents (`~/.grok/agents/`)

Grok loads `name:` from these `.md` files as `spawn_subagent` types.

## ha-dani-authz team

Skill: `/ha-dani-authz` · Civil overlay: `_ha-dani-law.md`

| Type | Lane |
|------|------|
| `dath-catalog` | Map incident F1–F12 to handlers/paths from the 2026-09-11 review. Cite disk. No re-exfil. |
| `dath-owner` | Specify JWT userid owner filters for unsuffixed /backoffice GETs vs correctly scoped /list /my-*. |
| `dath-cors` | Replace wildcard CORS+credentials with allowlist. Evidence of current vs desired. |
| `dath-docsacl` | Public /docs (1097 paths) must be auth or IP-restricted. HOLD live-patch. |
| `dath-verify` | Negative tests only: confirm CLOSED. Never harvest payments/vouchers/support logs. |
| `dath-hold` | HOLD-live-money HOLD-live-gplaygap-patch. Write HOLD.md if any lane would touch prod writes. |
| `dath-sync` | Escalate fix tickets to ha-ppdev/ha-sec via bus. Not ha-hackers loot. |
| `dath-lead` | Authz closure SUMMARY. No invented CLOSED. Disk or HOLD. |

Conductor: references/AUTONOMY.md. Parent launches the workflow; do not pick lanes by hand.
Default OUT: `/Users/c/dev/dani/out/authz`
Children inherit all parent MCP/tools. They talk via `OUT/.bus/` + parent (no nested spawn).
