#!/usr/bin/env python3
"""Fail-closed board verify for ha-dani-ops.

READY.* + required artifacts. Civil scan must pass.
Missing artifact => not ready. Civil hit => not ok even if READY flags exist.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from civil_scan import write_scan  # noqa: E402

PACK = "ha-dani-ops"
HOLD_REQUIRED = True
REQUIRED = {
    "perimeter": [
        "perimeter/STATUS.md"
    ],
    "ams": [
        "ams/HEALTH.md"
    ],
    "dash": [
        "dash/HEALTH.md"
    ],
    "change": [
        "change/WINDOW.md"
    ],
    "escalate": [
        "escalate/LOG.md"
    ],
    "hold": [
        "HOLD.md"
    ],
    "sync": [
        "sync/COLLAB.md"
    ],
    "lead": [
        "SUMMARY.md"
    ]
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

    civil = write_scan(out)
    lanes = list(REQUIRED.keys())
    ready_flags = {}
    missing = {}
    for ln in lanes:
        ok = check_ready(out, ln)
        ready_flags[ln] = ok
        if not ok:
            missing[ln] = [rel for rel in REQUIRED.get(ln, []) if not (out / rel).is_file()]

    hold_ok = True
    if HOLD_REQUIRED:
        hold_ok = (out / "HOLD.md").is_file()
        if not hold_ok:
            missing.setdefault("hold-file", []).append("HOLD.md")

    ready_count = sum(1 for v in ready_flags.values() if v)
    rec = {
        "ok": ready_count == len(lanes) and civil["ok"] and hold_ok,
        "pack": PACK,
        "ready": ready_flags,
        "ready_count": ready_count,
        "total": len(lanes),
        "missing": missing,
        "civil_ok": civil["ok"],
        "civil_hits": civil.get("hits", []),
        "hold_ok": hold_ok,
        "go_count": 0,
        "note": "civil pack: go_count stays 0. CLOSED is a named artifact, not a GO.",
    }
    (bus / "VERIFY.json").write_text(json.dumps(rec, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(rec))
    return 0 if rec["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
