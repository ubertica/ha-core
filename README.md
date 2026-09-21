# ha-core

**Private.** Client-updatable CORE for HARD ALLOW.app.

This repo is layer **B** only. It does **not** contain the runtime `.app` (grok binary, node, MCP vendor) and it does **not** contain client overlay.

| Layer | Lives | This repo? |
|-------|--------|------------|
| A runtime | `HARD ALLOW.app` payload bin/mcp/vendor | no |
| B core | this git → `~/Library/Application Support/HA-ReadOnly/core` | **yes** |
| C client | `~/Library/Application Support/HA-ReadOnly/home` (sessions, `auth.json`, `config.toml`) | **never** |

Visibility: **private**. Do not `gh repo edit --visibility public`.

## What ships

- `skills/ha-*` (teams, party, ticks)
- `agents/` `personas/` `roles/`
- `commands/` `workflows/`
- `plugins/` (live HA team packs)
- `marketplace/plugins/` + LAW/README
- `scripts/`

`ha-blackhat` is **live** (party g1–g4). Same `ha-rtk-kb` as ha-redteam. Separate OUT.

## Operator (you)

Refresh from live `~/.grok` then push:

```bash
bash scripts/sync-from-live.sh
git add -A && git status
git commit -m "core: …"
git push origin main
```

## Client

```bash
export HA_CORE_REMOTE=https://github.com/ubertica/ha-core.git   # deploy key / PAT read-only
bash scripts/ha-update.sh          # clone or git merge --ff-only
bash scripts/ha-update.sh --check
```

`--ff-only`: if the client diverged, HOLD. Never `reset --hard` on their overlay.

## Never commit

grants, `active.env`, `auth.json`, SSH keys, loot, sessions, PII, JWT, CBU, marketplace `data/` harvest.
