#!/usr/bin/env python3
"""Fail-closed board verify for ha-pumapay.

Counts READY.* flags + presence of required artifacts.
Writes OUT/.bus/VERIFY.json . Missing artifact => not ready.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED = {
    "docs": ["DOCS-INDEX.md"],
    "pm": ["pm/JIRA-MODEL.md", "pm/BACKLOG.md"],
    "qa": ["qa/QA-PLAN.md", "qa/GATES.md"],
    "test": ["test/TEST-REPORT.md"],
    "dev": ["dev/CHANGES.md"],
    "repo": ["repo/REPO-STATUS.md"],
    "sync": ["sync/COLLAB-STATUS.md"],
    "lead": ["SUMMARY.md", "BOARD.md"],
}

def check_ready(out: Path, lane: str) -> bool:
    flag = (out / ".bus" / f"READY.{lane}").is_file()
    if not flag:
        return False
    for rel in REQUIRED.get(lane, []):
        if not (out / rel).is_file():
            return False
    # extra for docs tree
    if lane == "docs":
        if not (out / "docs").is_dir():
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
            miss = []
            if not (bus / f"READY.{ln}").is_file():
                miss.append("READY flag")
            for rel in REQUIRED.get(ln, []):
                if not (out / rel).is_file():
                    miss.append(rel)
            if ln == "docs" and not (out / "docs").is_dir():
                miss.append("docs/")
            missing[ln] = miss

    ready_count = sum(1 for v in ready_flags.values() if v)
    total = len(lanes)

    report = {
        "ok": ready_count == total,
        "pack": "ha-pumapay",
        "out": str(out),
        "ready_count": ready_count,
        "total": total,
        "lanes": ready_flags,
        "missing": missing,
        "required_artifacts": REQUIRED,
        "note": "Fail closed. All READY + artifacts must exist for count.",
    }
    (bus / "VERIFY.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ready_count": ready_count, "total": total, "ok": report["ok"]}))
    return 0 if report["ok"] else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
