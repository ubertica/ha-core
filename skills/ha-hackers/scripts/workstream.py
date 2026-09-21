#!/usr/bin/env python3
"""Collective R&D bus. Open workstreams survive session death. No nested grok."""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

KINDS = ("0day", "chain", "pivot", "creds", "lateral")
AGENTS = {
    "0day": "hack-0day",
    "chain": "hack-chain",
    "pivot": "hack-0day",
    "creds": "hack-chain",
    "lateral": "hack-chain",
}


def bus_path(out: Path) -> Path:
    p = out / ".bus"
    p.mkdir(parents=True, exist_ok=True)
    return p / "WORKSTREAMS.jsonl"


def load(out: Path) -> list[dict]:
    f = bus_path(out)
    if not f.is_file():
        return []
    rows = []
    for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def latest_by_id(rows: list[dict]) -> dict[str, dict]:
    m: dict[str, dict] = {}
    for r in rows:
        i = r.get("id")
        if i:
            m[str(i)] = r
    return m


def append(out: Path, rec: dict) -> None:
    rec.setdefault("ts", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    with bus_path(out).open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")


def cmd_add(args: argparse.Namespace) -> dict:
    out = Path(args.out).expanduser().resolve()
    rec = {
        "id": args.id,
        "kind": args.kind,
        "title": args.title,
        "hypothesis": args.hypothesis or "",
        "status": "open",
        "agent": AGENTS.get(args.kind, "hack-0day"),
        "evidence": args.evidence or "",
    }
    append(out, rec)
    return rec


def cmd_close(args: argparse.Namespace) -> dict:
    out = Path(args.out).expanduser().resolve()
    rec = {
        "id": args.id,
        "status": "closed",
        "why": args.why or "",
    }
    append(out, rec)
    return rec


def cmd_next(args: argparse.Namespace) -> dict:
    out = Path(args.out).expanduser().resolve()
    latest = latest_by_id(load(out))
    open_ws = [v for v in latest.values() if v.get("status") == "open"]
    nxt = []
    seen = set()
    for w in open_ws:
        a = w.get("agent") or AGENTS.get(w.get("kind") or "", "hack-0day")
        if a not in seen:
            seen.add(a)
            nxt.append(a)
    rec = {
        "ok": True,
        "open": open_ws,
        "next": nxt,
        "action": "spawn" if nxt else "done",
    }
    (out / ".bus" / "WORKSTREAMS.next.json").write_text(
        json.dumps(rec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return rec


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("--out", required=True)
    a.add_argument("--id", required=True)
    a.add_argument("--kind", required=True, choices=KINDS)
    a.add_argument("--title", required=True)
    a.add_argument("--hypothesis", default="")
    a.add_argument("--evidence", default="")
    c = sub.add_parser("close")
    c.add_argument("--out", required=True)
    c.add_argument("--id", required=True)
    c.add_argument("--why", default="")
    n = sub.add_parser("next")
    n.add_argument("--out", required=True)
    args = ap.parse_args()
    fn = {"add": cmd_add, "close": cmd_close, "next": cmd_next}[args.cmd]
    print(json.dumps(fn(args)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
