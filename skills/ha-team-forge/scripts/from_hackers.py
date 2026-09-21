#!/usr/bin/env python3
"""Extract checklist of files from ha-hackers gold. Used by ctl from-hackers."""
from __future__ import annotations
import os
from pathlib import Path

GOLD = Path.home() / ".grok" / "plugins" / "ha-hackers"

def main():
    if not GOLD.exists():
        print("GOLD not found at", GOLD)
        return 1
    print("=== ha-hackers gold file checklist ===")
    for root, dirs, files in os.walk(GOLD):
        for f in sorted(files):
            rp = Path(root) / f
            rel = rp.relative_to(GOLD)
            print(str(rel))
    print("=== end ===")
    # also agents in ~/.grok/agents if present
    agents = Path.home() / ".grok" / "agents"
    if agents.exists():
        print("\n=== matching user agents ===")
        for f in sorted(agents.glob("hack-*.md")):
            print(f.name)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
