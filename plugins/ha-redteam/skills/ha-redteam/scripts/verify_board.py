#!/usr/bin/env python3
"""Fail-closed board verify for ha-redteam.

READY.* + artifacts. go_count from probe/FINDINGS.jsonl only — never ready_count.
Writes OUT/.bus/VERIFY.json pack=ha-redteam for jira_sync.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED = {
    "entry": ["entry/ENTRY.md"],
    "probe": ["probe/PROBE.md"],
    "correct": ["correct/LOOPS.md"],
    "fix": ["fix/FIXES.md"],
    "docs": ["docs/AUDIT.md"],
    "jira": ["jira/JIRA.md"],
    "sync": ["sync/COLLAB-STATUS.md"],
    "lead": ["SUMMARY.md"],
}


def load_findings(out: Path) -> list[dict]:
    recs: list[dict] = []
    p = out / "probe" / "FINDINGS.jsonl"
    if not p.is_file():
        return recs
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(rec, dict) and (rec.get("path") or rec.get("title")):
            recs.append(rec)
    return recs


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
    findings = load_findings(out)
    layer_ids = ("radio", "jump", "pivot", "intel", "memory", "spawn", "learn")
    layer_ready = {ln: (bus / f"READY.{ln}").is_file() for ln in layer_ids}
    rec = {
        "ok": sum(1 for v in ready_flags.values() if v) == len(lanes),
        "pack": "ha-redteam",
        "ready": ready_flags,
        "ready_count": sum(1 for v in ready_flags.values() if v),
        "total": len(lanes),
        "missing": missing,
        "layers": layer_ready,
        "go_count": len(findings),
        "confirmed": findings,
        "go": findings,
        "note": "go_count from probe/FINDINGS.jsonl only; layers optional always-on",
    }
    (bus / "VERIFY.json").write_text(json.dumps(rec, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(rec))
    return 0 if rec["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
