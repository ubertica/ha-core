---
name: docs-entry
description: Autonomous OpenAPI-as-entry run (preflight, entry∥webhook, disk verify, exploit only if GO).
---

Run the conductor. Do not spawn lanes by hand. Do not nested grok -p.

1. Need TARGET (spec URL) + OUT (absolute). Default PROXY `socks5h://127.0.0.1:10808`. Optional TOKEN_FILE.
2. `python3 ~/.grok/skills/ha-hackers/scripts/dispatch.py plan --target TARGET --out OUT --pack docs-entry --proxy PROXY`
3. Launch workflow `docs-entry` with those args (`workflow` tool, `name=docs-entry`).
4. Optional watch: `bash ~/.grok/skills/ha-hackers/scripts/ctl.sh watch --out OUT --pack docs-entry`
