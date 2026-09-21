# INTEL — via shared ha-rtk-kb

Do **not** keep a private KEV copy. Same brain as ha-redteam.

SoT cache: `~/.grok/ha-rtk-kb/cache/`

| Feed | Use |
|------|-----|
| CISA KEV | `kb.py intel --pack ha-blackhat --out OUT` |
| NVD / OSV / GHSA | cite; match tech on disk |
| Exploit-DB / searchsploit | cite; payloads stay in engagement OUT, never in KB |
| from-claude-pack | `~/.grok/skills/from-claude-pack/` |
| ha-context-nodes | `nodes_search` / `nodes_commit_turn` tags=ha-rtk-kb |

SOCKS AMS for third-party HTTP. Fail-open. Invented CVE = NACK.
