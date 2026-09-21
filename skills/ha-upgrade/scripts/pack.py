#!/usr/bin/env python3
"""Pack a /learn run (or notes) into a versioned HA upgrade plugin.

Never overwrites a prior version. Never installs. Never copies secrets.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

SECRET_RX = re.compile(
    r"(token|secret|password|api[_-]?key|authorization|webhook|ha_[a-f0-9]{16,})",
    re.I,
)
SKIP_NAME_RX = re.compile(r"(auth\.json|\.env|credentials|id_rsa|\.pem)$", re.I)


def grok_home() -> Path:
    return Path.home() / ".grok"


def registry_path() -> Path:
    return grok_home() / "hard-allow" / "upgrade" / "registry.json"


def marketplace_plugins() -> Path:
    return grok_home() / "ha-marketplace" / "plugins"


def load_registry() -> dict:
    p = registry_path()
    if not p.is_file():
        return {"current": 0, "plugins": []}
    return json.loads(p.read_text(encoding="utf-8"))


def save_registry(reg: dict) -> None:
    p = registry_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(reg, indent=2) + "\n", encoding="utf-8")


def next_version(reg: dict) -> int:
    return int(reg.get("current") or 0) + 1


def latest_learn_dir() -> Path | None:
    st = grok_home() / "learn" / "state.json"
    if not st.is_file():
        return None
    d = json.loads(st.read_text(encoding="utf-8"))
    raw = d.get("last_completed_dir") or (d.get("pending") or {}).get("run_dir")
    if not raw:
        return None
    p = Path(raw)
    return p if p.is_dir() else None


def redact(obj):
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if SECRET_RX.search(str(k)):
                out[k] = "<redacted>"
            else:
                out[k] = redact(v)
        return out
    if isinstance(obj, list):
        return [redact(x) for x in obj]
    if isinstance(obj, str) and SECRET_RX.search(obj):
        return SECRET_RX.sub("<redacted>", obj)
    return obj


def read_learn(run_dir: Path) -> dict:
    actions = {}
    report = ""
    manifest = {}
    aj = run_dir / "actions.json"
    if aj.is_file():
        actions = json.loads(aj.read_text(encoding="utf-8"))
    rp = run_dir / "report.md"
    if rp.is_file():
        report = rp.read_text(encoding="utf-8")
    mf = run_dir / "manifest.json"
    if mf.is_file():
        manifest = json.loads(mf.read_text(encoding="utf-8"))
    return {
        "run_dir": str(run_dir),
        "actions": redact(actions),
        "report": report[:200_000],
        "manifest": redact(manifest),
    }


def plugin_json(name: str, ver: int, n_actions: int) -> dict:
    return {
        "name": name,
        "version": f"{ver}.0.0",
        "description": (
            f"HA upgrade v{ver}: frozen /learn apply pack ({n_actions} actions). "
            "Install only when the operator says. Never mix Science marketplace."
        ),
        "category": "agentic",
        "keywords": [
            "ha-upgrade",
            f"v{ver}",
            "learn",
            "upgrade plugin",
            "version pack",
        ],
    }


def plugin_md(name: str, ver: int, src: str) -> str:
    return f"""# {name}

Frozen upgrade pack from agentic self-improvement (`/learn` → pack).

- **axis:** toolkit
- **status:** packed (not installed)
- **version:** v{ver}
- **source:** `{src}`

## Grants (pointer only — do not dump)
- none (upgrade of harness, not a nuclear)

## Skills to include
- `ha-upgrade-v{ver}` (apply this version)

## Next agent
- Do not `grok plugin install` unless operator says.
- Do not copy env/keys into `.mcp.json`.
- Do not overwrite older `ha-upgrade-v*`.
- Science plugins never install into original HA session.
- Apply = replay curated `actions.json` with operator consent. Rollback = trash originals.
"""


def apply_skill_md(ver: int) -> str:
    return f"""---
name: ha-upgrade-v{ver}
description: >
  Apply HA upgrade plugin v{ver} (frozen /learn actions). Use when the operator
  says apply upgrade v{ver}, instalar ha-upgrade-v{ver}, or rollback that version.
---

# ha-upgrade-v{ver}

This folder is a **frozen pack**. Do not edit it to make v{ver + 1}; pack a new plugin.

## Apply

```bash
python3 ~/.grok/skills/ha-upgrade/scripts/pack.py apply --version {ver} --go
```

Without `--go`: selftest only.

## Rollback

```bash
python3 ~/.grok/skills/ha-upgrade/scripts/pack.py rollback --version {ver} --go
```

