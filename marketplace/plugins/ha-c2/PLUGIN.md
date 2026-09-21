# ha-c2

FOLD into ha-infra by default. Split only if C2 surface needs its own trust gate.

- **axis:** toolkit
- **status:** fold

## Grants (pointer only — do not dump)
- `none`

## Skills to include


## Agents


## MCP intended (already in config.toml — do not duplicate)


## Next agent
- Do not `grok plugin install` unless operator says.
- Do not copy env/keys into `.mcp.json`.
- Science plugins never install into original HA session.
- If folding (`status: fold`), merge into the target plugin instead of shipping this folder.
