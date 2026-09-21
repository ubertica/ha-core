#!/usr/bin/env bash
# Conductor CLI. Never nested grok -p.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
cmd="${1:-status}"
shift || true
case "$cmd" in
  plan) exec python3 "$HERE/dispatch.py" plan "$@" ;;
  status|remainder) exec python3 "$HERE/dispatch.py" remainder "$@" ;;
  preflight) exec python3 "$HERE/session_guard.py" "$@" ;;
  verify) exec python3 "$HERE/verify_evidence.py" "$@" ;;
  jira-sync) exec python3 "$HERE/jira_sync.py" "$@" ;;
  watch-jira) exec python3 "$HERE/jira_sync.py" --watch --interval "${1:-20}" ;;
  workstream) exec python3 "$HERE/workstream.py" "$@" ;;
  hunt) exec python3 "$HERE/hunt_urlparams.py" "$@" ;;
  watch) exec bash "$HERE/watch.sh" "$@" ;;
  selftest) exec python3 "$HERE/test_autonomy.py" "$@" ;;
  auto)
    OUT=""
    TARGET=""
    PACK="auto"
    PROXY="${HA_PROXY:-socks5h://127.0.0.1:10808}"
    TOKEN=""
    MONEY=0
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --out) OUT="$2"; shift 2 ;;
        --target) TARGET="$2"; shift 2 ;;
        --pack) PACK="$2"; shift 2 ;;
        --proxy) PROXY="$2"; shift 2 ;;
        --token-file) TOKEN="$2"; shift 2 ;;
        --allow-money-write) MONEY=1; shift ;;
        *) shift ;;
      esac
    done
    if [[ -z "$OUT" || -z "$TARGET" ]]; then
      echo "usage: ctl.sh auto --target URL --out DIR [--pack auto|docs-entry|ha-hackers] [--proxy URL] [--token-file FILE]" >&2
      exit 2
    fi
    extra=()
    [[ -n "$TOKEN" ]] && extra+=(--token-file "$TOKEN")
    [[ "$MONEY" = 1 ]] && extra+=(--allow-money-write)
    python3 "$HERE/dispatch.py" plan --target "$TARGET" --out "$OUT" --pack "$PACK" --proxy "$PROXY" "${extra[@]+"${extra[@]}"}"
    wf=$(python3 -c "import json; print(json.load(open('$OUT/.bus/PLAN.json'))['workflow'])")
    pack=$(python3 -c "import json; print(json.load(open('$OUT/.bus/PLAN.json'))['pack'])")
    echo "LAUNCH workflow name=ha-auto (or $wf) args.target=$TARGET args.out=$OUT args.pack=$pack args.proxy=$PROXY"
    echo "WATCH  $HERE/watch.sh --out $OUT --pack $pack --target $TARGET"
    ;;
  sync-plugin)
    DEST="${HOME}/.grok/plugins/ha-hackers"
    mkdir -p "$DEST/skills/ha-hackers" "$DEST/skills/ha-docs-entry" "$DEST/skills/ha-auto" "$DEST/commands" "$DEST/agents"
    rsync -a "$HOME/.grok/skills/ha-hackers/" "$DEST/skills/ha-hackers/"
    rsync -a "$HOME/.grok/skills/ha-docs-entry/" "$DEST/skills/ha-docs-entry/"
    rsync -a "$HOME/.grok/skills/ha-auto/" "$DEST/skills/ha-auto/"
    rsync -a "$HOME/.grok/commands/ha-auto.md" "$HOME/.grok/commands/ha-hackers.md" "$HOME/.grok/commands/docs-entry.md" "$DEST/commands/"
    rsync -a "$HOME/.grok/agents/hack-"*.md "$HOME/.grok/agents/_ha-law.md" "$HOME/.grok/agents/README.md" "$DEST/agents/"
    echo "synced plugin -> $DEST"
    ;;
  *)
    echo "usage: ctl.sh plan|status|remainder|preflight|verify|jira-sync|watch-jira|watch|auto|selftest|sync-plugin --out DIR [--target URL] [--pack auto|docs-entry|ha-hackers]" >&2
    exit 2
    ;;
esac
