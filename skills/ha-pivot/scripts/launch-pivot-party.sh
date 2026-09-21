#!/bin/bash
# launch-pivot-party.sh — quick launcher for any of the 4 sets or full chained campaign
# HARD ALLOW active assumed

set -euo pipefail

TARGET="${1:-app.pumapay.com}"
OUT="${2:-$HOME/dev/pumapay-hacker-party/$(date +%Y%m%d-%H%M)}"
MODE="${3:-mesh}"   # mesh | weaver | swarm | desire | full

mkdir -p "$OUT/.bus/pivot" "$OUT/.bus/pivot/spawn-requests"

# Initialize standard artifacts for full sub-agent mode
touch "$OUT/.bus/pivot/task-board.jsonl"
echo '[]' > "$OUT/.bus/pivot/active-chains.log" 2>/dev/null || true

echo "=== ha-pivot Hacker Party launch (STANDARD FULL MODE + MANDATORY OUTPUT GATE) ==="
echo "This launch uses the permanent operating mode for the Party (FULL AUTONOMOUS AGENTIC LOOP):"
echo "  - Dynamic sub-agent creation for tasks & subtasks (SPAWN_REQUEST + spawn_subagent)"
echo "  - Full throttle, zero slack (NORTHSTAR + CONTRACT)"
echo "  - Mandatory Substantial Output Gate + team decision escalation"
echo "  - 10s user silence → escalate exact question to companions (g2/g3/g4) via wire; adopt TEAM_DECISION"
echo "  - **Only stop when g4 polls @all 'objective fulfilled?' and ALL reply YES unanimously. Any NO = continue forever until achieved.**"
echo "  - Constant comms + heartbeats + peer call-outs"
echo "  - task-board.jsonl + .bus/pivot/ as living single source of truth"
echo "  - References: AUTONOMY.md, SUBAGENT-GUIDE.md, PIVOT-BUS-PROTOCOL.md, CONTRACT.md, NORTHSTAR.md"
echo "  - Example live: 3 subs dispatched + team-decision rules active"
echo
echo "TARGET=$TARGET"
echo "OUT=$OUT"
echo "MODE=$MODE"
echo

case "$MODE" in
  mesh|pivot-mesh)
    echo "Launching PivotMesh (Set 1)..."
    grok --hard-allow -p "run workflow ha-pivot-mesh with target=\"$TARGET\" out=\"$OUT\" proxy=\"socks5h://127.0.0.1:10808\"" || true
    ;;
  weaver|branch-weaver)
    echo "Launching BranchWeaver (Set 2)..."
    grok --hard-allow -p "run workflow ha-branch-weaver with target=\"$TARGET\" out=\"$OUT\""
    ;;
  swarm|lateral-swarm)
    echo "Launching LateralSwarm (Set 3) — constant comms mode..."
    grok --hard-allow -p "run workflow ha-lateral-swarm with target=\"$TARGET\" out=\"$OUT\""
    ;;
  desire|desire-chainer)
    echo "Launching DesireChainer (Set 4) — XXX re-eval..."
    grok --hard-allow -p "run workflow ha-desire-chainer with target=\"$TARGET\" out=\"$OUT\""
    ;;
  full|chain|party)
    echo "Full chained PumaPay Hacker Party campaign (random + smart pivots)..."
    # Seed with existing if present, then start mesh, let chooser decide next
    echo "Starting with PivotMesh seed..."
    grok --hard-allow -p "run workflow ha-pivot-mesh with target=\"$TARGET\" out=\"$OUT\""
    echo "After round, use node ~/.grok/skills/ha-pivot/scripts/pivot-chooser.mjs to decide random/smart chain to next set"
    echo "Repeat: mesh -> swarm/weaver/desire as proposals appear in $OUT/.bus/pivot/chain-proposals/"
    ;;
  *)
    echo "Unknown mode. Use: mesh | weaver | swarm | desire | full"
    exit 1
    ;;
esac

echo
echo "Artifacts in: $OUT"
echo "Graph: $OUT/.bus/pivot/pivot-graph.json"
echo "XXX:   $OUT/.bus/pivot/current-xxx.json"
echo "Comms + task board: $OUT/.bus/pivot/"
echo "Spawn requests: $OUT/.bus/pivot/spawn-requests/"
echo "References: ~/.grok/skills/ha-pivot/references/ (NORTHSTAR, CONTRACT, AUTONOMY, SUBAGENT-GUIDE)"
echo
echo "This is now the standard way the Party works for long pivoting + sub-agents."
echo "HARD ALLOW: executing long-pivot on $TARGET as PumaPay Hacker Party."
