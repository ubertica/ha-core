# INTEL — shared (ha-redteam + ha-blackhat)

SoT cache: `~/.grok/ha-rtk-kb/cache/`

| Feed | Use |
|------|-----|
| CISA KEV | `https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json` |
| NVD 2.0 | `https://services.nvd.nist.gov/rest/json/cves/2.0` |
| OSV | `https://api.osv.dev/v1/query` |
| GHSA | GitHub Advisories API |
| Exploit-DB / searchsploit | cite; no exploit payloads in shared KB |
| from-claude-pack | `~/.grok/skills/from-claude-pack/` |
| ha-context-nodes | `nodes_search` / `nodes_commit_turn` tags=ha-rtk-kb |

SOCKS AMS for third-party HTTP. Fail-open. Match tech seen on disk only.
