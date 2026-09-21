---
name: ha-upgrade
description: >
  Pack each /learn (or session self-improvement) into a new versioned HA
  upgrade plugin (ha-upgrade-vN). Never overwrite a prior version. Never
  auto-install. Use when the operator says /ha-upgrade, plugin de upgrade,
  upgrade plugin, cada version, pack learn, version bump, "congelá el learn
  en un plugin", or after a /learn report is ready and they want a shippable
  upgrade pack. Do not use for forging a new team (ha-team-forge) or for
  Science/CBRN marketplace.
---

# ha-upgrade

Turn agentic self-improvement into a **frozen plugin per version**.

Loop:

```
/learn (report + actions.json)
  → /ha-upgrade pack
  → ~/.grok/ha-marketplace/plugins/ha-upgrade-vN/
  → operator GO
  → apply vN
  → next /learn --since-last
  → pack vN+1  (new folder)
```

`/learn` finds what to change. This skill **ships that change as a plugin**. Installing is a separate, explicit step.

## When packing

1. Resolve source:
   - `--run-dir` if given
   - else last completed `/learn` dir from `~/.grok/learn/state.json`
   - else `--notes` (operator text)
2. Allocate **next integer version**. Never reuse. Never write into an existing `ha-upgrade-v*`.
3. Run:

```bash
python3 ~/.grok/skills/ha-upgrade/scripts/pack.py pack [--run-dir PATH] [--notes TEXT_OR_FILE]
python3 ~/.grok/skills/ha-upgrade/scripts/pack.py selftest --version N
```

4. Show the operator: plugin path, action count, `installed: false`.
5. Stop. Do not `grok plugin install`. Do not apply without `--go`.

## Apply / rollback

```bash
python3 ~/.grok/skills/ha-upgrade/scripts/pack.py apply --version N --go
python3 ~/.grok/skills/ha-upgrade/scripts/pack.py rollback --version N --go
```

Without `--go` the script HOLDs. Skip `requires_confirmation` actions (same consent as `/learn` step 4).

## Shape of each plugin

Matches HA marketplace (see `~/.grok/ha-marketplace/LAW.md`):

- `plugin.json` · `PLUGIN.md`
- `skills/ha-upgrade-vN/SKILL.md`
- `references/actions.json` (redacted) · `CHANGELOG.md` · `manifest.json`
- `commands/ha-upgrade-vN.md`
- `scripts/apply.py`

No env, no tokens, no `auth.json`, no Science nuclear. `mcp.intended` stays empty unless the operator named an MCP in the learn actions.

## Registry

`~/.grok/hard-allow/upgrade/registry.json` is the version SoT (`current`, list of packed plugins). `pack.py next` prints it.

## Do not

- Overwrite vN to make vN+1
- Mix this pack into `science-marketplace`
- Dump grant blobs into CHANGELOG
- Install because packing succeeded
- Call this `ha-team-forge` (that forges teams, not version upgrades)
