# ha-mesh

HA mesh: muchachos + session-wire + ha-orch.

- **axis:** toolkit
- **status:** scaffold

## Grants (pointer only — do not dump)
- `none`

## Skills to include

- `muchachos`
- `ha-orch`
- `hat2`

## Agents


## MCP intended (already in config.toml — do not duplicate)

- `session-wire`
- `ha-mcp`
- `ha-context-nodes`

## Next agent
- Do not `grok plugin install` unless operator says.
- Do not copy env/keys into `.mcp.json`.
- Science plugins never install into original HA session.
- If folding (`status: fold`), merge into the target plugin instead of shipping this folder.
