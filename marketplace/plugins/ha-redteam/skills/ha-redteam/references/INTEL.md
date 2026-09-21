# INTEL — public knowledge (no invented CVE)

Query, cite, match to disk stack. Fail-open if a feed is down.

| Feed | Use |
|------|-----|
| CISA KEV | known exploited — `https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json` |
| NVD 2.0 | keyword/CPE — `https://services.nvd.nist.gov/rest/json/cves/2.0` |
| OSV | package/ecosystem — `https://api.osv.dev/v1/query` |
| GHSA | GitHub Advisories API |
| Exploit-DB / searchsploit | local if Kali; else public search — **cite**, don’t paste exploits into product OUT |
| from-claude-pack | `~/.grok/skills/from-claude-pack/` pentest catalog (~1271) |
| ha-context-nodes | prior HA facts (`nodes_search`) |

**Shared with ha-blackhat:** `~/.grok/skills/ha-rtk-kb/` + disk `~/.grok/ha-rtk-kb/`. Do not keep a private KEV copy.

SOCKS AMS. Fail-open. Match tech on disk only.
