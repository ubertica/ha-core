#!/usr/bin/env python3
"""Fail-closed board verify for ha-payments.

READY.<lane> + artifact at OUT root. Missing artifact => not ready.
OUT default is $PUMAPAY_OUT/payments/ so artifacts are MODEL.md not domain/MODEL.md.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED = {
    "rails": [
        "RAILS.md"
    ],
    "psp": [
        "PSP.md"
    ],
    "webhooks": [
        "WEBHOOKS.md"
    ],
    "qa": [
        "GATES.md"
    ],
    "test": [
        "TEST-REPORT.md"
    ],
    "dev": [
        "CHANGES.md"
    ],
    "sync": [
        "COLLAB-STATUS.md"
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

    lanes = list(REQUIRED.keys())
    ready_flags = {}
    missing = {}
    for ln in lanes:
        ok = check_ready(out, ln)
        ready_flags[ln] = ok
        if not ok:
            missing[ln] = [rel for rel in REQUIRED.get(ln, []) if not (out / rel).is_file()]
            if not (out / ".bus" / f"READY.{ln}").is_file():
                missing[ln] = missing.get(ln, []) + [f".bus/READY.{ln}"]
    ready_count = sum(1 for v in ready_flags.values() if v)
    rec = {
        "ok": ready_count == len(lanes),
        "pack": "ha-payments",
        "ready": ready_flags,
        "ready_count": ready_count,
        "total": len(lanes),
        "missing": missing,
        "go_count": ready_count,
        "note": "Fail-closed: READY without artifact is not ready. No invented GO.",
    }
    (bus / "VERIFY.json").write_text(json.dumps(rec, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(rec))
    return 0 if rec["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
