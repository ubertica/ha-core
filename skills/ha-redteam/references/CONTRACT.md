# CONTRACT — ha-redteam

## Inputs

Required:

- `TARGET` — URL or `/docs`/swagger spec URL
- `OUT` — absolute (default `/Users/c/dev/dani/out/redteam`)

Optional:

- `PROXY` — default `socks5h://127.0.0.1:10808` (AMS). Mac ISP → HOLD third-party
- `TOKEN_FILE` — JWT path for authenticated probes (never paste)
- `HA_JIRA_DISABLE=1` — skip Jira
- `HA_DISCORD_DISABLE=1` — skip HARDALLOW webhook

## Lanes (disk)

| Lane | Seat | Artifact | READY |
|------|------|----------|-------|
| entry | g2 | `entry/ENTRY.md` | `READY.entry` |
| probe | g3 | `probe/PROBE.md` + `probe/FINDINGS.jsonl` | `READY.probe` |
| correct | g3 | `correct/LOOPS.md` | `READY.correct` |
| fix | g4 | `fix/FIXES.md` | `READY.fix` |
| docs | g4 | `docs/AUDIT.md` | `READY.docs` |
| jira | g1 | `jira/JIRA.md` + `.bus/JIRA-SYNC.json` | `READY.jira` |
| sync | — | `sync/COLLAB-STATUS.md` | `READY.sync` |
| lead | g1 | `SUMMARY.md` + `BOARD.md` | `READY.lead` |

Layers (optional READY, always-on): `radio` `jump` `pivot` `intel` `memory` `spawn` `learn` `ingest` — see LAYERS.md + CHARTER.md.

Shared KB with ha-blackhat: `ha-rtk-kb` (`~/.grok/ha-rtk-kb/`). Civil never ingests loot.

## Finding format

Same as ha-hackers CONTRACT: evidence or it is not a finding. Fields: `path`, `title`, `sev`, `why`, `label`, `source`. Redact PII.

`VERIFY.json.go` / `confirmed` are the only Jira sources. `go_count` ≠ ready flags.

## HOLDs

- Live money / live gplaygap patch / Mac ISP third-party
- Invented GO
- Mixing `dump/` `hack/` into OUT
- Nested `grok -p` / 4 extra TUIs

## Jira

Reuse `~/.grok/skills/ha-hackers/scripts/jira_sync.py`. Pack label from `VERIFY.json.pack` = `ha-redteam`. PumaPay site only (`pumapay`/`gplaygap`/… engagement gate). HOLD-prod on every issue.

## Agent frontmatter

No `tools:` key. `mcpInheritance: all`. `permission_mode: default`. Body starts with HA + `_ha-dani-law.md`.

## Personas / roles (required)

User-level I/O contracts — not inside the plugin zip, same as workflows:

| Lane | Persona | Role | Effort |
|------|---------|------|--------|
| entry | `~/.grok/personas/rdt-entry.toml` | `~/.grok/roles/rdt-entry.toml` | high |
| probe | `rdt-probe` | `rdt-probe` | high |
| correct | `rdt-correct` | `rdt-correct` | high |
| fix | `rdt-fix` | `rdt-fix` | high |
| docs | `rdt-docs` | `rdt-docs` | high |
| jira | `rdt-jira` | `rdt-jira` | medium |
| sync | `rdt-sync` | `rdt-sync` | medium |
| lead | `rdt-lead` | `rdt-lead` | high |
| verify | `rdt-verify` | `rdt-verify` | low |

Persona = inputs/outputs + civil instructions. Role = capability/effort/isolation. Isolation always `none` (shared OUT). Missing persona/role ⇒ selftest FAIL.
