#!/usr/bin/env bash
# PumaPay conductor CLI. Never nested grok -p.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
cmd="${1:-status}"
shift || true
case "$cmd" in
  plan|remainder) exec python3 "$HERE/dispatch.py" "$cmd" "$@" ;;
  verify) exec python3 "$HERE/verify_board.py" "$@" ;;
  watch) exec bash "$HERE/watch.sh" "$@" ;;
  bus-append) exec python3 "$HERE/bus_append.py" "$@" ;;
  selftest)
    echo "=== ha-pumapay selftest ==="
    ERR=0
    for f in dispatch.py verify_board.py watch.sh bus_append.py; do
      if [[ -f "$HERE/$f" ]]; then
        echo "OK script: $f"
      else
        echo "MISSING: $f"; ERR=1
      fi
    done
    for a in pp-lead pp-docs pp-pm pp-qa pp-test pp-dev pp-repo pp-sync; do
      if [[ -f "$HERE/../../../../../agents/${a}.md" || -f "$HOME/.grok/agents/${a}.md" ]]; then
        echo "OK agent: $a"
      else
        echo "MISSING agent: $a"; ERR=1
      fi
    done
    if [[ -f "$HOME/.grok/workflows/ha-pumapay.rhai" ]]; then
      echo "OK workflow: ha-pumapay.rhai"
    else
      echo "MISSING workflow ha-pumapay.rhai"; ERR=1
    fi
    if [[ -f "$HOME/.grok/workflows/ha-pumapay-tick.rhai" ]]; then
      echo "OK workflow: ha-pumapay-tick.rhai"
    else
      echo "MISSING workflow ha-pumapay-tick.rhai"; ERR=1
    fi
    # check skills locations
    if [[ -f "$HOME/.grok/skills/ha-pumapay/scripts/ctl.sh" || -L "$HOME/.grok/skills/ha-pumapay/scripts/ctl.sh" ]]; then
      echo "OK ~/.grok/skills/ha-pumapay/scripts/ctl.sh present"
    else
      echo "MISSING or no symlink in ~/.grok/skills/ha-pumapay/scripts/ctl.sh"; ERR=1
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
      OUT="${PUMAPAY_OUT:-$HOME/Desktop/puma/docs/pumapay-v2}"
    fi
    python3 "$HERE/dispatch.py" plan --out "$OUT"
    wf=$(python3 -c "
import json,sys
p='$OUT/.bus/PLAN.json'
try:
  print(json.load(open(p))['workflow'])
except Exception:
  print('ha-pumapay')
" 2>/dev/null || echo ha-pumapay)
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
      OUT="${PUMAPAY_OUT:-$HOME/Desktop/puma/docs/pumapay-v2}"
    fi
    python3 "$HERE/dispatch.py" remainder --out "$OUT"
    echo "LAUNCH workflow name=ha-pumapay-tick args.out=$OUT"
    ;;
  status)
    OUT="${1:-${PUMAPAY_OUT:-$HOME/Desktop/puma/docs/pumapay-v2}}"
    python3 "$HERE/dispatch.py" status --out "$OUT"
    ;;
  *)
    echo "usage: ctl.sh auto|tick|status|plan|remainder|verify|watch|bus-append|selftest --out DIR" >&2
    exit 2
    ;;
esac
