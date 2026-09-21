# User agents (`~/.grok/agents/`)

Grok loads `name:` from these `.md` files as `spawn_subagent` types.

## ha-ledger team

Skill: `/ha-ledger`

| Type | Lane |
|------|------|
| `led-model` | Double-entry ledger model, accounts chart, posting rules. |
| `led-posting` | Idempotent post/hold/release APIs and invariants. |
| `led-recon` | Reconciliation vs bank/PSP; break detection. |
| `led-settle` | Settlement batches, cutoffs, multi-currency notes. |
| `led-test` | Ledger property tests and fixtures. |
| `led-dev` | Implement ledger changes; CHANGES.md |
| `led-sync` | Bus events to payments/risk/treasury. |
| `led-lead` | SUMMARY + BOARD for ledger team. |

Conductor: references/AUTONOMY.md. Parent launches the workflow; do not pick lanes by hand.

Wiring: skill `/ha-ledger`, workflow `ha-ledger`, contract in the skill `references/CONTRACT.md`.
Children inherit all parent MCP/tools. They talk via `OUT/.bus/` + parent (no nested spawn).
