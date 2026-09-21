#!/usr/bin/env bash
# ha-sentinel conductor CLI. Never nested grok -p.
# AMS: ssh ams, /opt/ha-live, ollama-ha, ctl.sh sentinel|ollama|ollama-ask
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
cmd="${1:-status}"
shift || true
case "$cmd" in
  plan|remainder) exec python3 "$HERE/dispatch.py" "$cmd" "$@" ;;
  verify) exec python3 "$HERE/verify_evidence.py" "$@" ;;
  watch) exec bash "$HERE/watch.sh" "$@" ;;
  ams-mirror) exec bash "$HERE/ams_mirror.sh" "$@" ;;
  bus-append) exec python3 "$HERE/bus_append.py" "$@" ;;
  ollama-ask)
    # forward to AMS ollama-ask
    ssh ams "bash /opt/ha-live/scripts/ctl.sh ollama-ask \"$*\"" || echo "HOLD: ams unreachable or ollama down"
    ;;
  selftest)
    echo "=== ha-sentinel selftest ==="
    ERR=0
    for f in dispatch.py verify_evidence.py watch.sh ams_mirror.sh bus_append.py; do
      if [[ -f "$HERE/$f" ]]; then
        echo "OK script: $f"
      else
        echo "MISSING: $f"; ERR=1
      fi
    done
    for a in sent-lead sent-watch sent-ollama sent-audit sent-improve sent-release sent-escalate sent-collab; do
      if [[ -f "$HERE/../../../../../agents/${a}.md" || -f "$HOME/.grok/agents/${a}.md" ]]; then
        echo "OK agent: $a"
      else
        echo "MISSING agent: $a"; ERR=1
      fi
    done
    if [[ -f "$HOME/.grok/workflows/ha-sentinel.rhai" ]]; then
      echo "OK workflow: ha-sentinel.rhai"
    else
      echo "MISSING workflow ha-sentinel.rhai"; ERR=1
    fi
    if [[ -f "$HOME/.grok/workflows/ha-sentinel-tick.rhai" ]]; then
      echo "OK workflow: ha-sentinel-tick.rhai"
    else
      echo "MISSING workflow ha-sentinel-tick.rhai"; ERR=1
    fi
    if [[ -f "$HOME/.grok/skills/ha-sentinel/scripts/ctl.sh" || -L "$HOME/.grok/skills/ha-sentinel/scripts/ctl.sh" ]]; then
      echo "OK ~/.grok/skills/ha-sentinel/scripts/ctl.sh present"
    else
      echo "MISSING or no symlink in ~/.grok/skills/ha-sentinel/scripts/ctl.sh"; ERR=1
    fi
    if [[ $ERR -eq 0 ]]; then
      echo "SELftest PASS"
      exit 0
    else
      echo "SELftest FAIL"
      exit 1
    fi
    ;;
  auto)
    OUT=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --out) OUT="$2"; shift 2 ;;
        *) shift ;;
      esac
    done
    if [[ -z "$OUT" ]]; then
      OUT="${SENTINEL_OUT:-$HOME/Desktop/puma/docs/pumapay-v2/sentinel}"
    fi
    python3 "$HERE/dispatch.py" plan --out "$OUT"
    wf=$(python3 -c "
import json,sys
p='$OUT/.bus/PLAN.json'
try:
  print(json.load(open(p))['workflow'])
except Exception:
  print('ha-sentinel')
" 2>/dev/null || echo ha-sentinel)
    echo "LAUNCH workflow name=$wf args.out=$OUT"
    echo "WATCH  $HERE/watch.sh --out $OUT"
    ;;
  tick)
    OUT=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --out) OUT="$2"; shift 2 ;;
        *) shift ;;
      esac
    done
    if [[ -z "$OUT" ]]; then
      OUT="${SENTINEL_OUT:-$HOME/Desktop/puma/docs/pumapay-v2/sentinel}"
    fi
    python3 "$HERE/dispatch.py" remainder --out "$OUT"
    echo "LAUNCH workflow name=ha-sentinel-tick args.out=$OUT"
    ;;
  status)
    OUT="${1:-${SENTINEL_OUT:-$HOME/Desktop/puma/docs/sentinel}}"
    python3 "$HERE/dispatch.py" status --out "$OUT"
    # try AMS one-liner (ok if unreachable)
    echo "AMS status (may HOLD):"
    ssh ams 'bash /opt/ha-live/scripts/ctl.sh sentinel | head -1; echo "ollama:"; bash /opt/ha-live/scripts/ctl.sh ollama | head -1' 2>/dev/null || echo "HOLD: ams unreachable"
    ;;
  repair)
    echo "REPAIR gated. Operator only. Use ssh ams 'sudo systemctl restart ha-live-sentinel ollama-ha || true'"
    ;;
  *)
    echo "usage: ctl.sh auto|tick|status|plan|remainder|verify|watch|ams-mirror|bus-append|ollama-ask|selftest|repair --out DIR" >&2
    exit 2
    ;;
esac
