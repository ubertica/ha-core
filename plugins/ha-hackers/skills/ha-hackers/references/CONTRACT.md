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
2. **Workflow** `~/.grok/workflows/ha-hackers.rhai` — preflight → recon∥api → authz → disk verify → exploit if `go_count>0` + lead.
2b. **Specialized** `~/.grok/workflows/docs-entry.rhai` — same gate; `hack-entry` ∥ `hack-webhook` when TARGET is `/docs`. Addendum: `~/.grok/skills/ha-docs-entry/references/CONTRACT.md`.
2c. **Conductor** `references/AUTONOMY.md` + `scripts/dispatch.py` + workflow `ha-auto`. Skip `READY.*`. Parent launches the workflow. No nested `grok -p`. Prober counts untrusted. `verify_evidence.py` is the only GO source.
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

Discord HARDALLOW: after evidenced critical/medium/GOLD/killchain/pivot, `ha hardallow <kind> --title … --body … --out OUT`. `verify_evidence.py` auto-posts GO. Never echo the webhook URL.
