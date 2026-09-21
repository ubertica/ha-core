---
description: Do this with ExpressAI this turn (fast/private). Natural language.
argument-hint: what to do
---

# /ea

**Arguments:** $ARGUMENTS

Stay on Grok 4.6. Run ExpressAI for this payload (MCP `ea_fast`/`ea_chat` if connected, else `expressai-tui`).

No flag soup. If MCP missing: `cd /Users/c/dev/expressai-tui && node bin/expressai.mjs fast transform -i "$ARGUMENTS"`.

Return the EA output. You synthesize if needed. Claude/Kimi: no.
