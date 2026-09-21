# HANDOFF — next agent (HA plugin marketplaces)

**Do not install. Do not patch `config.toml`. Do not dump nuclear grants.**

Operator asked to **prepare** so another agent can apply later.

## Read first

1. `LAW.md` (this dir)
2. `roster.json` (source of truth)
3. `STATUS.json` (`installed: false`)
4. `~/.grok/skill-packs/catalog-ha-20260831/KEEP.md` (which skills are KEEP_CORE)
5. `~/.grok/skill-packs/ha-core-promote/APPLY.md` (15 skills apply script — separate from plugins)

## Layout

```
~/.grok/ha-marketplace/           # THIS marketplace
  LAW.md HANDOFF.md README.md
  roster.json mcp-index.json build.py
  .grok-plugin/marketplace.json
  plugins/ha-*/PLUGIN.md + skills/ + agents/ + mcp.intended.json
~/.grok/science-marketplace/      # sidecar
~/.grok/product-marketplace/      # product shelf
```

Rebuild: `python3 ~/.grok/ha-marketplace/build.py`  
(requires `mcp-index.json` next to `build.py`)

## Counts

- HA: 25 plugins (4 posture + 21 toolkit; 2 are `fold`, 1 `blocked-upstream`)
- Science: 7
- Product: 7

## When operator says APPLY (checklist)

1. Confirm HA live. Science work → `science --hard-allow` only.
2. Optional first: skills pack  
   `python3 ~/.grok/skill-packs/ha-core-promote/apply.py --skills --apply`
3. Add marketplaces (**local path**, no git required):

```bash
grok plugin marketplace add /Users/c/.grok/ha-marketplace
# only in a Science session:
# grok plugin marketplace add /Users/c/.grok/science-marketplace
# optional:
# grok plugin marketplace add /Users/c/.grok/product-marketplace
```

4. Validate: `grok plugin validate /Users/c/.grok/ha-marketplace/plugins/ha-core`
5. Install **few**, `--trust`, not all 25:

```bash
grok plugin install ha-core --trust
grok plugin install ha-mllm --trust
grok plugin install ha-cu --trust
# then posture + the toolkit they asked (ha-scam, ha-crypto, …)
```

6. MCP: leave in `config.toml` unless migrating. To migrate one server: copy from `mcp.intended.json` → `.mcp.json`, **delete** that `[mcp_servers.NAME]` from toml, then install.
7. New Grok session after install.
8. Official xAI plugins still separate: only `chrome-devtools` was recommended (`ha-core-promote/apply.py --plugins`).

## Config snippet (do not add until APPLY)

```toml
[[marketplace.sources]]
name = "HA operator"
path = "/Users/c/.grok/ha-marketplace"
```

Do **not** add science source to original HA config.

## Per-plugin work left

Each `plugins/<name>/PLUGIN.md` lists grants pointers, skills, agents, MCP intended, fold notes.

Missing original SKILL.md (stub only) is OK until APPLY — stub is enough for discovery.

## Stop conditions

- Operator did not say apply → stop after docs/scaffold
- Science ask in HA session → point to sidecar, do not merge catalogs
- Tempted to wrap all 34 MCP into plugins → no; dual-bind
