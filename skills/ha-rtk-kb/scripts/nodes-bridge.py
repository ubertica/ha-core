#!/usr/bin/env python3
"""Placeholders on Mac. Bodies on Drive (walterg2924). Expand via nodes-drive.py."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

DRIVE_PY = Path.home() / ".grok" / "context-nodes" / "bin" / "nodes-drive.py"


def run(args: list[str]) -> dict:
    p = subprocess.run([sys.executable, str(DRIVE_PY), *args], capture_output=True, text=True)
    body = (p.stdout or "").strip().splitlines()[-1] if p.stdout else "{}"
    try:
        rec = json.loads(body)
    except json.JSONDecodeError:
        rec = {"ok": False, "raw": body[:400], "err": (p.stderr or "")[-300]}
    rec["_exit"] = p.returncode
    return rec


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", nargs="?", default="status", choices=["status", "get", "search", "expand"])
    ap.add_argument("--id", default="")
    ap.add_argument("--q", default="")
    ap.add_argument("--tenant", default="admin")
    ap.add_argument("--limit", type=int, default=10)
    args = ap.parse_args()
    if args.cmd in ("get", "expand"):
        rec = run(["get", "--tenant", args.tenant, "--id", args.id])
    elif args.cmd == "search":
        rec = run(["search", "--tenant", args.tenant, "--q", args.q, "--limit", str(args.limit)])
    else:
        rec = run(["status", "--tenant", args.tenant])
    print(json.dumps(rec, default=str))
    return 0 if rec.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
