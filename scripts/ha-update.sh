#!/usr/bin/env bash
# Client: update CORE only. Never touches HA-ReadOnly/home overlay.
# ff-only. HOLD if diverged.
set -euo pipefail

REMOTE="${HA_CORE_REMOTE:-https://github.com/ubertica/ha-core.git}"
STATE="${HA_READONLY_STATE:-$HOME/Library/Application Support/HA-ReadOnly}"
CORE="${HA_CORE_DIR:-$STATE/core}"
BRANCH="${HA_CORE_BRANCH:-main}"
CHECK=0
[[ "${1:-}" == "--check" ]] && CHECK=1

mkdir -p "$STATE"
if [[ ! -d "$CORE/.git" ]]; then
  if [[ "$CHECK" == 1 ]]; then
    echo "HA-CORE: not cloned ($CORE)"
    exit 2
  fi
  echo "HA-CORE: clone $REMOTE → $CORE"
  git clone --branch "$BRANCH" --single-branch "$REMOTE" "$CORE"
  echo "HA-CORE: seeded. overlay home untouched: $STATE/home"
  exit 0
fi

git -C "$CORE" remote set-url origin "$REMOTE" 2>/dev/null || true
git -C "$CORE" fetch origin "$BRANCH"
LOCAL=$(git -C "$CORE" rev-parse HEAD)
REMOTE_REV=$(git -C "$CORE" rev-parse "origin/$BRANCH")
if [[ "$LOCAL" == "$REMOTE_REV" ]]; then
  echo "HA-CORE: up to date $LOCAL"
  exit 0
fi
if [[ "$CHECK" == 1 ]]; then
  echo "HA-CORE: behind local=$LOCAL remote=$REMOTE_REV"
  exit 3
fi

if git -C "$CORE" merge-base --is-ancestor HEAD "origin/$BRANCH"; then
  git -C "$CORE" merge --ff-only "origin/$BRANCH"
  echo "HA-CORE: ff-only → $(git -C "$CORE" rev-parse --short HEAD)"
  echo "HA-CORE: overlay home untouched: $STATE/home"
else
  echo "HA-CORE HOLD: local diverged. no reset --hard. overlay preserved." >&2
  exit 4
fi
