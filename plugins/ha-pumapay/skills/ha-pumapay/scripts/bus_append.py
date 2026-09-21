#!/usr/bin/env python3
"""Append JSON message to shared pumapay-bus. Used by pp-sync and ctl."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

BUS_DIR = Path.home() / ".grok" / "pumapay-bus"

def append(bus_name: str, msg: dict) -> Path:
    BUS_DIR.mkdir(parents=True, exist_ok=True)
    f = BUS_DIR / bus_name
    if not msg.get("ts"):
        msg["ts"] = datetime.now(timezone.utc).isoformat()
    line = json.dumps(msg, ensure_ascii=False)
    with f.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")
    return f

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bus", default="pumapay-to-sentinel.jsonl", help="target jsonl under ~/.grok/pumapay-bus/")
    ap.add_argument("--from", dest="from_", default="pp-sync")
    ap.add_argument("--to", default="ha-sentinel")
    ap.add_argument("--type", default="health")
    ap.add_argument("--severity", default="info")
    ap.add_argument("--msg", default="")
    ap.add_argument("--path", default="")
    args = ap.parse_args()

    rec = {
        "from": args.from_,
        "to": args.to,
        "type": args.type,
        "severity": args.severity,
        "msg": args.msg or "sync event",
        "path": args.path,
    }
    p = append(args.bus, rec)
    print(json.dumps({"ok": True, "written": str(p), "rec": rec}))
    return 0

if __name__ == "__main__":
    sys.exit(main())
