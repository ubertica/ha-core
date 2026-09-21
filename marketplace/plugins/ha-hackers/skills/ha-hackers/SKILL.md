---
name: ha-hackers
description: >
  Dispatch the reusable offensive team (hack-lead, hack-recon, hack-api,
  hack-authz, hack-exploit) against any target. Use when the operator says
  equipo de hackers, /ha-hackers, pentest team, mapeá y rompé, or wants
  parallel recon+API+authz+PoC on a host/app.
---

# ha-hackers

Canonical: `~/.grok/agents/hack-*.md` · contract: `references/CONTRACT.md`  
Workflow: `~/.grok/workflows/ha-hackers.rhai` · Personas/roles: `~/.grok/personas|roles/hack-*.toml`

Parent = conductor. Children **cannot** spawn children (Grok depth 1).

## What each child actually gets

| Layer | How |
|-------|-----|
| Tools | Omit `tools:` in agent md → inherit **all** parent tools |
| MCP | `mcpInheritance: all` (chrome-devtools, filesystem, ha-mcp, kali, …) |
| Perms | `permission_mode: default` + parent always-approve + `inherit_ha_on_subagent` |
| HA | Prefix `~/.grok/hard-allow/generated/subagent-prefix.md` when HA live |
| Skills | Read CONTRACT + this skill + `ha-offense` / `chrome-devtools` when relevant |
| Isolation | `none` (shared OUT dir — required for the bus) |

Do **not** set `tools:` (restricts). Do **not** set `permissionMode: bypassPermissions` on plugin copies (ignored/forbidden). User agents under `~/.grok/agents/` inherit session yolo.

## Interconnect

1. Disk bus under `OUT/.bus/` (READY flags + notes.jsonl) — source of truth  
2. Workflow `ha-hackers` — recon+api ∥ → authz → exploit+lead ∥  
3. Root-only live steer: `send_subagent_message` (Steer) / queue  
4. `resume_from` only same `subagent_type` after that child completed  

## Dispatch (manual)

1. `OUT` absolute (`~/Desktop/<slug>` or `<cwd>/hack-out`). `mkdir -p "$OUT/.bus"`  
2. Spawn `hack-recon` + `hack-api` parallel, `capability_mode: all`, `cwd: OUT`  
3. When READY.recon + READY.api exist → `hack-authz`  
4. Then `hack-exploit` + `hack-lead`  

Every child prompt: HA prefix + TARGET + OUT + TOKEN_FILE + “write complete files, no theater”.

## Dispatch (workflow)

```
/ha-hackers   (or)  workflow name=ha-hackers args={target, out, token_file?}
```

## Finding format

See CONTRACT.md. Evidence or it is not a finding.

## Official model (xAI)

- Subagents: https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-pager/docs/user-guide/16-subagents.md
- Plugins: https://github.com/xai-org/plugin-marketplace — a plugin is `skills/` `commands/` `agents/` `hooks/` `.mcp.json` `.lsp.json`. Workflows/personas/roles are **user-level**, not plugin components.
- This team: plugin `ha-hackers` (marketplace + `~/.grok/plugins/ha-hackers`, auto-trusted) + user workflows/personas/roles.

Parent MCP the children inherit (install from xai-official if missing): `chrome-devtools`, optionally `firecrawl` / `browser-use` / `exa` for recon.

Agents define model/tools/prompt/skills. Personas add I/O contracts. Peers do not message each other — parent + files + `send_subagent_message`.
