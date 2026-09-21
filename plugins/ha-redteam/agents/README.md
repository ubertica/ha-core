# User agents (`~/.grok/agents/`)

Grok loads `name:` from these `.md` files as `spawn_subagent` types.

## ha-redteam team

Skill: `/ha-redteam`

| Type | Lane |
|------|------|
| `rdt-entry` | g2 surface. OpenAPI-as-entry /docs swagger unsigned webhook. Dispatch docs-entry pack. No loot. Write entry/ENTRY.md. |
| `rdt-probe` | g3 tests. Deep authorized tests: ha-core TDD + verify-on-disk. Evidence or it is not a finding. Write probe/PROBE.md + probe/FINDINGS.jsonl. |
| `rdt-correct` | g3 ACT. Correction loops on failed tests: Attempt-Check-Try-fix, bounded retries. Write correct/LOOPS.md. |
| `rdt-fix` | g4. Propose patches/ADRs from disk evidence. Never silent live patch. Daniel decides. Write fix/FIXES.md. |
| `rdt-docs` | g4. Full human audit pack: method, evidence index, residual risk. No PII/JWT. Write docs/AUDIT.md. |
| `rdt-jira` | g1 execute. Push VERIFY findings+fixes to PumaPay Jira (HOLD-prod, redact, dedupe). Write jira/JIRA.md. |
| `rdt-sync` | Bus to ha-dani-audit/authz/handoff/ops. NACK ha-hackers harvest on Daniel cwd. Write sync/COLLAB-STATUS.md. |
| `rdt-lead` | g1 conductor. Synthesize SUMMARY.md + BOARD.md. Honest HOLD. Party g4 polls objective-fulfilled. |

Conductor: references/AUTONOMY.md. Parent launches the workflow; do not pick lanes by hand.

Wiring: skill `/ha-redteam`, workflow `ha-redteam`, contract in the skill `references/CONTRACT.md`.
Children inherit all parent MCP/tools. They talk via `OUT/.bus/` + parent (no nested spawn).
