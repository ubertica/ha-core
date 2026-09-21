#!/usr/bin/env bash
# ha-payments conductor CLI — runtime auto/tick/selftest. Never nested grok -p. No forge.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"

# Climb to equipos/lib/paths.sh or repo/equipos/lib/paths.sh
_d="$HERE"
while [[ "$_d" != "/" ]]; do
  if [[ -f "$_d/equipos/lib/paths.sh" ]]; then
    # shellcheck disable=SC1091
    source "$_d/equipos/lib/paths.sh"
    break
  fi
  if [[ -f "$_d/lib/paths.sh" ]]; then
    # shellcheck disable=SC1091
    source "$_d/lib/paths.sh"
    break
  fi
  _d="$(dirname "$_d")"
done
unset _d

GROK_HOME="${GROK_HOME:-$HOME/.grok}"
: "${PUMAPAY_OUT:=${PUMAPAY_ROOT:-$HERE}/docs/out}"
: "${HA_PAYMENTS_OUT:=${PUMAPAY_OUT}/payments}"

default_out() {
  echo "${HA_PAYMENTS_OUT}"
}

find_repo_root() {
  local d="$HERE"
  while [[ "$d" != "/" ]]; do
    if [[ -f "$d/equipos/lib/paths.sh" ]]; then
      echo "$d"
      return 0
    fi
    if [[ -f "$d/lib/paths.sh" ]]; then
      dirname "$d"
      return 0
    fi
    d="$(dirname "$d")"
  done
  echo ""
}

agent_ok() {
  local a="$1"
  local repo
  repo="$(find_repo_root)"
  local cands=(
    "$HERE/../../../agents/${a}.md"
    "$HERE/../../../../agents/${a}.md"
    "$HERE/../../../${a}.md"
  )
  if [[ -n "$repo" ]]; then
    cands+=("$repo/equipos/agents/${a}.md")
    cands+=("$repo/equipos/plugins/ha-payments/agents/${a}.md")
  fi
  cands+=("$GROK_HOME/agents/${a}.md")
  local p
  for p in "${cands[@]}"; do
    if [[ -f "$p" ]]; then
      return 0
    fi
  done
  return 1
}

wf_ok() {
  local n="$1"
  local repo
  repo="$(find_repo_root)"
  [[ -n "$repo" && -f "$repo/equipos/workflows/${n}.rhai" ]] && return 0
  [[ -f "$GROK_HOME/workflows/${n}.rhai" ]] && return 0
  # skill-adjacent
  [[ -f "$HERE/../../../../workflows/${n}.rhai" ]] && return 0
  [[ -f "$HERE/../../../../../workflows/${n}.rhai" ]] && return 0
  return 1
}

cmd="${1:-status}"
shift || true
case "$cmd" in
  plan|remainder)
    exec python3 "$HERE/dispatch.py" "$cmd" "$@"
    ;;
  verify)
    exec python3 "$HERE/verify_board.py" "$@"
    ;;
  watch)
    exec bash "$HERE/watch.sh" "$@"
    ;;
  selftest)
    echo "=== ha-payments selftest ==="
    ERR=0
    for f in dispatch.py verify_board.py watch.sh; do
      if [[ -f "$HERE/$f" ]]; then
        echo "OK script: $f"
      else
        echo "MISSING: $f"; ERR=1
      fi
    done
    SKILL="$HERE/../SKILL.md"
    if [[ ! -f "$SKILL" ]]; then SKILL="$HERE/../../SKILL.md"; fi
    for ref in NORTHSTAR.md CONTRACT.md AUTONOMY.md; do
      if [[ -f "$HERE/../references/$ref" || -f "$HERE/../../references/$ref" ]]; then
        echo "OK ref: $ref"
      else
        echo "MISSING ref: $ref"; ERR=1
      fi
    done
    if [[ -f "$HERE/../SKILL.md" || -f "$HERE/../../SKILL.md" ]]; then
      echo "OK SKILL.md"
    else
      echo "MISSING SKILL.md"; ERR=1
    fi
    # fail-closed: no forge as primary autonomy, no forbidden path literals
    AUT="$HERE/../references/AUTONOMY.md"
    [[ -f "$AUT" ]] || AUT="$HERE/../../references/AUTONOMY.md"
    if [[ -f "$AUT" ]] && grep -E 'Workflow phases|Scaffold — dirs|ctl\.sh forge --' "$AUT" >/dev/null 2>&1; then
      echo "FAIL AUTONOMY still has forge scaffold phases"; ERR=1
    else
      echo "OK AUTONOMY runtime (no forge phases)"
    fi
    SK="$HERE/../SKILL.md"
    [[ -f "$SK" ]] || SK="$HERE/../../SKILL.md"
    if [[ -f "$SK" ]]; then
      if grep -E '/Users/[A-Za-z0-9._-]+/' "$SK" >/dev/null 2>&1; then
        echo "FAIL operator home /Users/<op>/ leaked into SKILL.md"; ERR=1
      else
        echo "OK SKILL portable paths (no /Users/<op>/)"
      fi
    fi
    for a in pay-rails pay-psp pay-webhooks pay-qa pay-test pay-dev pay-sync pay-lead; do
      if agent_ok "$a"; then
        echo "OK agent: $a"
      else
        echo "MISSING agent: $a"; ERR=1
      fi
    done
    if wf_ok "ha-payments"; then
      echo "OK workflow: ha-payments.rhai"
    else
      echo "MISSING workflow ha-payments.rhai"; ERR=1
    fi
    if wf_ok "ha-payments-tick"; then
      echo "OK workflow: ha-payments-tick.rhai"
    else
      echo "MISSING workflow ha-payments-tick.rhai"; ERR=1
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
    OUT=""
    LANES=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --out) OUT="$2"; shift 2 ;;
        --lanes) LANES="$2"; shift 2 ;;
        *) shift ;;
      esac
    done
    if [[ -z "$OUT" ]]; then
      OUT="$(default_out)"
    fi
    mkdir -p "$OUT/.bus"
    python3 "$HERE/dispatch.py" plan --out "$OUT" ${LANES:+--lanes "$LANES"}
    echo "LAUNCH workflow name=ha-payments args.out=$OUT"
    echo "WATCH  $HERE/watch.sh --out $OUT"
    ;;
  tick)
    OUT=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --out) OUT="$2"; shift 2 ;;
        *) shift ;;
      esac
    done
    if [[ -z "$OUT" ]]; then
      OUT="$(default_out)"
    fi
    mkdir -p "$OUT/.bus"
    python3 "$HERE/dispatch.py" remainder --out "$OUT"
    echo "LAUNCH workflow name=ha-payments-tick args.out=$OUT"
    ;;
  status)
    OUT=""
    if [[ "${1:-}" == "--out" ]]; then
      OUT="$2"
    elif [[ -n "${1:-}" && "${1:-}" != --* ]]; then
      OUT="$1"
    else
      OUT="$(default_out)"
    fi
    python3 "$HERE/dispatch.py" status --out "$OUT" || true
    ;;
  *)
    echo "usage: ctl.sh auto|tick|status|plan|remainder|verify|watch|selftest [--out DIR]" >&2
    exit 2
    ;;
esac
