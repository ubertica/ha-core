#!/usr/bin/env bash
# ha-team-forge conductor / CLI. Implements forge, selftest, from-hackers, sync, list-templates.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
SKILL_ROOT="$(cd "$HERE/.." && pwd)"
cmd="${1:-help}"
shift || true

case "$cmd" in
  forge)
    exec python3 "$HERE/forge.py" "$@"
    ;;
  selftest)
    exec python3 "$HERE/selftest.py" "$@"
    ;;
  from-hackers)
    exec python3 "$HERE/from_hackers.py" "$@"
    ;;
  sync)
    # sync skill to plugins mirror
    DEST="${HOME}/.grok/plugins/ha-team-forge"
    mkdir -p "$DEST/skills/ha-team-forge" "$DEST/commands" "$DEST/agents"
    rsync -a --delete "$SKILL_ROOT/" "$DEST/skills/ha-team-forge/" || cp -R "$SKILL_ROOT/"* "$DEST/skills/ha-team-forge/"
    # also copy current commands if present
    if [[ -f "$HOME/.grok/commands/ha-team-forge.md" ]]; then
      cp "$HOME/.grok/commands/ha-team-forge.md" "$DEST/commands/" || true
    fi
    echo "synced ha-team-forge skill -> $DEST"
    ;;
  list-templates)
    echo "Templates in $SKILL_ROOT/templates:"
    ls -1 "$SKILL_ROOT/templates/" || true
    ;;
  help|*)
    echo "ha-team-forge ctl: forge|selftest|from-hackers|sync|list-templates"
    echo "Example: $0 forge --name ha-smoke --prefix smk --mode team --tick 0 --purpose 'smoke' --lanes ... --plugin-root /tmp/..."
    exit 2
    ;;
esac
