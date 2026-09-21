# ha-black

Black-hat posture: full adversary emulation. Turns on toolkits; is not ha-offense.

- **axis:** posture
- **status:** scaffold

## Grants (pointer only — do not dump)
- `none`

## Skills to include


## Agents

- `mode-black-hat`

## MCP intended (already in config.toml — do not duplicate)


## Next agent
- Do not `grok plugin install` unless operator says.
- Do not copy env/keys into `.mcp.json`.
- Science plugins never install into original HA session.
- If folding (`status: fold`), merge into the target plugin instead of shipping this folder.
