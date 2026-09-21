#!/usr/bin/env python3
"""Next hosts from disk FINDINGS only. No invented jump."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlparse

HOST_RE = re.compile(r"https?://([^/\s]+)", re.I)


def hosts_from(text: str) -> list[str]:
    found: list[str] = []
    for m in HOST_RE.finditer(text or ""):
        h = m.group(1).split(":")[0].lower()
        if h and h not in found:
            found.append(h)
    return found


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    out = Path(args.out).expanduser().resolve()
    findings = out / "probe" / "FINDINGS.jsonl"
    entry = out / "entry" / "ENTRY.md"
    blob = ""
    recs = []
    if findings.is_file():
        for line in findings.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            recs.append(rec)
            blob += " " + json.dumps(rec)
    if entry.is_file():
        blob += " " + entry.read_text(encoding="utf-8")[:20000]
    tgt = out / ".bus" / "TARGET"
    current = tgt.read_text(encoding="utf-8").strip() if tgt.is_file() else ""
    cur_host = ""
    if current.startswith("http"):
        cur_host = (urlparse(current).hostname or "").lower()
    hs = [h for h in hosts_from(blob) if h != cur_host]
    nxt = {"ok": True, "current": current, "next_hosts": hs, "n_findings": len(recs), "invented": False}
    bus = out / ".bus"
    bus.mkdir(parents=True, exist_ok=True)
    (bus / "NEXT-HOSTS.json").write_text(json.dumps(nxt, indent=2) + "\n", encoding="utf-8")
    jump = out / "jump"
    jump.mkdir(parents=True, exist_ok=True)
    lines = [
        "# JUMP",
        "",
        f"current: `{current or 'none'}`",
        f"next_hosts: {hs or '[]'}",
        "",
        "Jump only these. Evidence on disk. Invalidate stale READY after switch.",
        "",
    ]
    (jump / "JUMP.md").write_text("\n".join(lines), encoding="utf-8")
    (bus / "READY.jump").write_text("ok\n", encoding="utf-8")
    print(json.dumps(nxt))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
