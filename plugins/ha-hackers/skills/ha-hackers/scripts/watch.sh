#!/usr/bin/env bash
# Dispatcher-aware watch. stdout: DONE | FAILED | ACTION_REQUIRED only.
# Does not nested grok -p. Writes NEXT.json; parent TUI spawns those types.
set -euo pipefail
SCRIPTS="$(cd "$(dirname "$0")" && pwd)"
OUT=""
PACK="docs-entry"
STALL=480
DEADLINE=$(( $(date +%s) + 3600 ))
TARGET=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --out) OUT="$2"; shift 2 ;;
    --pack) PACK="$2"; shift 2 ;;
    --stall) STALL="$2"; shift 2 ;;
    --deadline) DEADLINE="$2"; shift 2 ;;
    --target) TARGET="$2"; shift 2 ;;
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

jsonl_mtime() {
  local m=0 t f
  shopt -s nullglob
  for f in "$OUT"/docs-entry/*.jsonl "$OUT"/*.jsonl "$OUT"/OUT/docs-entry/*.jsonl; do
    t=$(stat -f %m "$f" 2>/dev/null || stat -c %Y "$f" 2>/dev/null || echo 0)
    if [[ "$t" -gt "$m" ]]; then m=$t; fi
  done
  echo "$m"
}

last_jsonl=0
last_change=$(date +%s)
last_action=""

while :; do
  now=$(date +%s)
  if [[ "$now" -ge "$DEADLINE" ]]; then
    echo "FAILED: deadline"
    exit 1
  fi

  python3 "$SCRIPTS/dispatch.py" remainder --out "$OUT" --pack "$PACK" --target "$TARGET" >>"$LOG" 2>&1 || true
  action="wait"
  next_csv=""
  n_go=0
  if [[ -s "$OUT/.bus/NEXT.json" ]]; then
    action=$(python3 -c "import json; print(json.load(open('$OUT/.bus/NEXT.json')).get('action') or 'wait')")
    next_csv=$(python3 -c "import json; print(','.join(json.load(open('$OUT/.bus/NEXT.json')).get('next') or []))")
    n_go=$(python3 -c "import json; print(int(json.load(open('$OUT/.bus/NEXT.json')).get('go_count') or 0))")
  fi
  printf '%s action=%s next=%s go=%s\n' "$(date -u +%FT%TZ)" "$action" "$next_csv" "$n_go" >>"$LOG"

  if [[ -f "$OUT/.bus/TOKEN.stale" && "$PACK" == "ha-hackers" ]]; then
    echo "ACTION_REQUIRED: token_stale — run session_guard --need-token --origin <spa>"
    exit 0
  fi

  jm=$(jsonl_mtime)
  if [[ "$jm" -gt "$last_jsonl" ]]; then
    last_jsonl=$jm
    last_change=$now
  fi

  # Open workstreams override pack-lane DONE (HF-bar: impossible ≠ fin)
  if [[ "$action" == "done" && -s "$OUT/.bus/WORKSTREAMS.jsonl" ]]; then
    python3 "$SCRIPTS/workstream.py" next --out "$OUT" >>"$LOG" 2>&1 || true
    if [[ -s "$OUT/.bus/WORKSTREAMS.next.json" ]]; then
      ws_action=$(python3 -c "import json; print(json.load(open('$OUT/.bus/WORKSTREAMS.next.json')).get('action') or 'done')")
      ws_next=$(python3 -c "import json; print(','.join(json.load(open('$OUT/.bus/WORKSTREAMS.next.json')).get('next') or []))")
      if [[ "$ws_action" == "spawn" && -n "$ws_next" ]]; then
        action="spawn"
        next_csv="$ws_next"
      fi
    fi
  fi

  case "$action" in
    done)
      python3 "$SCRIPTS/verify_evidence.py" --out "$OUT" --pack "$PACK" >>"$LOG" 2>&1 || true
      python3 "$SCRIPTS/jira_sync.py" --out "$OUT" --notify >>"$LOG" 2>&1 || true
      echo "DONE"
      exit 0
      ;;
    need-token)
      echo "ACTION_REQUIRED: token_stale — run session_guard --need-token --origin <spa>"
      exit 0
      ;;
    spawn)
      # Re-plan after probe lanes complete so verify runs before exploit ticket
      if [[ "$PACK" == "docs-entry" ]]; then
        e=0; w=0
        [[ -f "$OUT/.bus/READY.entry" ]] && e=1
        [[ -f "$OUT/.bus/READY.webhook" ]] && w=1
        if [[ "$e" = 1 && "$w" = 1 ]]; then
          python3 "$SCRIPTS/verify_evidence.py" --out "$OUT" --pack "$PACK" >>"$LOG" 2>&1 || true
          python3 "$SCRIPTS/jira_sync.py" --out "$OUT" --notify >>"$LOG" 2>&1 || true
          python3 "$SCRIPTS/dispatch.py" remainder --out "$OUT" --pack "$PACK" --target "$TARGET" >>"$LOG" 2>&1 || true
          action=$(python3 -c "import json; print(json.load(open('$OUT/.bus/NEXT.json')).get('action') or 'wait')")
          next_csv=$(python3 -c "import json; print(','.join(json.load(open('$OUT/.bus/NEXT.json')).get('next') or []))")
          n_go=$(python3 -c "import json; print(int(json.load(open('$OUT/.bus/NEXT.json')).get('go_count') or 0))")
        fi
      elif [[ "$PACK" == "ha-hackers" && -f "$OUT/.bus/READY.authz" ]]; then
        python3 "$SCRIPTS/verify_evidence.py" --out "$OUT" --pack "$PACK" >>"$LOG" 2>&1 || true
        python3 "$SCRIPTS/jira_sync.py" --out "$OUT" --notify >>"$LOG" 2>&1 || true
        python3 "$SCRIPTS/dispatch.py" remainder --out "$OUT" --pack "$PACK" --target "$TARGET" >>"$LOG" 2>&1 || true
        action=$(python3 -c "import json; print(json.load(open('$OUT/.bus/NEXT.json')).get('action') or 'wait')")
        next_csv=$(python3 -c "import json; print(','.join(json.load(open('$OUT/.bus/NEXT.json')).get('next') or []))")
        n_go=$(python3 -c "import json; print(int(json.load(open('$OUT/.bus/NEXT.json')).get('go_count') or 0))")
      fi
      if [[ "$action" == "done" || -z "$next_csv" ]]; then
        python3 "$SCRIPTS/jira_sync.py" --out "$OUT" --notify >>"$LOG" 2>&1 || true
        echo "DONE"
        exit 0
      fi
      if [[ "$next_csv" != "$last_action" ]]; then
        echo "ACTION_REQUIRED: spawn ${next_csv} (go_count=${n_go}) — parent spawn_subagent, no grok -p"
        last_action="$next_csv"
        exit 0
      fi
      ;;
  esac

  idle=$(( now - last_change ))
  if [[ "$idle" -ge "$STALL" && "$last_jsonl" -gt 0 ]]; then
    echo "FAILED: stall ${idle}s no jsonl growth"
    exit 1
  fi
  sleep 20
done
