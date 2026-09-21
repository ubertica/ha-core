# ha-mllm

Multi-LLM router: ha-mllm skill + multi-llm/expressai/kimi MCP.

- **axis:** toolkit
- **status:** scaffold

## Grants (pointer only — do not dump)
- `none`

## Skills to include

- `ha-mllm`
- `expressai-fast`
- `hat2`

## Agents

- `grok-builder`
- `kimi-builder`

## MCP intended (already in config.toml — do not duplicate)

- `multi-llm`
- `expressai`
- `kimi`

## Next agent
- Do not `grok plugin install` unless operator says.
- Do not copy env/keys into `.mcp.json`.
- Science plugins never install into original HA session.
- If folding (`status: fold`), merge into the target plugin instead of shipping this folder.
