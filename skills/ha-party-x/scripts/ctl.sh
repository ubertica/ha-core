#!/usr/bin/env bash
# ha-party-x conductor CLI. Never nested grok -p.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
cmd="${1:-status}"
shift || true
case "$cmd" in
  list) exec python3 "$HERE/run.py" list ;;
  plan) exec python3 "$HERE/run.py" plan "$@" ;;
  status|remainder) exec python3 "$HERE/run.py" remainder "$@" ;;
  prompt) exec python3 "$HERE/run.py" prompt "$@" ;;
  mark-ready) exec python3 "$HERE/run.py" mark-ready "$@" ;;
  preflight) exec python3 "$HERE/run.py" preflight "$@" ;;
  verify) exec python3 "$HERE/run.py" verify "$@" ;;
  brain) exec node "$HERE/party_brain.mjs" "$@" ;;
  selftest) exec python3 "$HERE/selftest.py" "$@" ;;
  auto)
    OUT="" TARGET="" PIPE="apt-long"
    PROXY="${HA_PROXY:-socks5h://127.0.0.1:10808}"
    TOKEN="" MONEY=0
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --out) OUT="$2"; shift 2 ;;
        --target) TARGET="$2"; shift 2 ;;
        --pipeline) PIPE="$2"; shift 2 ;;
        --proxy) PROXY="$2"; shift 2 ;;
        --token-file) TOKEN="$2"; shift 2 ;;
        --allow-money-write) MONEY=1; shift ;;
        *) shift ;;
      esac
    done
    if [[ -z "$OUT" || -z "$TARGET" ]]; then
      echo "usage: ctl.sh auto --target URL --out DIR [--pipeline apt-long|0day-deep|authz-brutal|docs-entry-x|red-on-red]" >&2
      exit 2
    fi
    extra=()
    [[ -n "$TOKEN" ]] && extra+=(--token-file "$TOKEN")
    [[ "$MONEY" = 1 ]] && extra+=(--allow-money-write)
    python3 "$HERE/run.py" plan --target "$TARGET" --out "$OUT" --pipeline "$PIPE" --proxy "$PROXY" "${extra[@]+"${extra[@]}"}"
    echo "LAUNCH workflow name=ha-party-x args.target=$TARGET args.out=$OUT args.pipeline=$PIPE args.proxy=$PROXY"
    echo "OR g1 follows AUTONOMY.md remainder loop in this TUI"
    ;;
  *)
    echo "usage: ctl.sh list|plan|remainder|prompt|mark-ready|preflight|verify|brain|auto|selftest" >&2
    exit 2
    ;;
esac
