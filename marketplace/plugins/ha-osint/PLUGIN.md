# ha-osint

OSINT gateway: crimewall, lusha, grok search MCP.

- **axis:** toolkit
- **status:** scaffold

## Grants (pointer only — do not dump)
- `none`

## Skills to include


## Agents

- `ocl-osint-agent`

## MCP intended (already in config.toml — do not duplicate)

- `crimewall`
- `lusha`
- `grok`

## Next agent
- Do not `grok plugin install` unless operator says.
- Do not copy env/keys into `.mcp.json`.
- Science plugins never install into original HA session.
- If folding (`status: fold`), merge into the target plugin instead of shipping this folder.
