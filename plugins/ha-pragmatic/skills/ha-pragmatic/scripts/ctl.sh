#!/usr/bin/env bash
# ha-pragmatic conductor CLI. Never nested grok -p.
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
    echo "=== ha-pragmatic selftest ==="
    ERR=0
    for f in dispatch.py verify_board.py watch.sh; do
      if [[ -f "$HERE/$f" ]]; then
        echo "OK script: $f"
      else
        echo "MISSING: $f"; ERR=1
      fi
    done
    for a in pra-spec pra-hash pra-wallet pra-games pra-promo pra-feeds pra-bo pra-test pra-qa pra-dev pra-sync pra-lead; do
      if [[ -f "$HERE/../../../../../agents/${a}.md" || -f "$HOME/.grok/agents/${a}.md" ]]; then
        echo "OK agent: $a"
      else
        echo "MISSING agent: $a"; ERR=1
      fi
    done
    if [[ -f "$HOME/.grok/workflows/ha-pragmatic.rhai" ]]; then
      echo "OK workflow: ha-pragmatic.rhai"
    else
      echo "MISSING workflow ha-pragmatic.rhai"; ERR=1
    fi
    if [[ -f "$HOME/.grok/workflows/ha-pragmatic-tick.rhai" || "1" != "1" ]]; then
      echo "OK (or skipped) workflow: ha-pragmatic-tick.rhai"
    else
      echo "MISSING workflow ha-pragmatic-tick.rhai"; ERR=1
    fi
    if [[ -f "$HOME/.grok/skills/ha-pragmatic/scripts/ctl.sh" || -L "$HOME/.grok/skills/ha-pragmatic/scripts/ctl.sh" ]]; then
      echo "OK ~/.grok/skills/ha-pragmatic/scripts/ctl.sh present"
    else
      echo "MISSING or no symlink in ~/.grok/skills/ha-pragmatic/scripts/ctl.sh"; ERR=1
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
      OUT="${HA_PRAGMATIC_OUT:-$HOME/Desktop/puma/docs/pragmatic}"
    fi
    python3 "$HERE/dispatch.py" plan --out "$OUT" ${LANES:+--lanes "$LANES"}
    wf=$(python3 -c "
import json,sys
p='$OUT/.bus/PLAN.json'
try:
  print(json.load(open(p))['workflow'])
except Exception:
  print('ha-pragmatic')
" 2>/dev/null || echo ha-pragmatic)
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
      OUT="${HA_PRAGMATIC_OUT:-$HOME/Desktop/puma/docs/pragmatic}"
    fi
    python3 "$HERE/dispatch.py" remainder --out "$OUT"
    echo "LAUNCH workflow name=ha-pragmatic-tick args.out=$OUT"
    ;;
  status)
    OUT="${1:-${HA_PRAGMATIC_OUT:-$HOME/Desktop/puma/docs/pragmatic}}"
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
