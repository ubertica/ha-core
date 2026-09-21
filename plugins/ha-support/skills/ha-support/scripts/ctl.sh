#!/usr/bin/env bash
# ha-support conductor CLI. Never nested grok -p.
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
    echo "=== ha-support selftest ==="
    ERR=0
    for f in dispatch.py verify_board.py watch.sh; do
      if [[ -f "$HERE/$f" ]]; then
        echo "OK script: $f"
      else
        echo "MISSING: $f"; ERR=1
      fi
    done
    for a in sup-triage sup-macros sup-queue sup-qa sup-dev sup-sync sup-lead; do
      if [[ -f "$HERE/../../../../../agents/${a}.md" || -f "$HOME/.grok/agents/${a}.md" ]]; then
        echo "OK agent: $a"
      else
        echo "MISSING agent: $a"; ERR=1
      fi
    done
    if [[ -f "$HOME/.grok/workflows/ha-support.rhai" ]]; then
      echo "OK workflow: ha-support.rhai"
    else
      echo "MISSING workflow ha-support.rhai"; ERR=1
    fi
    if [[ -f "$HOME/.grok/workflows/ha-support-tick.rhai" || "1" != "1" ]]; then
      echo "OK (or skipped) workflow: ha-support-tick.rhai"
    else
      echo "MISSING workflow ha-support-tick.rhai"; ERR=1
    fi
    if [[ -f "$HOME/.grok/skills/ha-support/scripts/ctl.sh" || -L "$HOME/.grok/skills/ha-support/scripts/ctl.sh" ]]; then
      echo "OK ~/.grok/skills/ha-support/scripts/ctl.sh present"
    else
      echo "MISSING or no symlink in ~/.grok/skills/ha-support/scripts/ctl.sh"; ERR=1
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
      OUT="${HA_SUPPORT_OUT:-$HOME/Desktop/puma/docs/support}"
    fi
    python3 "$HERE/dispatch.py" plan --out "$OUT" ${LANES:+--lanes "$LANES"}
    wf=$(python3 -c "
import json,sys
p='$OUT/.bus/PLAN.json'
try:
  print(json.load(open(p))['workflow'])
except Exception:
  print('ha-support')
" 2>/dev/null || echo ha-support)
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
      OUT="${HA_SUPPORT_OUT:-$HOME/Desktop/puma/docs/support}"
    fi
    python3 "$HERE/dispatch.py" remainder --out "$OUT"
    echo "LAUNCH workflow name=ha-support-tick args.out=$OUT"
    ;;
  status)
    OUT="${1:-${HA_SUPPORT_OUT:-$HOME/Desktop/puma/docs/support}}"
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
