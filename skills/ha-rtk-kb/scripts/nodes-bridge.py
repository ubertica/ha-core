#!/usr/bin/env python3
"""Pointer for ha-context-nodes. Does not dump node blobs or secrets."""
from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path

KB = Path(os.environ.get("HA_RTK_KB") or (Path.home() / ".grok" / "ha-rtk-kb")).expanduser()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", default="ha-redteam")
    ap.add_argument("--out", default="")
    ap.add_argument("--target", default="")
    args = ap.parse_args()
    (KB / "nodes").mkdir(parents=True, exist_ok=True)
    rec = {
        "ts": time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime()),
        "pack": args.pack,
        "out": args.out,
        "hydrate": f"nodes_search q={args.target or 'TARGET'} tags=ha-rtk-kb",
        "commit": f"nodes_commit_turn source=grok tags=[ha-rtk-kb,{args.pack}]",
        "note": "Do not put JWT/CBU/loot in nodes. Paths + redacted titles only.",
    }
    p = KB / "nodes" / "BRIDGE.json"
    p.write_text(json.dumps(rec, indent=2) + "\n", encoding="utf-8")
    if args.out:
        out = Path(args.out).expanduser().resolve()
        (out / "memory").mkdir(parents=True, exist_ok=True)
        (out / "memory" / "NODES.md").write_text(
            f"# NODES bridge\n\nShared: `{p}`\n\n{rec['hydrate']}\n{rec['commit']}\n",
            encoding="utf-8",
        )
    print(json.dumps(rec))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
