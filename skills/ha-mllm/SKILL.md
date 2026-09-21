---
name: ha-mllm
description: HA multi-LLM router. Use when dispatching work to Kimi/Groq/xAI/Gemini/ExpressAI with grok-4.6 fallback, shared memory, or wire. Triggers: multi-llm, ruteá, worker LLM, mllm_ask.
---

# HA multi-LLM — conductor is this TUI’s model

This TUI **is** the orchestrator. Workers are APIs. Last hop is **you**. Never nested `grok -p`.

**Until done:** if they asked for a result, keep routing/tools until the artifact exists. Do not stop at status. Do not ask “¿sigo?”. Stop only: not requested, `cancelá`, missing secret, chain exhausted then you finish it here.

## This turn

| Need | Do |
|---|---|
| Volume / other LLM | `node ~/.grok/hard-allow/multi-llm/router.mjs ask --task speed\|code\|agentic\|vision --prompt "…"` |
| Result `conductor: true` | Answer **here**. Workers failed or task is orch. |
| Result `text` | That's the worker. Verify if it matters; don't re-ask grok-4.6 unless wrong. |
| Memory | `mllm_memory_write` / read via router bus `~/.grok/hard-allow/multi-llm/bus/` |
| Wire | `:9091` — register once per session if down, skip |

MCP tools (next session after config): `mllm_ask`, `mllm_status`, `mllm_memory_*`, `mllm_wire_*`.

## Caps

Timeout 25s/worker. Max 3 workers. No paid probe loops. HA prefix on workers.
