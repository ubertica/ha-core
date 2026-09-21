#!/usr/bin/env python3
"""Fail closed if pack is incomplete. No live TARGET, no party API spend."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PIPE = ROOT / "pipelines"
PLAY = ROOT / "playbooks"
NEED_PLAY = ["conductor", "g2-surface", "g3-weapon", "g4-adversary"]
NEED_PIPE = ["apt-long", "0day-deep", "authz-brutal", "docs-entry-x", "red-on-red"]
WAVE_KEYS = {"id", "group", "title", "seats", "mode", "playbook", "exec", "artifact", "ready"}


def fail(msg: str) -> None:
    print(f"FAIL {msg}")
    sys.exit(1)


def main() -> int:
    for n in NEED_PLAY:
        p = PLAY / f"{n}.md"
        if not p.is_file() or p.stat().st_size < 200:
            fail(f"playbook {p}")
    ids = []
    for n in NEED_PIPE:
        p = PIPE / f"{n}.json"
        d = json.loads(p.read_text(encoding="utf-8"))
        if d.get("id") != n:
            fail(f"pipeline id {n}")
        waves = d.get("waves") or []
        if len(waves) < 6:
            fail(f"{n} too short ({len(waves)})")
        seen = set()
        for w in waves:
            missing = WAVE_KEYS - set(w)
            if missing:
                fail(f"{n}.{w.get('id')} missing {missing}")
            if w["id"] in seen:
                fail(f"dup wave {w['id']}")
            seen.add(w["id"])
            pb = PLAY / f"{w['playbook']}.md"
            if not pb.is_file():
                fail(f"{n}.{w['id']} playbook {w['playbook']}")
            if w.get("mode") not in ("exec", "parallel", "round"):
                fail(f"{n}.{w['id']} mode")
        ids.append(f"{n}:{len(waves)}")
        print(f"OK pipeline {n} waves={len(waves)}")

    apt = json.loads((PIPE / "apt-long.json").read_text())
    if len(apt["waves"]) < 16:
        fail("apt-long must stay longer than ha-hackers 5-lane")

    dry = subprocess.run(
        ["node", str(ROOT / "scripts/party_brain.mjs"), "--dry-run", "--playbook", "g3-weapon", "--seats", "g2,g4"],
        capture_output=True,
        text=True,
        timeout=20,
    )
    if dry.returncode != 0:
        fail(f"party_brain dry {dry.returncode} {dry.stderr}")
    j = json.loads(dry.stdout)
    if not j.get("ok") or j.get("extra_bytes", 0) < 200:
        fail(f"dry payload {j}")
    print(f"OK party_brain dry ids={j.get('ids')}")

    import tempfile

    with tempfile.TemporaryDirectory() as td:
        out = Path(td)
        r = subprocess.run(
            [sys.executable, str(ROOT / "scripts/run.py"), "plan", "--out", str(out), "--target", "https://example.invalid", "--pipeline", "apt-long"],
            capture_output=True,
            text=True,
            timeout=20,
        )
        if r.returncode != 0:
            fail(f"plan {r.returncode} {r.stderr}")
        nxt = json.loads((out / ".bus/NEXT.json").read_text())
        if nxt["next"][0] != "w00-preflight":
            fail(f"first remainder {nxt['next'][:3]}")
        (out / ".bus/READY.w00-preflight").write_text("")
        (out / ".bus/PLAN.json").write_text("{}")
        r2 = subprocess.run(
            [sys.executable, str(ROOT / "scripts/run.py"), "remainder", "--out", str(out), "--pipeline", "apt-long"],
            capture_output=True,
            text=True,
            timeout=20,
        )
        nxt2 = json.loads((out / ".bus/NEXT.json").read_text())
        if "w00-preflight" in nxt2["next"]:
            fail("READY skip broken")
        print("OK remainder skips READY")

    print("PASS ha-party-x selftest " + " ".join(ids))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
