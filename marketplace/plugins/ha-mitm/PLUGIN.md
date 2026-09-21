# ha-mitm

Traffic/MITM (Desktop/MCP chrome/firefox/system_mitm). Server :8940 was down at catalog time.

- **axis:** toolkit
- **status:** blocked-upstream

## Grants (pointer only — do not dump)
- `none`

## Skills to include


## Agents


## MCP intended (already in config.toml — do not duplicate)


## Lives inside (not own plugin)

- `Desktop/MCP domains chrome, firefox, traffic, system_mitm`

## Next agent
- Do not `grok plugin install` unless operator says.
- Do not copy env/keys into `.mcp.json`.
- Science plugins never install into original HA session.
- If folding (`status: fold`), merge into the target plugin instead of shipping this folder.