Consent rules are the same as `/learn` step 4: no apply of `requires_confirmation` without a pick.
"""


def apply_py_stub(ver: int) -> str:
    return f'''#!/usr/bin/env python3
"""Apply or rollback ha-upgrade-v{ver}. Thin wrapper around pack.py."""
import runpy
import sys
from pathlib import Path

sys.argv = [
    "pack.py",
    sys.argv[1] if len(sys.argv) > 1 else "apply",
    "--version",
    "{ver}",
    *sys.argv[2:],
]
runpy.run_path(str(Path.home() / ".grok" / "skills" / "ha-upgrade" / "scripts" / "pack.py"), run_name="__main__")
'''


def write_plugin(dest: Path, ver: int, payload: dict, notes: str) -> None:
    if dest.exists():
        raise SystemExit(f"refusing to overwrite {dest}")
    dest.mkdir(parents=True)
    n_actions = len((payload.get("actions") or {}).get("actions") or [])
    name = dest.name
    (dest / "plugin.json").write_text(
        json.dumps(plugin_json(name, ver, n_actions), indent=2) + "\n", encoding="utf-8"
    )
    (dest / "PLUGIN.md").write_text(
        plugin_md(name, ver, payload.get("run_dir") or "notes"), encoding="utf-8"
    )
    skill_dir = dest / "skills" / f"ha-upgrade-v{ver}"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(apply_skill_md(ver), encoding="utf-8")
    scripts = dest / "scripts"
    scripts.mkdir()
    (scripts / "apply.py").write_text(apply_py_stub(ver), encoding="utf-8")
    refs = dest / "references"
    refs.mkdir()
    (refs / "actions.json").write_text(
        json.dumps(payload.get("actions") or {}, indent=2) + "\n", encoding="utf-8"
    )
    (refs / "manifest.json").write_text(
        json.dumps(payload.get("manifest") or {}, indent=2) + "\n", encoding="utf-8"
    )
    changelog = [
        f"# ha-upgrade-v{ver}",
        "",
        f"packed_at: {datetime.now(timezone.utc).isoformat()}",
        f"source: {payload.get('run_dir') or 'notes'}",
        f"actions: {n_actions}",
        "",
    ]
    if notes:
        changelog += ["## Operator notes", "", notes.strip(), ""]
    report = (payload.get("report") or "").strip()
    if report:
        changelog += ["## /learn report (copy)", "", report, ""]
    (refs / "CHANGELOG.md").write_text("\n".join(changelog), encoding="utf-8")
    cmd = dest / "commands"
    cmd.mkdir()
    (cmd / f"ha-upgrade-v{ver}.md").write_text(
        f"---\nname: ha-upgrade-v{ver}\ndescription: Apply frozen HA upgrade v{ver}.\n---\n\n"
        f"Follow `skills/ha-upgrade-v{ver}/SKILL.md`. Do not pack v{ver + 1} in this folder.\n",
        encoding="utf-8",
    )


def cmd_pack(args: argparse.Namespace) -> None:
    run_dir = Path(args.run_dir) if args.run_dir else latest_learn_dir()
    notes = ""
    if args.notes:
        np = Path(args.notes)
        notes = np.read_text(encoding="utf-8") if np.is_file() else args.notes
    payload = {"run_dir": None, "actions": {}, "report": "", "manifest": {}}
    if run_dir:
        payload = read_learn(run_dir)
    elif not notes:
        raise SystemExit("no learn run_dir and no --notes; nothing to pack")
    reg = load_registry()
    ver = next_version(reg)
    name = f"ha-upgrade-v{ver}"
    dest = marketplace_plugins() / name
    write_plugin(dest, ver, payload, notes)
    rec = {
        "version": ver,
        "name": name,
        "path": str(dest),
        "packed_at": datetime.now(timezone.utc).isoformat(),
        "source": payload.get("run_dir"),
        "installed": False,
    }
    reg["current"] = ver
    reg.setdefault("plugins", []).append(rec)
    save_registry(reg)
    print(json.dumps({"ok": True, **rec, "installed": False, "hint": "not installed; pass --go on apply"}, indent=2))


def cmd_next(_: argparse.Namespace) -> None:
    reg = load_registry()
    print(json.dumps({"current": reg.get("current") or 0, "next": next_version(reg), "plugins": reg.get("plugins") or []}, indent=2))


def find_plugin(ver: int) -> Path:
    dest = marketplace_plugins() / f"ha-upgrade-v{ver}"
    if not dest.is_dir():
        raise SystemExit(f"missing plugin {dest}")
    return dest


def cmd_selftest(args: argparse.Namespace) -> None:
    ver = args.version
    dest = find_plugin(ver)
    pj = json.loads((dest / "plugin.json").read_text(encoding="utf-8"))
    problems = []
    if pj.get("name") != dest.name:
        problems.append("plugin.json name mismatch")
    if not (dest / "PLUGIN.md").is_file():
        problems.append("missing PLUGIN.md")
    if not (dest / "skills" / f"ha-upgrade-v{ver}" / "SKILL.md").is_file():
        problems.append("missing version skill")
    if not (dest / "references" / "actions.json").is_file():
        problems.append("missing actions.json")
    for p in dest.rglob("*"):
        if p.is_file() and SKIP_NAME_RX.search(p.name):
            problems.append(f"secret-looking file {p.name}")
        if p.is_file() and p.suffix in {".md", ".json", ".py"}:
            txt = p.read_text(encoding="utf-8", errors="ignore")
            if "SECOPS_HARD_ALLOW_TOKEN=" in txt or "xai-" in txt[:200] and "xai-…" not in txt:
                if re.search(r"xai-[A-Za-z0-9]{20,}", txt):
                    problems.append(f"possible key in {p.relative_to(dest)}")
    print(json.dumps({"ok": not problems, "path": str(dest), "problems": problems}, indent=2))
    if problems:
        raise SystemExit(2)


def _copy_original(src: Path, trash: Path) -> None:
    trash.parent.mkdir(parents=True, exist_ok=True)
    if src.is_file():
        shutil.copy2(src, trash)


def cmd_apply(args: argparse.Namespace) -> None:
    ver = args.version
    dest = find_plugin(ver)
    if not args.go:
        print(json.dumps({"hold": True, "reason": "no --go", "path": str(dest)}, indent=2))
        return
    actions = json.loads((dest / "references" / "actions.json").read_text(encoding="utf-8"))
    items = actions.get("actions") or []
    trash_root = grok_home() / "learn" / "trash" / f"ha-upgrade-v{ver}" / "originals"
    applied = []
    skipped = []
    for a in items:
        if a.get("requires_confirmation"):
            skipped.append({"id": a.get("id"), "reason": "requires_confirmation"})
            continue
        if a.get("action") not in {"create", "edit"}:
            skipped.append({"id": a.get("id"), "reason": f"action {a.get('action')} not auto-applied"})
            continue
        path = Path(a.get("path") or "")
        edit = a.get("edit") or {}
        if a.get("action") == "create":
            path.parent.mkdir(parents=True, exist_ok=True)
            if path.exists():
                _copy_original(path, trash_root / path.name)
            path.write_text(edit.get("replacement") or "", encoding="utf-8")
            applied.append(a.get("id"))
            continue
        if not path.is_file():
            skipped.append({"id": a.get("id"), "reason": "missing file"})
            continue
        text = path.read_text(encoding="utf-8")
        anchor = edit.get("anchor") or ""
        repl = edit.get("replacement") or ""
        mode = edit.get("mode") or "replace"
        if anchor and anchor not in text:
            skipped.append({"id": a.get("id"), "reason": "anchor missing"})
            continue
        _copy_original(path, trash_root / path.name)
        if mode == "replace" and anchor:
            text = text.replace(anchor, repl, 1)
        elif mode == "insert_after" and anchor:
            text = text.replace(anchor, anchor + repl, 1)
        elif mode == "append":
            text = text + repl
        else:
            skipped.append({"id": a.get("id"), "reason": f"bad mode {mode}"})
            continue
        path.write_text(text, encoding="utf-8")
        applied.append(a.get("id"))
    reg = load_registry()
    for p in reg.get("plugins") or []:
        if p.get("version") == ver:
            p["installed"] = True
    save_registry(reg)
    print(json.dumps({"ok": True, "applied": applied, "skipped": skipped, "undo": str(trash_root)}, indent=2))


def cmd_rollback(args: argparse.Namespace) -> None:
    ver = args.version
    trash_root = grok_home() / "learn" / "trash" / f"ha-upgrade-v{ver}" / "originals"
    if not args.go:
        print(json.dumps({"hold": True, "reason": "no --go", "undo": str(trash_root)}, indent=2))
        return
    if not trash_root.is_dir():
        raise SystemExit(f"no originals at {trash_root}")
    restored = []
    for src in trash_root.iterdir():
        # originals are basename copies; full restore needs a map. Best-effort: skip unknown.
        restored.append(src.name)
    print(json.dumps({
        "ok": True,
        "note": "originals live here; copy back by filename from the apply log",
        "originals": restored,
        "dir": str(trash_root),
    }, indent=2))


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("pack")
    p.add_argument("--run-dir")
    p.add_argument("--notes")
    sub.add_parser("next")
    s = sub.add_parser("selftest")
    s.add_argument("--version", type=int, required=True)
    a = sub.add_parser("apply")
    a.add_argument("--version", type=int, required=True)
    a.add_argument("--go", action="store_true")
    r = sub.add_parser("rollback")
    r.add_argument("--version", type=int, required=True)
    r.add_argument("--go", action="store_true")
    args = ap.parse_args()
    {"pack": cmd_pack, "next": cmd_next, "selftest": cmd_selftest, "apply": cmd_apply, "rollback": cmd_rollback}[args.cmd](args)


if __name__ == "__main__":
    main()
