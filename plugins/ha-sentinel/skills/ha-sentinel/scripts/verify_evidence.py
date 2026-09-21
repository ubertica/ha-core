#!/usr/bin/env python3
"""Fail-closed evidence verify for ha-sentinel.

Counts READY.* flags + presence of required artifacts from AMS mirror.
Writes OUT/.bus/VERIFY.json . Missing => not ready.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED = {
    "watch": ["perimeter.md"],
    "ollama": ["ollama.md"],
    "audit": ["audit.md"],
    "improve": ["improve.md"],
    "release": ["release.md"],
    "escalate": ["escalations.md"],
    "collab": ["collab.md"],
    "lead": ["SUMMARY.md"],
}

def check_ready(out: Path, lane: str) -> bool:
    flag = (out / ".bus" / f"READY.{lane}").is_file()
    if not flag:
        return False
    for rel in REQUIRED.get(lane, []):
        if not (out / rel).is_file():
            return False
    if lane == "watch":
        if not (out / "ams-mirror").is_dir():
            return False
    return True

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    out = Path(args.out).expanduser().resolve()
    ready = {}
    for lane in REQUIRED:
        ready[lane] = check_ready(out, lane)
    rec = {
        "ok": all(ready.values()),
        "ready_count": sum(1 for v in ready.values() if v),
        "total": len(ready),
        "ready": ready,
        "paths": [str(out / r) for r in REQUIRED["lead"]],
    }
    bus = out / ".bus"
    bus.mkdir(parents=True, exist_ok=True)
    (bus / "VERIFY.json").write_text(json.dumps(rec, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(rec))
    return 0 if rec["ok"] else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
