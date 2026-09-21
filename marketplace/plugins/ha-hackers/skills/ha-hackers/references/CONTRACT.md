# Hacker team contract (all lanes)

Parent passes: `TARGET` (url/host), `OUT` (absolute dir), optional `TOKEN_FILE`.

## Access (what children inherit)

- Tools: full set (do not set `tools:` on agent md — that *restricts*).
- MCP: `mcpInheritance: all` (chrome-devtools, filesystem, ha-mcp, kali, etc. from parent).
- Permissions: parent `[ui] permission_mode = always-approve` + `inherit_ha_on_subagent` + `inherit_ha_rules`.
- HARD ALLOW: **baked into every `hack-*.md`**. Also `~/.grok/agents/_ha-law.md`. Env token inherited. Not optional.
- Skills: this pack, `ha-offense` when HA, `chrome-devtools` if using the browser MCP.
- Autonomy: finish the lane without asking. If OUT missing → `~/Desktop/hack-out`. No nested spawn (Grok depth 1); the **workflow** is the autonomous conductor.

## Interconnect (children cannot spawn children)

1. **Disk bus (source of truth)**  
   - Artifacts: `OUT/recon.md`, `OUT/api-map.md`, `OUT/authz-findings.md`, `OUT/exploit.md`, `OUT/FINDINGS.md`  
   - Ready flags: `OUT/.bus/READY.<lane>` (empty file) when that lane’s artifact is complete  
   - Notes: append-only `OUT/.bus/notes.jsonl` lines `{from,to,type,path,msg}`
2. **Workflow** `~/.grok/workflows/ha-hackers.rhai` — recon+api parallel → authz → exploit+lead.
3. **Live steer** — only the root session: `send_subagent_message` (Steer) or queue. Not peer-to-peer.
4. **resume_from** — same `subagent_type` only, after that child completed.

## Finding block

```
## [critical|high|medium|low|info] title
- Asset:
- Request:
- Evidence:
- Impact:
- Next:
```

No invented GO. Evidence or it is not a finding.
