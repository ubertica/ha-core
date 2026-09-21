---
description: Natural-language HA orch this turn. Grok or EA. Optional background queue.
argument-hint: what to do (plain language)
---

# /orch

**Arguments:** $ARGUMENTS

The operator spoke in the TUI. Execute. Do not reply with a CLI tutorial.

1. Stay on this Grok 4.6 HA session.
2. If the text is short/mechanical or says EA/enclave/rápido/privado: run ExpressAI now (`expressai-tui` fast/chat). Return the result.
3. If they said dejalo / background / overnight / cuando no esté: enqueue with
   `node ~/.grok/hard-allow/bin/ha-orch.mjs add --engine auto --order "$ARGUMENTS"`
   and confirm in one line.
4. Otherwise do the work yourself (tools / spawn_subagent).
5. Claude/Kimi: no.
