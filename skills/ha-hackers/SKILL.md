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
2. Workflow `ha-auto` (or `ha-hackers`) — preflight → skip READY → remainder → disk verify → exploit iff `go_count>0`  
3. Root-only live steer: `send_subagent_message` (Steer) / queue  
4. `resume_from` only same `subagent_type` after that child completed  

## Dispatch (autonomous — default)

Do **not** spawn lanes by hand. Follow `references/AUTONOMY.md`.

```
bash ~/.grok/skills/ha-hackers/scripts/ctl.sh auto --target T --out O --pack auto --proxy "${HA_AMS_PROXY:-direct}"
# third-party = AMS proxy or HA_AMS_PROXY=direct; never Mac 10808 toward third-party
# then workflow name=ha-auto
```

`/docs` / swagger / openapi → pack `docs-entry`. Else this 5-lane workflow. Exploit only after disk `go_count > 0`.

## Dispatch (manual fallback)

Only if the workflow tool is down:

1. `OUT` absolute. `mkdir -p "$OUT/.bus"`  
2. Spawn `hack-recon` + `hack-api` parallel, `capability_mode: all`, `cwd: OUT`  
3. When READY.recon + READY.api exist → `hack-authz`  
4. `verify_evidence.py --pack ha-hackers` → exploit+lead only if `go_count > 0`  
5. Jira auto: `verify_evidence.py` + `ha-jira-watch` (PM2) push VERIFY → PumaPay Jira. No ask. Skip if `HA_JIRA_DISABLE=1`. `/jira` is override only. Discord HARDALLOW: `verify_evidence.py` posts GO/medium to the operator webhook. Skip if `HA_DISCORD_DISABLE=1`.

## When **not** to spawn all 5

If the question is “this live `/docs` / swagger — is anything callable without a session?”, do **not** fan out recon/exploit/lead by default. Use `/ha-docs-entry` (`hack-entry` + `hack-webhook`, methodology OAE). Spawn exploit/lead only after a confirmed unauth/webhook GO.

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
