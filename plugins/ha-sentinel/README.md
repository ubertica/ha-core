# ha-sentinel

Autonomous sentinel team for AMS perimeter + ollama-ha judgment. Feeds ha-pumapay via bus.

## Usage

```
# Full run (watch∥ollama → audit∥improve → release → escalate∥collab → lead)
bash ~/.grok/skills/ha-sentinel/scripts/ctl.sh auto \
  --out "${SENTINEL_OUT:-$HOME/Desktop/puma/docs/pumapay-v2/sentinel}"

# then launch
workflow name=ha-sentinel args.out=...

# Periodic tick (remainder + escalate/collab + lead)
bash ~/.grok/skills/ha-sentinel/scripts/ctl.sh tick --out "$OUT"
workflow name=ha-sentinel-tick args.out=...

# Direct AMS
bash ~/.grok/skills/ha-sentinel/scripts/ctl.sh ams-mirror --out "$OUT"
bash ~/.grok/skills/ha-sentinel/scripts/ctl.sh ollama-ask "status of sentinel god"
```

## Lanes (via workflow + dispatch)

- sent-watch: perimeter + ams-mirror of sentinel-god
- sent-ollama: ollama-ha status + ask via ctl
- sent-audit: evidence audit
- sent-improve: improvement proposals
- sent-release: release notes
- sent-escalate: high/crit to pumapay-bus
- sent-collab: bus exchange
- sent-lead: SUMMARY always
