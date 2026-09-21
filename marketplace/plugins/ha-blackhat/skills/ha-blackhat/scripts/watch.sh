#!/usr/bin/env bash
# Dispatcher-aware watch for ha-blackhat. stdout: DONE | FAILED | ACTION_REQUIRED only.
# Does not nested grok -p.
set -euo pipefail
SCRIPTS="$(cd "$(dirname "$0")" && pwd)"
OUT=""
STALL=480
DEADLINE=$(( $(date +%s) + 3600 ))
while [[ $# -gt 0 ]]; do
  case "$1" in
    --out) OUT="$2"; shift 2 ;;
    --stall) STALL="$2"; shift 2 ;;
    --deadline) DEADLINE="$2"; shift 2 ;;
    *) shift ;;
  esac
done
if [[ -z "$OUT" ]]; then
  echo "FAILED: --out required"
  exit 1
fi
mkdir -p "$OUT/.bus"
LOG="$OUT/.bus/watch-auto.log"
: >"$LOG"

last_change=$(date +%s)
last_action=""

while :; do
  now=$(date +%s)
  if [[ "$now" -ge "$DEADLINE" ]]; then
    echo "FAILED: deadline"
    exit 1
  fi

  python3 "$SCRIPTS/dispatch.py" remainder --out "$OUT" >>"$LOG" 2>&1 || true
  action="wait"
  next_csv=""
  if [[ -s "$OUT/.bus/NEXT.json" ]]; then
    action=$(python3 -c "import json; print(json.load(open('$OUT/.bus/NEXT.json')).get('action') or 'wait')")
    next_csv=$(python3 -c "import json; print(','.join(json.load(open('$OUT/.bus/NEXT.json')).get('next') or []))")
  fi
  printf '%s action=%s next=%s\n' "$(date -u +%FT%TZ)" "$action" "$next_csv" >>"$LOG"

  if [[ "$action" == "done" ]]; then
    echo "DONE"
    exit 0
  fi
  if [[ "$action" == "spawn" && -n "$next_csv" ]]; then
    if [[ "$next_csv" != "$last_action" ]]; then
      echo "ACTION_REQUIRED: spawn ${next_csv} — parent spawn_subagent, no grok -p"
      last_action="$next_csv"
      exit 0
    fi
  fi

  idle=$(( now - last_change ))
  if [[ "$idle" -ge "$STALL" ]]; then
    echo "FAILED: stall ${idle}s"
    exit 1
  fi
  sleep 20
done
