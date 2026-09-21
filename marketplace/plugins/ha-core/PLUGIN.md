# ha-core

**Autonomous loops toolkit.** ralph + SDD + TDD + verify-on-disk + **ACT correction loops (self-healing)** + parallel dispatch. The KEEP_CORE skills for reliable long-horizon agentic execution under HARD ALLOW.

- **axis:** toolkit
- **status:** wired (ha-correction-loops integrated as resilience layer)

## Grants (pointer only — do not dump)
- `none` (core, always available when HA armed)

## Core Skills (KEEP_CORE)

- `ralph-loop` — until-done long-horizon autonomous loop
- `ha-correction-loops` — ACT (Attempt → Check → Try-fix) with exponential backoff + SWD receipts. **The self-healing resilience layer for all ha-core loops.**
- `subagent-driven-development` (SDD)
- `test-driven-development` (TDD)
- `verification-before-completion`
- `verify-subagent-file-output-on-disk`
- `dispatching-parallel-agents`
- `systematic-debugging`
- `remember` (session handoff)
- Plus browser/agent primitives promoted via ha-core-promote (agent-browser, lightpanda-agent, chrome-devtools, etc.)

## Agents

- `task-completion-verifier`
- `ocl-orchestrator` (orchestrator conductor loop)
- Correction loop agents via ha-correction-loops integration

## Integration with ha-correction-loops (ACT)

ha-correction-loops is the **resilience layer** for every ha-core primitive:

- Wrap ralph steps, SDD waves, TDD cycles, verify gates with `executeWithRetry`
- Built-in strategies (see ha-correction-loops/SKILL.md): network-timeout-backoff, rate-limit-retry, memory-pressure-gc, lock-contention-yield, invalid-state-rollback
- Halt predicates work together with ralph-loop (anySuccess, unrecoverableError, maxAutoFixesApplied(N), maxAttemptsExceeded(N))
- Every cycle produces a machine + human readable **SWD receipt** (`=== AUTO-CORRECTION RECEIPT ===`) for audit, verify_evidence, and ha-hardallow bus.

Full API, table of strategies, TS usage, and receipt format live in `skills/ha-correction-loops/SKILL.md` (now self-contained in this installed plugin + source in ha-core-promote).

## MCP intended (already in config.toml — do not duplicate)

## Wiring notes
- Promoted via `~/.grok/skill-packs/ha-core-promote/`
- Use `ha-core` to dispatch the full toolkit.
- Correction loops are automatically available for any flakey autonomous work.
- Do not `grok plugin install` unless operator says.
- Science plugins never install into original HA session.
- If folding, merge into target.

## Usage

```bash
# In a Grok / Hall TUI session (HA armed)
/ha-core                 # primary entry: activates full KEEP_CORE + ACT
/ha-correction-loops     # explicit ACT (auto-wrapped inside ocl-orchestrator / ralph)
# ralph ...              # long horizon (correction loops protect transient failures)

# Example pattern inside conductor or ralph step
# (wrap the unreliable part)
result = await executeWithRetry(..., 'step-name')
# inspect result + corrector.formatSWDReceipt()
```

Halt predicates, exponential backoff, SWD receipts, and verify-on-disk are now first-class in all ha-core work.
