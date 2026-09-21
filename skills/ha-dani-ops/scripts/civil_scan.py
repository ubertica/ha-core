#!/usr/bin/env python3
"""Fail-closed civil scan for ha-dani OUT trees.

Daniel packs are read-only / client-facing. OUT must never grow into a loot dump.
This is the disk gate that keeps ha-hackers muscle from leaking into civil work.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

FORBIDDEN_NAME = {
    "ACCESS.md",
    "session.json",
    "LOOT-PUMA.md",
    "LOOT-USERS.md",
}

# Always-fail material (secrets / loot bodies). Markdown may *cite* quarantine
# folder names; those hits only apply to json/csv/jsonl copies.
SECRET_SUBSTR = (
    "eyJhbGciOi",  # JWT header
    "BEGIN RSA PRIVATE KEY",
    "BEGIN OPENSSH PRIVATE KEY",
)
LOOT_SUBSTR = (
    "dump/vouchers/",
    "dump/accounts/",
    "dump/exports/",
    "hack/full/",
)
LOOT_EXT = {".json", ".csv", ".jsonl", ".ndjson"}

IMAGE_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"}

# 22-digit Argentine CBU if it appears as a standalone token in OUT (not SoT reviews).
CBU_RE = re.compile(r"(?<!\d)\d{22}(?!\d)")


def civil_scan(out: Path) -> dict:
    out = Path(out).expanduser().resolve()
    hits: list[dict] = []
    if not out.is_dir():
        return {"ok": False, "hits": [{"file": str(out), "why": "OUT missing"}], "scanned": 0}

    scanned = 0
    for p in out.rglob("*"):
        if not p.is_file():
            continue
        if ".bus" in p.parts:
            # PLAN/VERIFY json may cite SoT paths; still scan for JWT blobs.
            pass
        scanned += 1
        rel = str(p.relative_to(out))
        if p.name in FORBIDDEN_NAME:
            hits.append({"file": rel, "why": f"forbidden filename {p.name}"})
            continue
        if p.suffix.lower() in IMAGE_EXT:
            hits.append({"file": rel, "why": "image in civil OUT (voucher/loot risk)"})
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError as e:
            hits.append({"file": rel, "why": f"unreadable: {e}"})
            continue
        bad = False
        for s in SECRET_SUBSTR:
            if s in text:
                hits.append({"file": rel, "why": f"forbidden substring {s!r}"})
                bad = True
                break
        if not bad and p.suffix.lower() in LOOT_EXT:
            for s in LOOT_SUBSTR:
                if s in text:
                    hits.append({"file": rel, "why": f"loot path inside {p.suffix} {s!r}"})
                    bad = True
                    break
        if not bad and len(CBU_RE.findall(text)) >= 3:
            hits.append({"file": rel, "why": "multiple 22-digit tokens (possible CBU dump)"})

    rec = {
        "ok": len(hits) == 0,
        "hits": hits,
        "scanned": scanned,
        "rule": "ha-dani-civil",
    }
    return rec


def write_scan(out: Path) -> dict:
    rec = civil_scan(out)
    bus = Path(out).expanduser().resolve() / ".bus"
    bus.mkdir(parents=True, exist_ok=True)
    (bus / "CIVIL.json").write_text(json.dumps(rec, indent=2) + "\n", encoding="utf-8")
    return rec


if __name__ == "__main__":
    import argparse
    import sys

    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    rec = write_scan(Path(args.out))
    print(json.dumps(rec))
    sys.exit(0 if rec["ok"] else 1)
