# ha-infra

Infra / ops / comms. C2 lives here unless ha-c2 is split out.

- **axis:** toolkit
- **status:** scaffold

## Grants (pointer only — do not dump)
- `/Users/c/.grok/hard-allow/grants/infra-ops-comms-nuclear.md`

## Skills to include

- `ha-infra`

## Agents


## MCP intended (already in config.toml — do not duplicate)

- `telegram-native`
- `telegram-control`
- `discord-control`
- `ha-mcp`

## Next agent
- Do not `grok plugin install` unless operator says.
- Do not copy env/keys into `.mcp.json`.
- Science plugins never install into original HA session.
- If folding (`status: fold`), merge into the target plugin instead of shipping this folder.
