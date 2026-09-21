#!/usr/bin/env python3
"""selftest for ha-team-forge skill itself or forged teams."""
from __future__ import annotations
import argparse
import os
import stat
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]

def is_executable(p: Path) -> bool:
    if not p.exists():
        return False
    st = p.stat()
    return bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))

def check_team(name: str) -> int:
    print(f"=== selftest --name {name} ===")
    ERR = 0
    # check plugin mirror or skill
    plugin = Path.home() / ".grok" / "plugins" / name
    skill = Path.home() / ".grok" / "skills" / name
    wf = Path.home() / ".grok" / "workflows" / f"{name}.rhai"
    if not (plugin.exists() or skill.exists()):
        print(f"MISSING plugin or skill for {name}")
        ERR = 1
    if not wf.exists():
        print(f"MISSING workflow {name}.rhai")
        ERR = 1
    # check agents for prefix if possible (best effort)
    print("SELftest basic structure checked.")
    if ERR == 0:
        print("SELftest PASS")
        return 0
    print("SELftest FAIL")
    return 1

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", default="ha-team-forge")
    args = ap.parse_args()
    if args.name == "ha-team-forge":
        # self test the forge skill
        print("=== ha-team-forge self selftest ===")
        scripts_dir = SKILL_ROOT / "scripts"
        for f in ["ctl.sh", "forge.py", "selftest.py", "from_hackers.py"]:
            p = scripts_dir / f
            if p.exists():
                print(f"OK script: {f}")
            else:
                print(f"MISSING: {f}")
                return 1
        tmpl_dir = SKILL_ROOT / "templates"
        need = ["plugin.json.tmpl", "agent.md.tmpl", "SKILL.md.tmpl", "workflow.rhai.tmpl", "ctl.sh.tmpl", "dispatch.py.tmpl"]
        for n in need:
            if (tmpl_dir / n).exists():
                print(f"OK template: {n}")
            else:
                print(f"MISSING template: {n}")
                return 1
        ex = SKILL_ROOT / "examples" / "lanes-minimal.json"
        if ex.exists():
            print("OK example lanes")
        else:
            print("MISSING lanes-minimal")
            return 1
        print("ha-team-forge SELftest PASS")
        return 0
    else:
        return check_team(args.name)

if __name__ == "__main__":
    sys.exit(main())
