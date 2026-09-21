#!/usr/bin/env bash
# ha-blackhat conductor CLI. Never nested grok -p. Never 4 extra TUIs.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
JIRA_SYNC="$HOME/.grok/skills/ha-hackers/scripts/jira_sync.py"
DEFAULT_OUT="${HA_BLACKHAT_OUT:-$HOME/dev/ha-live/proof/engagements/blackhat}"
cmd="${1:-status}"
shift || true
case "$cmd" in
  plan|remainder) exec python3 "$HERE/dispatch.py" "$cmd" "$@" ;;
  verify) exec python3 "$HERE/verify_board.py" "$@" ;;
  watch) exec bash "$HERE/watch.sh" "$@" ;;
  jira-sync)
    OUT=""
    extra=()
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --out) OUT="$2"; shift 2 ;;
        *) extra+=("$1"); shift ;;
      esac
    done
    OUT="${OUT:-$DEFAULT_OUT}"
    if [[ -z "${HA_BLACKHAT_JIRA:-}" ]]; then
      echo "HOLD jira-sync: ha-blackhat is not Puma Jira default. Set HA_BLACKHAT_JIRA=1 to push. out=$OUT"
      exit 0
    fi
    if [[ -n "${HA_JIRA_DISABLE:-}" ]]; then
      echo "jira-sync skipped HA_JIRA_DISABLE=1 out=$OUT"
      exit 0
    fi
    exec python3 "$JIRA_SYNC" --out "$OUT" "${extra[@]+"${extra[@]}"}"
    ;;
  kb)
    exec python3 "$HOME/.grok/skills/ha-rtk-kb/scripts/kb.py" "${1:-status}" --pack ha-blackhat "${@:2}"
    ;;
  ingest)
    OUT="$DEFAULT_OUT"
    extra=()
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --out) OUT="$2"; shift 2 ;;
        *) extra+=("$1"); shift ;;
      esac
    done
    exec python3 "$HERE/ingest.py" --out "$OUT" "${extra[@]+"${extra[@]}"}"
    ;;
  radio|jump|intel|memory|layers|charter)
    OUT="$DEFAULT_OUT"
    extra=()
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --out) OUT="$2"; shift 2 ;;
        *) extra+=("$1"); shift ;;
      esac
    done
    case "$cmd" in
      radio) exec python3 "$HERE/radio.py" --out "$OUT" "${extra[@]+"${extra[@]}"}" ;;
      jump) exec python3 "$HERE/jump.py" --out "$OUT" ;;
      intel) exec python3 "$HERE/intel.py" --out "$OUT" "${extra[@]+"${extra[@]}"}" ;;
      memory) exec python3 "$HERE/memory.py" --out "$OUT" "${extra[@]+"${extra[@]}"}" ;;
      layers) exec python3 "$HERE/layers.py" --out "$OUT" "${extra[@]+"${extra[@]}"}" ;;
      charter) exec python3 "$HERE/charter.py" "${extra[@]+"${extra[@]}"}" ;;
    esac
    ;;
  spawn)
    OUT="$DEFAULT_OUT"; ROLE="bht-child"; TASK=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --out) OUT="$2"; shift 2 ;;
        --role) ROLE="$2"; shift 2 ;;
        --task) TASK="$2"; shift 2 ;;
        *) shift ;;
      esac
    done
    [[ -n "$TASK" ]] || { echo "spawn needs --task"; exit 2; }
    exec python3 "$HERE/spawn_child.py" --out "$OUT" --role "$ROLE" --task "$TASK"
    ;;
  selftest)
    echo "=== ha-blackhat selftest ==="
    ERR=0
    for f in dispatch.py verify_board.py watch.sh radio.py jump.py intel.py memory.py ingest.py learn.py layers.py charter.py spawn_child.py; do
      if [[ -f "$HERE/$f" ]]; then
        echo "OK script: $f"
      else
        echo "MISSING: $f"; ERR=1
      fi
    done
    [[ -f "$HOME/.grok/agents/_ha-law.md" ]] && echo "OK _ha-law.md" || { echo "MISSING _ha-law.md"; ERR=1; }
    [[ -f "$HOME/.grok/agents/_ha-dani-law.md" ]] && echo "NOTE dani-law present (civil pack only — do not load on blackhat)"
    KB_PY="$HOME/.grok/skills/ha-rtk-kb/scripts/kb.py"
    [[ -f "$KB_PY" ]] && echo "OK shared kb.py" || { echo "MISSING ha-rtk-kb kb.py"; ERR=1; }
    for a in bht-entry bht-probe bht-exploit bht-loot bht-chain bht-weapon bht-docs bht-lead bht-jump bht-pivot bht-radio bht-intel bht-memory bht-spawn bht-learn bht-sync; do
      if [[ -f "$HOME/.grok/agents/${a}.md" ]]; then
        echo "OK agent: $a"
      else
        echo "MISSING agent: $a"; ERR=1
      fi
      if [[ -f "$HOME/.grok/personas/${a}.toml" ]]; then
        echo "OK persona: $a"
      else
        echo "MISSING persona: $a"; ERR=1
      fi
      if [[ -f "$HOME/.grok/roles/${a}.toml" ]]; then
        echo "OK role: $a"
      else
        echo "MISSING role: $a"; ERR=1
      fi
    done
    for w in ha-blackhat.rhai ha-blackhat-tick.rhai; do
      if [[ -f "$HOME/.grok/workflows/$w" ]]; then
        echo "OK workflow: $w"
      else
        echo "MISSING workflow $w"; ERR=1
      fi
    done
    if [[ -f "$HOME/.grok/skills/ha-blackhat/scripts/ctl.sh" || -L "$HOME/.grok/skills/ha-blackhat/scripts/ctl.sh" ]]; then
      echo "OK ~/.grok/skills/ha-blackhat/scripts/ctl.sh present"
    else
      echo "MISSING skills ctl.sh"; ERR=1
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
    OUT=""; TARGET=""; PROXY="${HA_PROXY:-socks5h://127.0.0.1:10808}"
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --out) OUT="$2"; shift 2 ;;
        --target) TARGET="$2"; shift 2 ;;
        --proxy) PROXY="$2"; shift 2 ;;
        --lanes) LANES="$2"; shift 2 ;;
        *) shift ;;
      esac
    done
    OUT="${OUT:-$DEFAULT_OUT}"
    mkdir -p "$OUT/.bus"
    if [[ -n "$TARGET" ]]; then
      printf '%s\n' "$TARGET" > "$OUT/.bus/TARGET"
      printf '%s\n' "$PROXY" > "$OUT/.bus/PROXY"
    fi
    python3 "$HERE/dispatch.py" plan --out "$OUT" ${LANES:+--lanes "$LANES"}
    python3 "$HERE/layers.py" --out "$OUT" ${PROXY:+--proxy "$PROXY"} || true
    echo "LAUNCH workflow name=ha-blackhat args.out=$OUT args.target=${TARGET:-}"
    echo "LAYERS $HERE/ctl.sh layers --out $OUT"
    echo "WATCH  $HERE/watch.sh --out $OUT"
    echo "JIRA   $HERE/ctl.sh jira-sync --out $OUT"
    echo "PARTY  g1=this TUI g2=entry/jump g3=probe+intel g4=fix+docs — radio always"
    ;;
  tick)
    OUT=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --out) OUT="$2"; shift 2 ;;
        *) shift ;;
      esac
    done
    OUT="${OUT:-$DEFAULT_OUT}"
    python3 "$HERE/dispatch.py" remainder --out "$OUT"
    echo "LAUNCH workflow name=ha-blackhat-tick args.out=$OUT"
    ;;
  status)
    OUT="${1:-$DEFAULT_OUT}"
    python3 "$HERE/dispatch.py" status --out "$OUT" || true
    ;;
  *)
    echo "usage: ctl.sh auto|tick|status|plan|remainder|verify|jira-sync|watch|selftest|layers|radio|jump|intel|memory|ingest|kb|spawn|charter --out DIR" >&2
    exit 2
    ;;
esac
