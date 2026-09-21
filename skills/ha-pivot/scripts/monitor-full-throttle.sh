#!/bin/bash
# monitor-full-throttle.sh — quick checker that the Party is working at full capacity
# Run periodically or from inside agents

OUT=${1:-.}
BUS="$OUT/.bus/pivot"

echo "=== ha-pivot Full-Throttle Monitor ==="
echo "OUT: $OUT"

if [ -f "$BUS/comms.jsonl" ]; then
  LAST=$(tail -1 "$BUS/comms.jsonl" 2>/dev/null)
  echo "Last comms: $LAST"
else
  echo "No comms.jsonl yet"
fi

if [ -f "$BUS/task-board.jsonl" ]; then
  OPEN=$(grep -c '"status":"open"' "$BUS/task-board.jsonl" 2>/dev/null || echo 0)
  INPROG=$(grep -c '"status":"in_progress"' "$BUS/task-board.jsonl" 2>/dev/null || echo 0)
  echo "Task board: $OPEN open, $INPROG in progress"
fi

SPAWNS=$(ls "$BUS/spawn-requests/" 2>/dev/null | wc -l)
echo "Spawn requests pending: $SPAWNS"

echo
echo "Check for recent heartbeats and self-reviews in comms."
echo "If long silence or many open tasks with no progress → spawn more subs or call out."
