#!/usr/bin/env bash
# ha-pp-consensus conductor CLI
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
BUS="${PUMAPAY_CONSENSUS_BUS:-$HOME/.grok/pumapay-bus/consensus}"
REPO="${PPDEV_OUT:-$HOME/dev/pumapay}"
cmd="${1:-status}"
shift || true

mkdir -p "$BUS/proposals" "$BUS/decisions"

case "$cmd" in
  propose)
    exec python3 "$HERE/consensus.py" propose --bus "$BUS" --repo "$REPO" "$@"
    ;;
  auto|run)
    ID=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --id) ID="$2"; shift 2 ;;
        *) shift ;;
      esac
    done
    [[ -n "$ID" ]] || { echo "need --id"; exit 2; }
    python3 "$HERE/consensus.py" plan --bus "$BUS" --id "$ID"
    echo "LAUNCH workflow name=ha-pp-consensus args.id=$ID args.bus=$BUS args.repo=$REPO"
    ;;
  verify)
    exec python3 "$HERE/consensus.py" verify --bus "$BUS" "$@"
    ;;
  status)
    exec python3 "$HERE/consensus.py" status --bus "$BUS" "$@"
    ;;
  selftest)
    echo "=== ha-pp-consensus selftest ==="
    ERR=0
    for f in consensus.py ctl.sh; do
      [[ -f "$HERE/$f" ]] && echo "OK $f" || { echo "MISSING $f"; ERR=1; }
    done
    [[ -f "$HOME/.grok/workflows/ha-pp-consensus.rhai" ]] && echo "OK workflow" || { echo "MISSING workflow"; ERR=1; }
    [[ -f "$BUS/CONSENSUS.md" ]] && echo "OK protocol" || { echo "MISSING CONSENSUS.md"; ERR=1; }
    [[ -f "$HOME/.grok/agents/pp-docs.md" ]] && echo "OK pp-docs" || ERR=1
    [[ -f "$HOME/.grok/agents/ppd-arch.md" ]] && echo "OK ppd-arch" || ERR=1
    [[ $ERR -eq 0 ]] && echo "SELftest PASS" && exit 0 || { echo "SELftest FAIL"; exit 1; }
    ;;
  *)
    echo "usage: ctl.sh propose|auto|verify|status|selftest [--id ID]" >&2
    exit 2
    ;;
esac
