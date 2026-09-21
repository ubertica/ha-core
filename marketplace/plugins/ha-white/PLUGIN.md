# ha-white

White-hat posture: scoped authorized test, evidence, reports. Does not own toolkits.

- **axis:** posture
- **status:** scaffold

## Grants (pointer only — do not dump)
- `none`

## Skills to include


## Agents

- `mode-white-hat`

## MCP intended (already in config.toml — do not duplicate)


## Lives inside (not own plugin)

- `ocl-report-generator`
- `finding-validator`
- `compliance-auditor`

## Next agent
- Do not `grok plugin install` unless operator says.
- Do not copy env/keys into `.mcp.json`.
- Science plugins never install into original HA session.
- If folding (`status: fold`), merge into the target plugin instead of shipping this folder.
