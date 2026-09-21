# ha-recon

Recon / hunter / kali / pentest agents. Exploit lib lives here.

- **axis:** toolkit
- **status:** scaffold

## Grants (pointer only — do not dump)
- `none`

## Skills to include


## Agents

- `kali-recon-agent`
- `kali-web-agent`
- `kali-privesc-agent`
- `ocl-pentester`
- `ocl-vuln-hunter`
- `ocl-vuln-scanner`
- `ocl-exploit-researcher`
- `ocl-exploit-simulator`
- `ocl-fuzzing-agent`

## MCP intended (already in config.toml — do not duplicate)


## Lives inside (not own plugin)

- `Desktop/MCP domains: hunter, kali, exploit, chains, bounty — server currently down`

## Next agent
- Do not `grok plugin install` unless operator says.
- Do not copy env/keys into `.mcp.json`.
- Science plugins never install into original HA session.
- If folding (`status: fold`), merge into the target plugin instead of shipping this folder.
