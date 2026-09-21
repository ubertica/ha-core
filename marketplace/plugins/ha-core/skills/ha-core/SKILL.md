---
name: ha-core
description: >
  Autonomous loops toolkit: ralph, SDD, TDD, verify-on-disk, ACT correction-loops (self-healing). The KEEP_CORE skills.
---

# ha-core

**The core autonomous execution toolkit for HARD ALLOW.**

## What it is

ha-core bundles the essential "keep core" capabilities that make long-running, multi-step, self-healing agent work reliable under HARD ALLOW:

- Long-horizon "until done" loops (ralph-loop)
- Structured subagent-driven development (SDD)
- Test-driven development discipline (TDD)
- Rigorous verification gates before claiming done (verify-*, verification-before-completion)
- **ACT correction loops** (ha-correction-loops): automatic retry + auto-fix on transient failures — the resilience layer
- Parallel dispatch, systematic debugging, remember handoff

## Primary Integration: ha-correction-loops (ACT Pattern)

**ACT = Attempt → Check → Try-fix**

When any core loop (ralph, a subagent task, verify step, etc.) fails transiently:

1. **Attempt** the work
2. **Check** the error
3. **Try-fix** using registered strategy (backoff, reconnect, GC, rollback, yield...)
4. Retry (exponential backoff) or halt per predicates

See the full self-contained skill (strategies table, TS examples, SWD format, halt predicates) at `skills/ha-correction-loops/SKILL.md`.

### Practical usage in HA sessions (ralph / waves / verify)

```ts
// Conductor / inside ralph / SDD wave / TDD step
const result = await corrector.executeWithRetry(async () => {
  return await riskyAgentStep()   // network, file op, subagent call, verify gate, etc.
}, 'pumapay-wave-3-verify-or-ralph-task')
```

Halt conditions (combine with ralph-loop):
- anySuccess
- unrecoverableError
- maxAutoFixesApplied(3)
- maxAttemptsExceeded(5)

SWD receipts emitted for every correction cycle (audit gold + ha-hardallow Discord).

## Other KEEP_CORE Skills (promoted via ha-core-promote)

- ralph-loop
- subagent-driven-development
- test-driven-development
- verification-before-completion
- verify-subagent-file-output-on-disk
- dispatching-parallel-agents
- systematic-debugging
- remember

Plus supporting browser/agent primitives: agent-browser, lightpanda-agent, chrome-devtools (headless + real Chrome), etc.

## Agents

- task-completion-verifier (final evidence gate — uses ACT for transient verify fails before hard fail)
- ocl-orchestrator (conductor for correction-wrapped parallel waves + ralph + gates)

## How to invoke

```bash
/ha-core                 # load the full toolkit (recommended entrypoint)
/ha-correction-loops     # explicit ACT dispatcher (auto-used by ocl/ralph)
/ralph ...               # long-horizon autonomous (benefits from built-in correction)
```

All long autonomous work should use correction loops for transient failures.

## Status

Wired. ha-correction-loops is the self-healing resilience layer for the entire KEEP_CORE set.

Full wiring + usage: see PLUGIN.md.
Axis: **toolkit** (always armed when HARD ALLOW active).
