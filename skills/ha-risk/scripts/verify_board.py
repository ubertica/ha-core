#!/usr/bin/env python3
"""Fail-closed board verify for ha-risk.

Counts READY.* flags + presence of required artifacts.
Writes OUT/.bus/VERIFY.json . Missing artifact => not ready.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED = {
    "rules": ["risk/RULES.md"],
    "cases": ["risk/CASES.md"],
    "score": ["risk/SCORING.md"],
    "qa": ["qa/GATES.md"],
    "dev": ["dev/CHANGES.md"],
    "sync": ["sync/COLLAB-STATUS.md"],
    "lead": ["SUMMARY.md"]
}

def check_ready(out: Path, lane: str) -> bool:
    flag = (out / ".bus" / f"READY.{lane}").is_file()
    if not flag:
        return False
    for rel in REQUIRED.get(lane, []):
        if not (out / rel).is_file():
            return False
    return True

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    out = Path(args.out).expanduser().resolve()
    bus = out / ".bus"
    bus.mkdir(parents=True, exist_ok=True)

    lanes = list(REQUIRED.keys())
    ready_flags = {}
    missing = {}
    for ln in lanes:
        ok = check_ready(out, ln)
        ready_flags[ln] = ok
        if not ok:
            missing[ln] = [rel for rel in REQUIRED.get(ln, []) if not (out / rel).is_file()]
    ready_count = sum(1 for v in ready_flags.values() if v)
    rec = {
        "ok": ready_count == len(lanes),
        "pack": "ha-risk",
        "ready": ready_flags,
        "ready_count": ready_count,
        "total": len(lanes),
        "missing": missing,
        "go_count": ready_count,  # simplistic; real packs use evidence count
    }
    (bus / "VERIFY.json").write_text(json.dumps(rec, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(rec))
    return 0 if rec["ok"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
