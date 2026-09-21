#!/usr/bin/env bash
# Shared KB CLI for ha-redteam + ha-blackhat. Never dump loot. Never echo secrets.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
KB_PY="$HERE/kb.py"
cmd="${1:-status}"
shift || true
case "$cmd" in
  status|intel|memory|ingest|query|learn)
    exec python3 "$KB_PY" "$cmd" "$@"
    ;;
  search)
    exec python3 "$KB_PY" query "$@"
    ;;
  selftest)
    echo "=== ha-rtk-kb selftest ==="
    ERR=0
    [[ -f "$KB_PY" ]] && echo "OK kb.py" || { echo "MISSING kb.py"; ERR=1; }
    python3 "$KB_PY" status >/tmp/ha-rtk-kb-status.json || { echo "FAIL status"; ERR=1; }
    python3 -c 'import json; json.load(open("/tmp/ha-rtk-kb-status.json"))' && echo "OK status json"
    KB="${HA_RTK_KB:-$HOME/.grok/ha-rtk-kb}"
    [[ -d "$KB" ]] && echo "OK disk $KB" || { echo "MISSING $KB"; ERR=1; }
    if [[ $ERR -eq 0 ]]; then
      echo "SELftest PASS"
      exit 0
    fi
    echo "SELftest FAIL"
    exit 1
    ;;
  *)
    echo "usage: ctl.sh status|intel|memory|ingest|query|learn|search|selftest --pack ha-redteam|ha-blackhat --out DIR" >&2
    exit 2
    ;;
esac
