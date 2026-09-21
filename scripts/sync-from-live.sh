#!/usr/bin/env bash
# Operator: copy live ~/.grok CORE into this repo. Never copies overlay/secrets.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
GROK="${GROK_HOME:-$HOME/.grok}"
EX=(--exclude '.DS_Store' --exclude '__pycache__' --exclude '*.pyc' --exclude '*.sock' --exclude '*.log')

copy_tree() {
  local src="$1" dst="$2"
  mkdir -p "$dst"
  rsync -a --delete "${EX[@]}" "$src/" "$dst/"
}

echo "==> skills/ha-*"
mkdir -p "$ROOT/skills"
# drop skills that vanished live
find "$ROOT/skills" -mindepth 1 -maxdepth 1 -type d -exec rm -rf {} +
for d in "$GROK/skills"/ha-*; do
  [[ -d "$d" ]] || continue
  name="$(basename "$d")"
  rsync -a "${EX[@]}" "$d/" "$ROOT/skills/$name/"
done

echo "==> agents commands workflows personas roles"
copy_tree "$GROK/agents" "$ROOT/agents"
copy_tree "$GROK/commands" "$ROOT/commands"
copy_tree "$GROK/workflows" "$ROOT/workflows"
copy_tree "$GROK/personas" "$ROOT/personas"
copy_tree "$GROK/roles" "$ROOT/roles"

if [[ -d "$GROK/plugins" ]]; then
  echo "==> plugins"
  copy_tree "$GROK/plugins" "$ROOT/plugins"
fi

echo "==> marketplace/plugins (no data/)"
mkdir -p "$ROOT/marketplace/plugins"
rsync -a --delete "${EX[@]}" "$GROK/ha-marketplace/plugins/" "$ROOT/marketplace/plugins/"
for f in LAW.md README.md HANDOFF.md roster.json; do
  [[ -f "$GROK/ha-marketplace/$f" ]] && cp -f "$GROK/ha-marketplace/$f" "$ROOT/marketplace/$f"
done

python3 - "$ROOT" <<'PY'
import json, pathlib, datetime
root = pathlib.Path(__import__("sys").argv[1])
skills = sorted(p.name for p in (root / "skills").glob("ha-*") if p.is_dir())
man = {
  "name": "ha-core",
  "layer": "B",
  "version": "0.1.0",
  "generated_at": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
  "visibility": "private",
  "wip": [],
  "skills": skills,
  "never": ["auth.json", "active.env", "grants", "secrets", "sessions", "loot", "HA-ReadOnly"],
}
(root / "core-manifest.json").write_text(json.dumps(man, indent=2) + "\n")
print("manifest skills", len(skills))
PY

echo "==> done $ROOT"
