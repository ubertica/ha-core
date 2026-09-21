#!/usr/bin/env python3
"""PumaPay docs↔dev consensus bus helpers."""
from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def append_log(bus: Path, obj: dict) -> None:
    path = bus / "consensus.jsonl"
    with path.open("a") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def propose(bus: Path, repo: str, id_: str, title: str, paths: list[str], question: str) -> dict:
    prop = {
        "id": id_,
        "ts": now(),
        "from": "grok-ha",
        "type": "proposal",
        "title": title,
        "paths": paths,
        "question": question,
        "repo": repo,
        "status": "open",
    }
    (bus / "proposals" / f"{id_}.json").write_text(json.dumps(prop, indent=2) + "\n")
    append_log(bus, prop)
    # mirror stub in repo
    mirror = Path(os.path.expanduser(repo)) / "docs" / "consensus" / "proposals"
    mirror.mkdir(parents=True, exist_ok=True)
    (mirror / f"{id_}.json").write_text(json.dumps(prop, indent=2) + "\n")
    print(json.dumps({"ok": True, "proposal": str(bus / "proposals" / f"{id_}.json")}))
    return prop


def plan(bus: Path, id_: str) -> None:
    p = bus / "proposals" / f"{id_}.json"
    if not p.exists():
        raise SystemExit(f"missing proposal {p}")
    prop = json.loads(p.read_text())
    out = {
        "ok": True,
        "workflow": "ha-pp-consensus",
        "id": id_,
        "proposal": prop,
        "need_docs": not (bus / "proposals" / f"{id_}.docs.json").exists(),
        "need_dev": not (bus / "proposals" / f"{id_}.dev.json").exists(),
    }
    (bus / "proposals" / f"{id_}.PLAN.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out))


def _load_vote(bus: Path, id_: str, side: str) -> dict | None:
    p = bus / "proposals" / f"{id_}.{side}.json"
    if not p.exists():
        return None
    return json.loads(p.read_text())


def verify(bus: Path, id_: str) -> dict:
    prop_path = bus / "proposals" / f"{id_}.json"
    if not prop_path.exists():
        out = {"ok": False, "error": "no proposal", "id": id_}
        print(json.dumps(out))
        return out
    docs = _load_vote(bus, id_, "docs")
    dev = _load_vote(bus, id_, "dev")
    if not docs or not dev:
        out = {
            "ok": False,
            "status": "incomplete",
            "id": id_,
            "have_docs": bool(docs),
            "have_dev": bool(dev),
        }
        print(json.dumps(out))
        return out

    dv = (docs.get("vote") or "").lower()
    ev = (dev.get("vote") or "").lower()
    if dv == "nack" or ev == "nack":
        status = "hold"
        ok = False
    elif dv in ("ack", "revise") and ev in ("ack", "revise"):
        if dv == "ack" and ev == "ack":
            status = "decided"
            ok = True
        else:
            status = "revise"
            ok = False
    else:
        status = "hold"
        ok = False

    decision = {
        "id": id_,
        "ts": now(),
        "type": "decision",
        "status": status,
        "docs_vote": dv,
        "dev_vote": ev,
        "docs": docs,
        "dev": dev,
        "paths": json.loads(prop_path.read_text()).get("paths"),
        "summary": f"docs={dv} dev={ev} → {status}",
    }
    (bus / "decisions" / f"{id_}.json").write_text(json.dumps(decision, indent=2) + "\n")
    append_log(bus, {k: decision[k] for k in ("id", "ts", "type", "status", "docs_vote", "dev_vote", "summary")})

    # board digest
    board = bus.parent / "board.jsonl"
    with board.open("a") as f:
        f.write(
            json.dumps(
                {
                    "ts": now(),
                    "from": "ha-pp-consensus",
                    "to": "ha-ppdev|ha-pumapay",
                    "type": "consensus",
                    "severity": "info" if ok else "med",
                    "msg": decision["summary"],
                    "ids": {"consensus_id": id_, "status": status},
                }
            )
            + "\n"
        )

    # repo mirror
    repo = Path(os.path.expanduser(json.loads(prop_path.read_text()).get("repo") or "~/dev/pumapay"))
    ddir = repo / "docs" / "consensus" / "decisions"
    ddir.mkdir(parents=True, exist_ok=True)
    md = [
        f"# Decision `{id_}`\n",
        f"**Status:** {status}  \n",
        f"**Docs:** {dv} · **Dev:** {ev}  \n",
        f"**TS:** {decision['ts']}\n\n",
        "## Docs notes\n\n",
        (docs.get("notes") or "") + "\n\n",
        "## Dev notes\n\n",
        (dev.get("notes") or "") + "\n\n",
        "## Blockers\n\n",
        json.dumps({"docs": docs.get("blockers"), "dev": dev.get("blockers")}, indent=2) + "\n",
    ]
    (ddir / f"{id_}.md").write_text("".join(md))

    out = {"ok": ok, **decision}
    print(json.dumps(out))
    return out


def status(bus: Path, id_: str | None) -> None:
    if id_:
        verify(bus, id_)
        return
    props = sorted((bus / "proposals").glob("*.json"))
    props = [p for p in props if p.name.count(".") == 1]  # id.json only
    print(
        json.dumps(
            {
                "ok": True,
                "open_proposals": [p.stem for p in props],
                "decisions": [p.stem for p in sorted((bus / "decisions").glob("*.json"))],
            }
        )
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["propose", "plan", "verify", "status"])
    ap.add_argument("--bus", required=True)
    ap.add_argument("--repo", default=str(Path.home() / "dev" / "pumapay"))
    ap.add_argument("--id")
    ap.add_argument("--title", default="")
    ap.add_argument("--paths", default="")
    ap.add_argument("--question", default="ACK this proposal?")
    args = ap.parse_args()
    bus = Path(os.path.expanduser(args.bus))
    bus.mkdir(parents=True, exist_ok=True)
    (bus / "proposals").mkdir(exist_ok=True)
    (bus / "decisions").mkdir(exist_ok=True)

    if args.cmd == "propose":
        assert args.id and args.title
        paths = [p.strip() for p in args.paths.split(",") if p.strip()]
        propose(bus, args.repo, args.id, args.title, paths, args.question)
    elif args.cmd == "plan":
        assert args.id
        plan(bus, args.id)
    elif args.cmd == "verify":
        assert args.id
        verify(bus, args.id)
    else:
        status(bus, args.id)


if __name__ == "__main__":
    main()
