#!/usr/bin/env python3
"""Append realtime comms.jsonl. Optional HARDALLOW post. Never echo webhook URL."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
from pathlib import Path


def redact(s: str) -> str:
    import re

    s = s or ""
    s = re.sub(r"eyJ[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+", "[JWT]", s)
    s = re.sub(r"ha_[A-Za-z0-9_\-]{8,}", "[HA]", s)
    s = re.sub(r"[A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,}", "[email]", s, flags=re.I)
    s = re.sub(r"\b\d{22}\b", "[CBU]", s)
    return s[:2000]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--kind", default="HEARTBEAT")
    ap.add_argument("--from-seat", default="g1")
    ap.add_argument("--body", default="")
    ap.add_argument("--hardallow", default="", help="gold|critical|medium|pivot|audit|broadcast")
    args = ap.parse_args()
    out = Path(args.out).expanduser().resolve()
    bus = out / ".bus" / "pivot"
    bus.mkdir(parents=True, exist_ok=True)
    rec = {
        "ts": time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime()),
        "type": args.kind,
        "from": args.from_seat,
        "body": redact(args.body),
        "pack": "ha-blackhat",
        "full_throttle": True,
    }
    with (bus / "comms.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    ha = Path.home() / ".grok" / "hard-allow" / "bin" / "ha-hardallow.mjs"
    posted = False
    if args.hardallow and ha.is_file() and not os.environ.get("HA_DISCORD_DISABLE"):
        try:
            subprocess.run(
                [
                    "node",
                    str(ha),
                    args.hardallow,
                    "--title",
                    redact(args.kind)[:80],
                    "--body",
                    redact(args.body)[:1500],
                    "--out",
                    str(out),
                ],
                check=False,
                timeout=20,
                capture_output=True,
            )
            posted = True
        except Exception:
            posted = False
    print(json.dumps({"ok": True, "wrote": str(bus / "comms.jsonl"), "hardallow": posted}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
