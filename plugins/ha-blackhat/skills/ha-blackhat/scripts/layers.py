#!/usr/bin/env python3
"""One always-on cycle: memory → radio → jump → intel. Fail-open per layer."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run(script: str, extra: list[str]) -> dict:
    cmd = [sys.executable, str(HERE / script), *extra]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        body = (p.stdout or "").strip().splitlines()[-1] if p.stdout else "{}"
        try:
            rec = json.loads(body)
        except json.JSONDecodeError:
            rec = {"raw": body[:400]}
        rec["_exit"] = p.returncode
        rec["_script"] = script
        return rec
    except Exception as e:
        return {"ok": False, "error": type(e).__name__, "_script": script}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--proxy", default="")
    args = ap.parse_args()
    extra = ["--out", args.out]
    rec = {
        "ok": True,
        "pack": "ha-blackhat",
        "layers": {
            "memory": run("memory.py", extra + ["--op", "hydrate"]),
            "radio": run(
                "radio.py",
                extra + ["--kind", "HEARTBEAT", "--body", "ha-blackhat layers cycle"],
            ),
            "jump": run("jump.py", extra),
            "intel": run("intel.py", extra + (["--proxy", args.proxy] if args.proxy else [])),
            "ingest": run("ingest.py", extra),
        },
    }
    bus = Path(args.out).expanduser().resolve() / ".bus"
    bus.mkdir(parents=True, exist_ok=True)
    (bus / "LAYERS.json").write_text(json.dumps(rec, indent=2) + "\n")
    print(json.dumps(rec))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
