#!/usr/bin/env bash
# ha-aml conductor CLI. Never nested grok -p.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
cmd="${1:-status}"
shift || true
case "$cmd" in
  plan|remainder) exec python3 "$HERE/dispatch.py" "$cmd" "$@" ;;
  verify) exec python3 "$HERE/verify_board.py" "$@" ;;
  watch) exec bash "$HERE/watch.sh" "$@" ;;
  bus-append) exec python3 "$HERE/bus_append.py" "$@" 2>/dev/null || echo "bus_append not present" ;;
  selftest)
    echo "=== ha-aml selftest ==="
    ERR=0
    for f in dispatch.py verify_board.py watch.sh; do
      if [[ -f "$HERE/$f" ]]; then
        echo "OK script: $f"
      else
        echo "MISSING: $f"; ERR=1
      fi
    done
    for a in aml-monitor aml-rules aml-cases aml-rating aml-qa aml-dev aml-sync aml-lead; do
      if [[ -f "$HERE/../../../../../agents/${a}.md" || -f "$HOME/.grok/agents/${a}.md" ]]; then
        echo "OK agent: $a"
      else
        echo "MISSING agent: $a"; ERR=1
      fi
    done
    if [[ -f "$HOME/.grok/workflows/ha-aml.rhai" ]]; then
      echo "OK workflow: ha-aml.rhai"
    else
      echo "MISSING workflow ha-aml.rhai"; ERR=1
    fi
    if [[ -f "$HOME/.grok/workflows/ha-aml-tick.rhai" || "1" != "1" ]]; then
      echo "OK (or skipped) workflow: ha-aml-tick.rhai"
    else
      echo "MISSING workflow ha-aml-tick.rhai"; ERR=1
    fi
    if [[ -f "$HOME/.grok/skills/ha-aml/scripts/ctl.sh" || -L "$HOME/.grok/skills/ha-aml/scripts/ctl.sh" ]]; then
      echo "OK ~/.grok/skills/ha-aml/scripts/ctl.sh present"
    else
      echo "MISSING or no symlink in ~/.grok/skills/ha-aml/scripts/ctl.sh"; ERR=1
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
        --lanes) LANES="$2"; shift 2 ;;
        *) shift ;;
      esac
    done
    if [[ -z "$OUT" ]]; then
      OUT="${HA_AML_OUT:-$HOME/Desktop/puma/docs/aml}"
    fi
    python3 "$HERE/dispatch.py" plan --out "$OUT" ${LANES:+--lanes "$LANES"}
    wf=$(python3 -c "
import json,sys
p='$OUT/.bus/PLAN.json'
try:
  print(json.load(open(p))['workflow'])
except Exception:
  print('ha-aml')
" 2>/dev/null || echo ha-aml)
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
      OUT="${HA_AML_OUT:-$HOME/Desktop/puma/docs/aml}"
    fi
    python3 "$HERE/dispatch.py" remainder --out "$OUT"
    echo "LAUNCH workflow name=ha-aml-tick args.out=$OUT"
    ;;
  status)
    OUT="${1:-${HA_AML_OUT:-$HOME/Desktop/puma/docs/aml}}"
    python3 "$HERE/dispatch.py" status --out "$OUT" || true
    ;;
  from-hackers)
    python3 "$HERE/../../../scripts/from_hackers.py" || echo "run from skill root"
    ;;
  *)
    echo "usage: ctl.sh auto|tick|status|plan|remainder|verify|watch|selftest --out DIR [--lanes JSON]" >&2
    exit 2
    ;;
esac
