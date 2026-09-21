#!/usr/bin/env python3
"""ha-sre pack router + remainder. Writes OUT/.bus/PLAN.json + NEXT.json. No grok spawn."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

LANES_FULL = ("slo", "deploy", "oncall", "change", "dev", "sync", "lead")
LANES_TICK_ALWAYS = ("lead",)  # always run lead on tick; add sync if present

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
    order = [l for l in LANES_FULL if l not in LANES_TICK_ALWAYS]
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
    out_l = []
    for x in nxt:
        if x not in seen:
            seen.add(x)
            out_l.append(x)
    return out_l

def _write(out: Path, name: str, rec: dict) -> None:
    bus = out / ".bus"
    bus.mkdir(parents=True, exist_ok=True)
    (bus / name).write_text(json.dumps(rec, indent=2) + "\n", encoding="utf-8")

def plan(out_arg: str, lanes_json: str | None = None) -> dict:
    out = Path(out_arg).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)
    (out / ".bus").mkdir(exist_ok=True)
    ready = ready_map(out)
    nxt = next_lanes(ready, is_tick=False)
    v = read_verify(out)
    rec = {
        "ok": True,
        "pack": "ha-sre",
        "workflow": "ha-sre",
        "conductor": "ha-sre",
        "out": str(out),
        "ready": ready,
        "next": nxt,
        "ready_count": sum(1 for k,vv in ready.items() if vv),
        "total_lanes": len(LANES_FULL),
        "action": "spawn" if nxt else "done",
        "note": "Parent launches workflow. Skip READY lanes with on-disk artifacts.",
    }
    _write(out, "PLAN.json", rec)
    _write(out, "NEXT.json", {"next": nxt, "action": rec["action"], "pack": "ha-sre", "out": str(out)})
    return rec

def remainder(out_arg: str) -> dict:
    out = Path(out_arg).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)
    (out / ".bus").mkdir(exist_ok=True)
    ready = ready_map(out)
    nxt = next_lanes(ready, is_tick=True)
    for ln in LANES_TICK_ALWAYS:
        if ln not in nxt:
            nxt.append(ln)
    seen = set()
    nxt = [x for x in nxt if not (x in seen or seen.add(x))]
    rec = {
        "ok": True,
        "pack": "ha-sre-tick",
        "workflow": "ha-sre-tick",
        "out": str(out),
        "ready": ready,
        "next": nxt,
        "action": "spawn" if nxt else "done",
        "note": "Tick remainder + always lead (and sync if configured)",
    }
    _write(out, "PLAN.json", rec)
    _write(out, "NEXT.json", {"next": nxt, "action": rec["action"], "pack": "ha-sre-tick", "out": str(out)})
    return rec

def status(out_arg: str) -> dict:
    out = Path(out_arg).expanduser().resolve()
    rec = plan(out_arg)
    rec["verify"] = read_verify(out)
    print(json.dumps(rec, indent=2))
    return rec

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", nargs="?", default="plan", choices=["plan", "status", "remainder"])
    ap.add_argument("--out", required=True)
    ap.add_argument("--lanes", default=None)
    args = ap.parse_args()
    if args.cmd == "plan":
        rec = plan(args.out, args.lanes)
    elif args.cmd == "remainder":
        rec = remainder(args.out)
    else:
        rec = status(args.out)
    if args.cmd != "status":
        print(json.dumps(rec))
    return 0

if __name__ == "__main__":
    sys.exit(main())
