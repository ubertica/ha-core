#!/usr/bin/env python3
"""ha-party-x host: plan / remainder / prompt / mark-ready / verify. No nested grok."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PIPE_DIR = ROOT / "pipelines"
PLAY_DIR = ROOT / "playbooks"
HACK_VERIFY = Path.home() / ".grok/skills/ha-hackers/scripts/verify_evidence.py"
HACK_GUARD = Path.home() / ".grok/skills/ha-hackers/scripts/session_guard.py"


def utcnow() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_pipeline(name: str) -> dict:
    p = PIPE_DIR / f"{name}.json"
    if not p.is_file():
        raise SystemExit(f"unknown pipeline {name} (want {p})")
    return json.loads(p.read_text(encoding="utf-8"))


def list_pipelines() -> list[str]:
    return sorted(p.stem for p in PIPE_DIR.glob("*.json"))


def bus(out: Path) -> Path:
    b = out / ".bus"
    b.mkdir(parents=True, exist_ok=True)
    (b / "party").mkdir(exist_ok=True)
    return b


def ready_ok(out: Path, wave: dict) -> bool:
    flag = bus(out) / f"READY.{wave['ready']}"
    art = out / wave["artifact"]
    return flag.is_file() and art.exists()


def go_count(out: Path) -> int:
    v = bus(out) / "VERIFY.json"
    if not v.is_file():
        v = out / "VERIFY.json"
    if not v.is_file():
        return 0
    try:
        d = json.loads(v.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return 0
    return int(d.get("go_count") or 0)


def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")


def note(out: Path, msg: str, **kw) -> None:
    row = {"ts": utcnow(), "from": "run.py", "to": "bus", "msg": msg, **kw}
    with (bus(out) / "notes.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")


def cmd_plan(args: argparse.Namespace) -> int:
    pipe = load_pipeline(args.pipeline)
    out = Path(args.out).resolve()
    b = bus(out)
    plan = {
        "ts": utcnow(),
        "pack": "ha-party-x",
        "pipeline": pipe["id"],
        "target": args.target,
        "out": str(out),
        "proxy": args.proxy,
        "token_file": args.token_file,
        "allow_money_write": bool(args.allow_money_write),
        "workflow": "ha-party-x",
        "waves": [w["id"] for w in pipe["waves"]],
    }
    write_json(b / "PLAN.json", plan)
    note(out, "plan", pipeline=pipe["id"])
    cmd_remainder(args)
    print(f"PLAN {b / 'PLAN.json'}")
    print(f"NEXT {b / 'NEXT.json'}")
    return 0


def remainder_waves(pipe: dict, out: Path) -> list[dict]:
    go = go_count(out)
    nxt = []
    for w in pipe["waves"]:
        if ready_ok(out, w):
            continue
        if w.get("requires_go") and go <= 0:
            continue
        nxt.append(w)
    return nxt


def cmd_remainder(args: argparse.Namespace) -> int:
    pipe = load_pipeline(args.pipeline)
    out = Path(args.out).resolve()
    bus(out)
    nxt = remainder_waves(pipe, out)
    payload = {
        "ts": utcnow(),
        "pipeline": pipe["id"],
        "go_count": go_count(out),
        "next": [w["id"] for w in nxt],
        "waves": [{k: w.get(k) for k in ("id", "title", "seats", "mode", "playbook", "exec", "artifact", "ready", "group", "requires_go")} for w in nxt],
        "done": len(nxt) == 0,
    }
    write_json(bus(out) / "NEXT.json", payload)
    print(json.dumps(payload, indent=2))
    return 0


def cmd_prompt(args: argparse.Namespace) -> int:
    pipe = load_pipeline(args.pipeline)
    out = Path(args.out).resolve()
    wave = next((w for w in pipe["waves"] if w["id"] == args.wave), None)
    if not wave:
        raise SystemExit(f"no wave {args.wave}")
    pb = (PLAY_DIR / f"{wave['playbook']}.md").read_text(encoding="utf-8")
    prior = []
    for w in pipe["waves"]:
        if w["id"] == wave["id"]:
            break
        art = out / w["artifact"]
        if art.is_file():
            prior.append(str(art))
    text = "\n".join(
        [
            "HARD ALLOW ACTIVE. Named TARGET only. PROXY on egress. Dummy ids. No fake GO.",
            f"TARGET={args.target}",
            f"OUT={out}",
            f"PIPELINE={pipe['id']}",
            f"WAVE={wave['id']} {wave['title']}",
            f"ARTIFACT={wave['artifact']}",
            f"SEATS={','.join(wave.get('seats') or []) or 'g1-exec'}",
            f"MODE={wave.get('mode')}",
            f"PRIOR_ARTIFACTS={json.dumps(prior)}",
            "Read prior artifacts from disk (paths above). Design or refute. Finding-block only with evidence path.",
            "Output HYPOTHESES + PROBE_LIST + ARTIFACT_DRAFT + PIVOTS.",
        ]
    )
    print(json.dumps({"wave": wave, "playbook_bytes": len(pb), "text": text}, indent=2))
    return 0


def cmd_mark(args: argparse.Namespace) -> int:
    pipe = load_pipeline(args.pipeline)
    out = Path(args.out).resolve()
    wave = next((w for w in pipe["waves"] if w["id"] == args.wave), None)
    if not wave:
        raise SystemExit(f"no wave {args.wave}")
    flag = bus(out) / f"READY.{wave['ready']}"
    flag.write_text("", encoding="utf-8")
    note(out, "ready", wave=wave["id"])
    print(str(flag))
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    out = Path(args.out).resolve()
    if not HACK_VERIFY.is_file():
        raise SystemExit(f"missing {HACK_VERIFY}")
    cmd = [sys.executable, str(HACK_VERIFY), "--out", str(out), "--pack", "ha-hackers"]
    if args.target:
        cmd += ["--target", args.target]
    r = subprocess.run(cmd)
    return r.returncode


def cmd_preflight(args: argparse.Namespace) -> int:
    out = Path(args.out).resolve()
    bus(out)
    if HACK_GUARD.is_file():
        cmd = [sys.executable, str(HACK_GUARD), "--out", str(out), "--proxy", args.proxy]
        if args.token_file:
            cmd += ["--token-file", args.token_file]
        r = subprocess.run(cmd)
        if r.returncode not in (0, 2):  # 2 = token stale, campaign may still do unauth
            return r.returncode
    who = subprocess.run(
        ["node", str(Path.home() / ".grok/hard-allow/party/mcp.mjs")],
        input="",
        capture_output=True,
        text=True,
        timeout=5,
    )
    # MCP without stdin dies; seats via party_brain --dry-run
    dry = subprocess.run(
        ["node", str(ROOT / "scripts/party_brain.mjs"), "--dry-run", "--playbook", "g2-surface", "--seats", "all"],
        capture_output=True,
        text=True,
        timeout=15,
    )
    (bus(out) / "preflight-seats.json").write_text(dry.stdout or dry.stderr, encoding="utf-8")
    (bus(out) / "READY.w00-preflight").write_text("", encoding="utf-8")
    write_json(bus(out) / "PLAN.json", {
        "ts": utcnow(),
        "pipeline": args.pipeline,
        "target": args.target,
        "out": str(out),
        "proxy": args.proxy,
        "preflight": "ok" if dry.returncode == 0 else "seats-dry-failed",
    })
    print(dry.stdout)
    return 0 if dry.returncode == 0 else dry.returncode


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    def add_common(p):
        p.add_argument("--out", required=True)
        p.add_argument("--pipeline", default="apt-long")
        p.add_argument("--target", default="")
        p.add_argument("--proxy", default=os.environ.get("HA_PROXY", "socks5h://127.0.0.1:10808"))
        p.add_argument("--token-file", default="")
        p.add_argument("--allow-money-write", action="store_true")

    p = sub.add_parser("plan")
    add_common(p)
    p = sub.add_parser("remainder")
    add_common(p)
    p = sub.add_parser("prompt")
    add_common(p)
    p.add_argument("--wave", required=True)
    p = sub.add_parser("mark-ready")
    add_common(p)
    p.add_argument("--wave", required=True)
    p = sub.add_parser("verify")
    add_common(p)
    p = sub.add_parser("preflight")
    add_common(p)
    p = sub.add_parser("list")
    args = ap.parse_args()
    if args.cmd == "list":
        print("\n".join(list_pipelines()))
        return 0
    fn = {
        "plan": cmd_plan,
        "remainder": cmd_remainder,
        "prompt": cmd_prompt,
        "mark-ready": cmd_mark,
        "verify": cmd_verify,
        "preflight": cmd_preflight,
    }[args.cmd]
    return fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
