# ha-core

Dispatch the ha-core autonomous toolkit (KEEP_CORE + ACT self-healing).

## Usage
/ha-core

(Also: /ha-correction-loops for explicit ACT, /ralph for long horizon, etc.)

## Effect
Activates the full set:

- ralph-loop (until-done)
- ha-correction-loops (ACT: Attempt→Check→Try-fix with backoff + SWD receipts)
- subagent-driven-development (SDD)
- test-driven-development (TDD)
- verification-before-completion + verify-subagent-file-output-on-disk
- dispatching-parallel-agents
- systematic-debugging
- remember

ha-correction-loops is wired as the automatic resilience layer around transient failures in all of the above.

All long autonomous work in this session should benefit from correction loops.

See PLUGIN.md, skills/ha-core/SKILL.md and skills/ha-correction-loops/SKILL.md.
