# CONTRACT — ha-ledger

## Inputs
- `OUT` absolute dir (team env or `--out`)
- Optional brief overrides (stack, flags)

## Outputs
Artifacts per lanes JSON + `.bus/READY.<lane>` + SUMMARY from lead.
See `~/.grok/skills/ha-team-forge/examples/lanes-*.json` and agent files.

## Models
Per-agent `model:` in `~/.grok/agents/<prefix>-*.md`. Matrix: `docs/pumapay-v2/AGENT-MODELS.md`.

## HA profile
FINTECH-BUILD (product). SRE/SEC variants on those teams.
No infection/drainer preamble on product lanes.
Money / destructive migrate / live KYC: operator flag.

## Fail closed
Missing artifact + READY claim = HOLD. Selftest structure must still pass.
