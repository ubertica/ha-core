#!/usr/bin/env python3
"""Pack router + remainder plan. Does NOT spawn grok. Writes OUT/.bus/PLAN.json + NEXT.json."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

DOCS_HINTS = ("/docs", "/swagger", "openapi", "/api-docs")

# docs-entry uses namespaced exploit/lead so ha-hackers READY.exploit does not short-circuit
LANES_DOCS = ("entry", "webhook", "docs-exploit", "docs-lead")
LANES_HACK = ("recon", "api", "authz", "exploit", "lead")

AGENT_FOR = {
    "entry": "hack-entry",
    "webhook": "hack-webhook",
    "docs-exploit": "hack-exploit",
    "docs-lead": "hack-lead",
    "recon": "hack-recon",
    "api": "hack-api",
    "authz": "hack-authz",
    "exploit": "hack-exploit",
    "lead": "hack-lead",
}


def classify_pack(target: str, pack: str) -> str:
    if pack in {"docs-entry", "ha-hackers"}:
        return pack
    t = (target or "").lower()
    for h in DOCS_HINTS:
        if h in t:
            return "docs-entry"
    return "ha-hackers"


def ready_map(out: Path, lanes: tuple[str, ...]) -> dict[str, bool]:
    bus = out / ".bus"
    m = {}
    for lane in lanes:
        m[lane] = (bus / f"READY.{lane}").is_file()
    if "entry" in m:
        m["docs-authz"] = (bus / "READY.docs-authz").is_file()
        m["docs-api"] = (bus / "READY.docs-api").is_file()
    return m


def read_go_count(out: Path) -> int:
    verify = out / ".bus" / "VERIFY.json"
    if not verify.is_file():
        return 0
    try:
        return int(json.loads(verify.read_text()).get("go_count") or 0)
    except (json.JSONDecodeError, ValueError, TypeError):
        return 0


def next_lanes(pack: str, ready: dict[str, bool], go_count: int) -> list[str]:
    if pack == "docs-entry":
        nxt: list[str] = []
        if not ready.get("entry"):
            nxt.append("hack-entry")
        if not ready.get("webhook"):
            nxt.append("hack-webhook")
        if ready.get("entry") and ready.get("webhook"):
            if go_count > 0:
                if not ready.get("docs-exploit"):
                    nxt.append("hack-exploit")
                if not ready.get("docs-lead"):
                    nxt.append("hack-lead")
        return nxt
    nxt = []
    if not ready.get("recon"):
        nxt.append("hack-recon")
    if not ready.get("api"):
        nxt.append("hack-api")
    if ready.get("recon") and ready.get("api") and not ready.get("authz"):
        nxt.append("hack-authz")
    if ready.get("authz"):
        if go_count > 0 and not ready.get("exploit"):
            nxt.append("hack-exploit")
        if not ready.get("lead"):
            nxt.append("hack-lead")
    return nxt


def workflow_name(pack: str) -> str:
    return "docs-entry" if pack == "docs-entry" else "ha-hackers"


def workstream_next(out: Path) -> list[str]:
    f = out / ".bus" / "WORKSTREAMS.jsonl"
    if not f.is_file():
        return []
    latest: dict[str, dict] = {}
    for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        i = rec.get("id")
        if i:
            latest[str(i)] = rec
    agents = []
    seen = set()
    kind_agent = {
        "0day": "hack-0day",
        "chain": "hack-chain",
        "pivot": "hack-0day",
        "creds": "hack-chain",
        "lateral": "hack-chain",
    }
    for w in latest.values():
        if w.get("status") != "open":
            continue
        a = w.get("agent") or kind_agent.get(w.get("kind") or "", "hack-0day")
        if a not in seen:
            seen.add(a)
            agents.append(a)
    return agents


def action_for(pack: str, ready: dict[str, bool], nxt: list[str], token_stale: bool) -> str:
    if token_stale and pack == "ha-hackers":
        return "need-token"
    if nxt:
        return "spawn"
    if pack == "docs-entry":
        if ready.get("entry") and ready.get("webhook"):
            return "done"
        return "wait"
    if ready.get("authz") and ready.get("lead"):
        return "done"
    return "wait"


def _write(out: Path, name: str, rec: dict) -> None:
    (out / ".bus").mkdir(parents=True, exist_ok=True)
    (out / ".bus" / name).write_text(json.dumps(rec, indent=2) + "\n", encoding="utf-8")


def plan(args: argparse.Namespace) -> dict:
    out = Path(args.out).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)
    (out / ".bus").mkdir(exist_ok=True)
    pack = classify_pack(args.target, args.pack)
    if pack == "docs-entry":
        (out / "docs-entry").mkdir(exist_ok=True)
    lanes = LANES_DOCS if pack == "docs-entry" else LANES_HACK
    ready = ready_map(out, lanes)
    go_count = read_go_count(out)
    nxt = next_lanes(pack, ready, go_count)
    if not nxt:
        for a in workstream_next(out):
            if a not in nxt:
                nxt.append(a)
    token_stale = (out / ".bus" / "TOKEN.stale").is_file()
    rec = {
        "ok": True,
        "pack": pack,
        "workflow": workflow_name(pack),
        "conductor": "ha-auto",
        "target": args.target,
        "out": str(out),
        "token_file": args.token_file or "",
        "proxy": args.proxy or "",
        "need_token": pack == "ha-hackers" or bool(args.need_token),
        "allow_money_write": bool(args.allow_money_write),
        "ready": ready,
        "next": nxt,
        "go_count": go_count,
        "action": action_for(pack, ready, nxt, token_stale),
        "token_stale": token_stale,
        "launch": "workflow",
        "note": "Parent launches workflow name=ha-auto (or PLAN.workflow). Do not nested grok -p. Skip READY lanes.",
    }
    _write(out, "PLAN.json", rec)
    _write(out, "NEXT.json", {"next": nxt, "action": rec["action"], "go_count": go_count, "pack": pack})
    return rec


def status(args: argparse.Namespace) -> dict:
    out = Path(args.out).expanduser().resolve()
    rec = plan(args)
    v = out / ".bus" / "VERIFY.json"
    if v.is_file():
        try:
            rec["verify"] = json.loads(v.read_text())
            rec["go_count"] = rec["verify"].get("go_count") or 0
        except json.JSONDecodeError:
            pass
        rec["next"] = next_lanes(rec["pack"], rec["ready"], rec["go_count"])
        if not rec["next"]:
            for a in workstream_next(out):
                if a not in rec["next"]:
                    rec["next"].append(a)
        rec["action"] = action_for(
            rec["pack"], rec["ready"], rec["next"], rec.get("token_stale", False)
        )
        _write(out, "NEXT.json", {
            "next": rec["next"],
            "action": rec["action"],
            "go_count": rec["go_count"],
            "pack": rec["pack"],
        })
    return rec


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", nargs="?", default="plan", choices=["plan", "status", "remainder"])
    ap.add_argument("--target", default="")
    ap.add_argument("--out", required=True)
    ap.add_argument("--token-file", default="")
    ap.add_argument("--proxy", default="")
    ap.add_argument("--pack", default="auto")
    ap.add_argument("--need-token", action="store_true")
    ap.add_argument("--allow-money-write", action="store_true")
    args = ap.parse_args()
    rec = plan(args) if args.cmd == "plan" else status(args)
    print(json.dumps(rec))
    return 0


if __name__ == "__main__":
    sys.exit(main())
