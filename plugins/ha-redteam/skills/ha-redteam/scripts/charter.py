#!/usr/bin/env python3
"""Classify an action: UNBREAKABLE (HOLD) vs BENDABLE (GO)."""
from __future__ import annotations

import argparse
import json
import re
import sys

UNBREAKABLE = [
    ("live-money", r"live money|deposit|withdraw|payout|claim prize|force.?pay|cash.?out"),
    ("live-gplaygap-patch", r"patch api\.gplaygap|live.?patch.*gplaygap"),
    ("invented-go", r"invent(ed)? go|fake go|ready_count.*go"),
    ("pii", r"\b(cbu|cuit|jwt|dash\.pass|password dump)\b"),
    ("loot-mix", r"dump/|hack/full|exfil-loot"),
    ("mac-isp", r"mac isp|without socks|direct isp"),
    ("minors", r"\bminor\b|\bchild porn"),
    ("nested-grok", r"nested grok -p|grok -p"),
    ("extra-tui", r"spawn .*tui|4 grok tui"),
    ("operator-stop", r"cancelá|operator.?stop|steal.*(clipboard|retina|focus)"),
    ("no-prod-effect-lie", r"no production effect|dummy.*harmless"),
]


def classify(text: str) -> dict:
    t = (text or "").lower()
    hits = [name for name, pat in UNBREAKABLE if re.search(pat, t, re.I)]
    return {
        "ok": True,
        "class": "UNBREAKABLE" if hits else "BENDABLE",
        "hits": hits,
        "action": "HOLD" if hits else "GO-bend",
        "note": "UNBREAKABLE cannot be bent. Else bend in service of OBJECTIVE.",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("text", nargs="*", default=[])
    ap.add_argument("--text", dest="flag_text", default="")
    args = ap.parse_args()
    blob = args.flag_text or " ".join(args.text) or sys.stdin.read()
    rec = classify(blob)
    print(json.dumps(rec))
    return 2 if rec["class"] == "UNBREAKABLE" else 0


if __name__ == "__main__":
    raise SystemExit(main())
