# ha-payments

Grok plugin (marketplace layout): `agents/`, `skills/`, `commands/`.

User-level:

- `$GROK_HOME/workflows/ha-payments.rhai` (+ `-tick`)
- `$GROK_HOME/agents/pay-*.md`
- `$GROK_HOME/skills/ha-payments/`

Children inherit the **parent** MCP. This plugin does not ship `.mcp.json`.

Install: `equipos/install.sh` (symlinks into `$GROK_HOME`).

Runtime (not forge):

```bash
source "$PUMAPAY_ROOT/equipos/lib/paths.sh"
bash "$GROK_HOME/skills/ha-payments/scripts/ctl.sh" auto --out "$HA_PAYMENTS_OUT"
bash "$GROK_HOME/skills/ha-payments/scripts/ctl.sh" selftest
```

OUT default: `$PUMAPAY_OUT/payments`.
Purpose: PumaPay payments: CORE-SURFACE rails, sandbox PSP, signed webhooks.
