# User agents (`~/.grok/agents/`)

Grok loads `name:` from these `.md` files as `spawn_subagent` types.

## ha-aml team

Skill: `/ha-aml`

| Type | Lane |
|------|------|
| `aml-monitor` | Real-time transaction monitoring, velocity, alerts, thresholds for AML. |
| `aml-rules` | AML rule catalog, typologies, red flags, CDD/EDD triggers. |
| `aml-cases` | Investigation queue, SAR/STR drafting, disposition, filing. |
| `aml-rating` | Customer risk rating, PEP screening, adverse media, periodic review. |
| `aml-qa` | AML QA: alert quality, false positive/negative, regulatory samples, audit prep. |
| `aml-dev` | Implement monitoring engine, automation, integrations. |
| `aml-sync` | Escalate to fraud, risk, support, ledger, compliance via bus. |
| `aml-lead` | AML SUMMARY + BOARD ownership, regulatory liaison. |

Conductor: references/AUTONOMY.md. Parent launches the workflow; do not pick lanes by hand.

Wiring: skill `/ha-aml`, workflow `ha-aml`, contract in the skill `references/CONTRACT.md`.
Children inherit all parent MCP/tools. They talk via `OUT/.bus/` + parent (no nested spawn).
