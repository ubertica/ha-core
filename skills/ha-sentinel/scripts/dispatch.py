#!/usr/bin/env python3
"""ha-sentinel pack router + remainder. Writes OUT/.bus/PLAN.json + NEXT.json. No grok spawn."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

LANES_FULL = ("watch", "ollama", "audit", "improve", "release", "escalate", "collab", "lead")
# Tick remainder: missing non-lead + always escalate/collab/lead
LANES_TICK_ALWAYS = ("escalate", "collab", "lead")

def ready_map(out: Path) -> dict[str, bool]:
    bus = out / ".bus"
    m = {}
    for lane in LANES_FULL:
        m[lane] = (bus / f"READY.{lane}").is_file()
    return m

def read_verify(out: Path) -> dict:
    v = out / ".bus" / "VERIFY.json"
    if not v.is_file():
        return {"ok": False, "ready_count": 0, "total": len(LANES_FULL)}
    try:
        data = json.loads(v.read_text())
        return data
    except Exception:
        return {"ok": False, "ready_count": 0, "total": len(LANES_FULL)}

def next_lanes(ready: dict[str, bool], is_tick: bool) -> list[str]:
    nxt: list[str] = []
    order = ["watch", "ollama", "audit", "improve", "release"]
    if is_tick:
        for ln in order:
            if not ready.get(ln):
                nxt.append(ln)
        for ln in LANES_TICK_ALWAYS:
            if not ready.get(ln):
                nxt.append(ln)
    else:
        for ln in LANES_FULL:
            if not ready.get(ln):
                nxt.append(ln)
    seen = set()
    outl = []
    for x in nxt:
        if x not in seen:
            seen.add(x)
            outl.append(x)
    return outl

def _write(out: Path, name: str, rec: dict) -> None:
    bus = out / ".bus"
    bus.mkdir(parents=True, exist_ok=True)
    (bus / name).write_text(json.dumps(rec, indent=2) + "\n", encoding="utf-8")

def plan(out_arg: str) -> dict:
    out = Path(out_arg).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)
    (out / ".bus").mkdir(exist_ok=True)
    ready = ready_map(out)
    nxt = next_lanes(ready, is_tick=False)
    v = read_verify(out)
    rec = {
        "ok": True,
        "pack": "ha-sentinel",
        "workflow": "ha-sentinel",
        "conductor": "ha-sentinel",
        "out": str(out),
        "ready": ready,
        "next": nxt,
        "ready_count": sum(1 for k,vv in ready.items() if vv),
        "total_lanes": len(LANES_FULL),
        "action": "spawn" if nxt else "done",
        "note": "Parent launches workflow. Skip READY lanes. Use escalate+collab+lead always on tick.",
    }
    _write(out, "PLAN.json", rec)
    print(json.dumps(rec))
    return rec

def remainder(out_arg: str) -> dict:
    out = Path(out_arg).expanduser().resolve()
    ready = ready_map(out)
    nxt = next_lanes(ready, is_tick=True)
    rec = {
        "ok": True,
        "pack": "ha-sentinel",
        "workflow": "ha-sentinel-tick",
        "out": str(out),
        "ready": ready,
        "next": nxt,
        "ready_count": sum(1 for k,vv in ready.items() if vv),
        "total_lanes": len(LANES_FULL),
        "action": "spawn" if nxt else "done",
    }
    _write(out, "NEXT.json", rec)
    print(json.dumps(rec))
    return rec

def status(out_arg: str) -> dict:
    out = Path(out_arg).expanduser().resolve()
    ready = ready_map(out)
    v = read_verify(out)
    rec = {"ok": True, "out": str(out), "ready": ready, "verify": v}
    print(json.dumps(rec, indent=2))
    return rec

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=["plan", "remainder", "status"])
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    if args.action == "plan":
        plan(args.out)
    elif args.action == "remainder":
        remainder(args.out)
    else:
        status(args.out)
    return 0

if __name__ == "__main__":
    sys.exit(main())
