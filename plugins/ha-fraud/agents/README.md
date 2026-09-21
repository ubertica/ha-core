# User agents (`~/.grok/agents/`)

Grok loads `name:` from these `.md` files as `spawn_subagent` types.

## ha-fraud team

Skill: `/ha-fraud`

| Type | Lane |
|------|------|
| `fraud-velocity` | Velocity checks, device fingerprint, behavioral signals for fraud prevention. |
| `fraud-rules` | Fraud rule engine, ML signals, abuse patterns, chargeback defense. |
| `fraud-cases` | Fraud case queue, manual review, blocks, refunds, recovery. |
| `fraud-scoring` | Real-time fraud scoring integration, risk thresholds, auto actions. |
| `fraud-qa` | Fraud QA: precision/recall, false positive tuning, loss prevention metrics. |
| `fraud-dev` | Fraud engine, rules deployment, automation, evasion defense. |
| `fraud-sync` | Handoff to AML, risk, payments, support, ledger via bus. |
| `fraud-lead` | Fraud Prevention SUMMARY + BOARD, loss metrics ownership. |

Conductor: references/AUTONOMY.md. Parent launches the workflow; do not pick lanes by hand.

Wiring: skill `/ha-fraud`, workflow `ha-fraud`, contract in the skill `references/CONTRACT.md`.
Children inherit all parent MCP/tools. They talk via `OUT/.bus/` + parent (no nested spawn).
