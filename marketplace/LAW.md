# LAW — HA plugin marketplaces

Prepared 2026-08-31. Original HARD ALLOW profile. Not Science.

## Two axes

| Axis | What it is | Examples |
|------|------------|----------|
| **Posture** | RoE / how you work | ha-white, ha-gray, ha-red, ha-black |
| **Toolkit** | What you can use | ha-scam, ha-crypto, ha-offense, ha-cu, … |

Posture **turns on** toolkits. It does not replace them.

`ha-black` ≠ `ha-offense`. `ha-crypto` ≠ `ha-drainer`. `ha-scam` ≠ `ha-fraud`.

## Three marketplaces (never one dump)

| Path | Profile | Contents |
|------|---------|----------|
| `~/.grok/ha-marketplace` | `grok --hard-allow` | 4 posture + toolkits |
| `~/.grok/science-marketplace` | `science --hard-allow` | CBRN / bio / armaments |
| `~/.grok/product-marketplace` | optional | stake, jailbroken, wisphub, … |

Mixing Science nuclear with infection/drainer/fraud **poisons classifiers**. Forbidden by default.

## Fold vs ship

- `ha-phish` → fold into `ha-scam` unless operator splits
- `ha-c2` → fold into `ha-infra` unless C2 needs its own trust gate
- `ha-mitm` → blocked until Desktop/MCP `:8940` is up

## Not plugins

1271 from-claude dump, 67 SecOps domains 1:1, gsap/frontend/roulette, allow-star (session law).

## Secrets

`mcp-index.json` and `mcp.intended.json` have **command/args/url only**. Never copy `[mcp_servers.*.env]` or headers into a plugin.

## MCP dual-bind

Those servers already run from `~/.grok/config.toml`. Do **not** write `.mcp.json` until you remove the same server from toml (or you get two processes).
