# ha-correction-loops

Explicit dispatcher for the ACT self-healing correction loops (Attempt → Check → Try-fix).

Part of ha-core (the autonomous toolkit).

## Usage

/ha-correction-loops [optional description]

Usually invoked implicitly by ocl-orchestrator, ralph-loop, SDD waves, TDD, or verify steps when transient failures occur.

You can call it directly to force ACT wrapping around the next block of work.

## What it does

- Registers / activates the AutoCorrector + built-in strategies
- Provides `executeWithRetry(task, description)`
- Emits SWD receipts on every correction cycle
- Respects combined halt predicates with ralph

## Common strategies applied automatically

- network-timeout-backoff
- rate-limit-retry
- memory-pressure-gc
- lock-contention-yield
- invalid-state-rollback

## Recommended

Use `/ha-core` (broader) for most sessions. Use this when you want to highlight or force the correction layer on a specific risky phase.

See:
- skills/ha-core/SKILL.md
- skills/ha-correction-loops/SKILL.md (full spec + examples)
- agents/ocl-orchestrator.md
