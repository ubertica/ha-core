#!/usr/bin/env python3
"""g1-only SPAWN_REQUEST. Children do not spawn. Budget 8. Wraps ha-pivot helper."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

HELPER = Path.home() / ".grok" / "skills" / "ha-pivot" / "scripts" / "request-subagent.mjs"
MAX_LIVE = 8


def live_count(out: Path) -> int:
    d = out / ".bus" / "pivot"
    if not d.is_dir():
        return 0
    return len(list(d.glob("spawn-request-*.json")))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--role", default="bht-child")
    ap.add_argument("--task", required=True)
    args = ap.parse_args()
    out = Path(args.out).expanduser().resolve()
    n = live_count(out)
    if n >= MAX_LIVE:
        print(json.dumps({"ok": False, "error": "child-budget", "live": n, "max": MAX_LIVE}))
        return 2
    if not HELPER.is_file():
        print(json.dumps({"ok": False, "error": "missing request-subagent.mjs"}))
        return 1
    r = subprocess.run(
        [
            "node",
            str(HELPER),
            "--out",
            str(out),
            "--role",
            args.role,
            "--task",
            args.task,
            "--parent",
            "ha-blackhat",
        ],
        capture_output=True,
        text=True,
    )
    print(r.stdout)
    if r.returncode != 0:
        print(r.stderr, file=sys.stderr)
    (out / ".bus" / "READY.spawn").write_text("ok\n", encoding="utf-8")
    return r.returncode


if __name__ == "__main__":
    raise SystemExit(main())
