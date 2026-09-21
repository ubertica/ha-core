# User agents (`~/.grok/agents/`)

Grok loads `name:` from these `.md` files as `spawn_subagent` types.

## ha-dani-ops team

Skill: `/ha-dani-ops` · Civil overlay: `_ha-dani-law.md`

| Type | Lane |
|------|------|
| `dops-perimeter` | Read-only perimeter of Daniel infra (lx-prod/uat, gppay, wallets, PAM staging, S3, WS). Cite HA-SERVICE-PUMA-INFRA.md. Do not live-patch. |
| `dops-ams` | AMS danielcliente units ha-live / loot / sentinel health via documented ctl. Not root. No HA token on that user. |
| `dops-dash` | Dash puma.jailbroken.tech /health /api/service. Creds from ACCESS.md path only, never echo passwords. |
| `dops-change` | Change windows, freeze, rollback notes. Link ha-release GONOGO when product train. |
| `dops-escalate` | Escalate to ha-sentinel/ha-sre/ha-sec. Not ha-hackers. |
| `dops-hold` | HOLD-live-money HOLD-live-gplaygap-patch HOLD-Mac-ISP-third-party. |
| `dops-sync` | Bus to the other three dani packs. |
| `dops-lead` | Ops SUMMARY. Honest down hosts. elite-play 503 is theirs not HA. |

Conductor: references/AUTONOMY.md. Parent launches the workflow; do not pick lanes by hand.
Default OUT: `/Users/c/dev/dani/out/ops`
Children inherit all parent MCP/tools. They talk via `OUT/.bus/` + parent (no nested spawn).
