#!/usr/bin/env bash
# ha-redteam conductor CLI. Never nested grok -p. Never 4 extra TUIs.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
JIRA_SYNC="$HOME/.grok/skills/ha-hackers/scripts/jira_sync.py"
# SoT = Google Drive dani house (not the Mac).
if [[ -f "$HOME/.grok/context-nodes/DANI-PATHS.env" ]]; then
  # shellcheck disable=SC1091
  source "$HOME/.grok/context-nodes/DANI-PATHS.env"
fi
DEFAULT_OUT="${HA_REDTEAM_OUT:-$HOME/Library/CloudStorage/GoogleDrive-walterg2924@gmail.com/Mi unidad/dani/out/50-redteam}"
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
    if [[ -n "${HA_JIRA_DISABLE:-}" ]]; then
      echo "jira-sync skipped HA_JIRA_DISABLE=1 out=$OUT"
      exit 0
    fi
    exec python3 "$JIRA_SYNC" --out "$OUT" "${extra[@]+"${extra[@]}"}"
    ;;
  kb)
    exec python3 "$HOME/.grok/skills/ha-rtk-kb/scripts/kb.py" "${1:-status}" --pack ha-redteam "${@:2}"
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
    OUT="$DEFAULT_OUT"; ROLE="rdt-child"; TASK=""
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
    echo "=== ha-redteam selftest ==="
    ERR=0
    for f in dispatch.py verify_board.py watch.sh radio.py jump.py intel.py memory.py ingest.py learn.py layers.py charter.py spawn_child.py; do
      if [[ -f "$HERE/$f" ]]; then
        echo "OK script: $f"
      else
        echo "MISSING: $f"; ERR=1
      fi
    done
    [[ -f "$JIRA_SYNC" ]] && echo "OK jira_sync wrap: ha-hackers" || { echo "MISSING ha-hackers jira_sync.py"; ERR=1; }
    [[ -f "$HOME/.grok/agents/_ha-dani-law.md" ]] && echo "OK civil law" || { echo "MISSING _ha-dani-law.md"; ERR=1; }
    for a in rdt-entry rdt-probe rdt-correct rdt-fix rdt-docs rdt-jira rdt-sync rdt-lead rdt-verify rdt-jump rdt-pivot rdt-radio rdt-intel rdt-memory rdt-spawn rdt-learn; do
      if [[ "$a" != "rdt-verify" ]]; then
        if [[ -f "$HOME/.grok/agents/${a}.md" ]]; then
          echo "OK agent: $a"
        else
          echo "MISSING agent: $a"; ERR=1
        fi
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
    for w in ha-redteam.rhai ha-redteam-tick.rhai; do
      if [[ -f "$HOME/.grok/workflows/$w" ]]; then
        echo "OK workflow: $w"
      else
        echo "MISSING workflow $w"; ERR=1
      fi
    done
    if [[ -f "$HOME/.grok/skills/ha-redteam/scripts/ctl.sh" || -L "$HOME/.grok/skills/ha-redteam/scripts/ctl.sh" ]]; then
      echo "OK ~/.grok/skills/ha-redteam/scripts/ctl.sh present"
    else
      echo "MISSING skills ctl.sh"; ERR=1
    fi
    KB_PY="$HOME/.grok/skills/ha-rtk-kb/scripts/kb.py"
    [[ -f "$KB_PY" ]] && echo "OK shared kb.py" || { echo "MISSING ha-rtk-kb kb.py"; ERR=1; }
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
    echo "LAUNCH workflow name=ha-redteam args.out=$OUT args.target=${TARGET:-}"
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
    echo "LAUNCH workflow name=ha-redteam-tick args.out=$OUT"
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
