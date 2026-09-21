#!/usr/bin/env python3
"""PumaPay pack router + remainder. Writes OUT/.bus/PLAN.json + NEXT.json. No grok spawn."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

LANES_FULL = ("docs", "pm", "qa", "test", "dev", "repo", "sync", "lead")
# Tick remainder: missing non-lead/sync + always sync+lead
LANES_TICK_ALWAYS = ("sync", "lead")

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
    order = ["docs", "pm", "qa", "test", "dev", "repo"]
    if is_tick:
        for ln in order:
            if not ready.get(ln):
                nxt.append(ln)
        # always add sync/lead at end for tick if not ready (but typically run anyway)
        for ln in LANES_TICK_ALWAYS:
            if not ready.get(ln):
                nxt.append(ln)
    else:
        for ln in LANES_FULL:
            if not ready.get(ln):
                nxt.append(ln)
    # dedup preserve order
    seen = set()
    out = []
    for x in nxt:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out

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
        "pack": "ha-pumapay",
        "workflow": "ha-pumapay",
        "conductor": "ha-pumapay",
        "out": str(out),
        "ready": ready,
        "next": nxt,
        "ready_count": sum(1 for k,vv in ready.items() if vv),
        "total_lanes": len(LANES_FULL),
        "action": "spawn" if nxt else "done",
        "note": "Parent launches workflow. Skip READY lanes with on-disk artifacts. Use pp-sync + pp-lead always on tick.",
    }
    _write(out, "PLAN.json", rec)
    _write(out, "NEXT.json", {"next": nxt, "action": rec["action"], "pack": "ha-pumapay", "out": str(out)})
    return rec

def remainder(out_arg: str) -> dict:
    out = Path(out_arg).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)
    (out / ".bus").mkdir(exist_ok=True)
    ready = ready_map(out)
    nxt = next_lanes(ready, is_tick=True)
    # for tick, ensure sync and lead are considered
    if "sync" not in nxt:
        nxt.append("sync")
    if "lead" not in nxt:
        nxt.append("lead")
    # dedup
    seen = set()
    nxt = [x for x in nxt if not (x in seen or seen.add(x))]
    rec = {
        "ok": True,
        "pack": "ha-pumapay-tick",
        "workflow": "ha-pumapay-tick",
        "out": str(out),
        "ready": ready,
        "next": nxt,
        "action": "spawn" if nxt else "done",
        "note": "Tick remainder + always sync+lead",
    }
    _write(out, "PLAN.json", rec)
    _write(out, "NEXT.json", {"next": nxt, "action": rec["action"], "pack": "ha-pumapay-tick", "out": str(out)})
    return rec

def status(out_arg: str) -> dict:
    out = Path(out_arg).expanduser().resolve()
    rec = plan(out_arg)  # reuse plan logic
    rec["verify"] = read_verify(out)
    rec["next"] = next_lanes(rec["ready"], is_tick=False)
    print(json.dumps(rec, indent=2))
    return rec

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", nargs="?", default="plan", choices=["plan", "status", "remainder"])
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    if args.cmd == "plan":
        rec = plan(args.out)
    elif args.cmd == "remainder":
        rec = remainder(args.out)
    else:
        rec = status(args.out)
    if args.cmd != "status":
        print(json.dumps(rec))
    return 0

if __name__ == "__main__":
    sys.exit(main())
