#!/usr/bin/env python3
"""Disk evidence gate. Agents' confirmed_count is untrusted. Fail closed.

Only `*-findings.md` (never ENTRY.md / WEBHOOK.md / FINDINGS.md / authz-entry.md).
Pack isolation: docs-entry does not ingest ha-hackers BOLA files, and vice versa.
Dedup by (sev, title, path).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

HEAD = re.compile(r"^## \[(critical|high|medium|low|info)\]\s+(.*)$", re.I | re.M)
ASSET = re.compile(r"(?im)^-\s*Asset:\s*(.+)$")
EVID = re.compile(r"(?im)^-\s*Evidence:\s*(.+)$")
REQ = re.compile(r"(?im)^-\s*Request:\s*(.+)$")
PATH_IN = re.compile(r"(https?://[^\s`]+|/[/A-Za-z0-9_{}.\-]+)")

SENSITIVE = re.compile(
    r"otpToken|password|secret|pbkdf2|pending|balance|cuit|foreign|"
    r"other-user|userid|email@|authorization|jwt|private.?key|cbu|"
    r"unsigned|no HMAC|no secret|ok\"?\s*:\s*true|\"ok\":true",
    re.I,
)
PUBLIC_OK = re.compile(r"status.:.ok|totalDocs.:0|health|expected-public", re.I)
GO_SEV = {"critical", "high"}
OK_STATUS = {200, 201, 202, 206}

SKIP_MD_NAMES = {
    "entry.md",
    "webhook.md",
    "findings.md",
    "summary.md",
    "negative.md",
    "lanes.md",
    "authz-entry.md",
    "methodology.md",
    "contract.md",
    "autonomy.md",
}


def load_jsonl(paths: list[Path]) -> list[dict]:
    rows: list[dict] = []
    for p in paths:
        if not p.is_file():
            continue
        for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows


def rec_path(o: dict) -> str:
    for k in ("spec_path", "url_path", "path", "url"):
        v = o.get(k)
        if isinstance(v, str) and v:
            return v
    return ""


def rec_status(o: dict) -> int | None:
    for k in ("status", "code", "http"):
        v = o.get(k)
        if isinstance(v, int):
            return v
        if isinstance(v, str) and v.isdigit():
            return int(v)
    return None


def rec_preview(o: dict) -> str:
    return str(o.get("preview") or o.get("body_preview") or o.get("body") or "")[:800]


def extract_path(text: str) -> str:
    urls = PATH_IN.findall(text or "")
    for u in urls:
        if u.startswith("http"):
            return urlparse(u).path or u
        if u.startswith("/"):
            return u.split("?")[0]
    return ""


def parse_findings(md: str, source: str) -> list[dict]:
    out: list[dict] = []
    matches = list(HEAD.finditer(md))
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(md)
        block = md[start:end]
        sev = m.group(1).lower()
        title = m.group(2).strip()
        am = ASSET.search(block)
        em = EVID.search(block)
        rm = REQ.search(block)
        asset = am.group(1).strip() if am else ""
        evid = em.group(1).strip() if em else ""
        req = rm.group(1).strip() if rm else ""
        out.append(
            {
                "sev": sev,
                "title": title,
                "asset": asset,
                "evidence": evid,
                "request": req,
                "path": extract_path(asset) or extract_path(req),
                "source": source,
                "block": block[:2000],
            }
        )
    return out


def _is_findings_md(p: Path) -> bool:
    name = p.name.lower()
    if name in SKIP_MD_NAMES:
        return False
    if not name.endswith("findings.md"):
        return False
    if name == "findings.md":
        return False
    return p.is_file() and p.stat().st_size > 40


def find_md(out: Path, pack: str) -> list[Path]:
    """Pack-isolated. Only *-findings.md."""
    found: list[Path] = []
    seen: set[Path] = set()

    def add(p: Path) -> None:
        try:
            rp = p.resolve()
        except OSError:
            return
        if rp in seen:
            return
        if _is_findings_md(p):
            found.append(p)
            seen.add(rp)

    if pack == "docs-entry":
        for root in (out / "docs-entry", out / "OUT" / "docs-entry"):
            if not root.is_dir():
                continue
            for p in sorted(root.glob("*findings.md")):
                add(p)
        return found

    for n in ("authz-findings.md", "exploit-findings.md"):
        add(out / n)
        add(out / "hack" / n)
    for p in out.glob("*findings.md"):
        if "docs-entry" in p.parts:
            continue
        add(p)
    return found


def find_jsonl(out: Path, pack: str) -> list[Path]:
    hits: list[Path] = []
    seen: set[Path] = set()

    def add(p: Path) -> None:
        try:
            rp = p.resolve()
        except OSError:
            return
        if rp in seen or not p.is_file():
            return
        hits.append(p)
        seen.add(rp)

    if pack == "docs-entry":
        for root in (out / "docs-entry", out / "OUT" / "docs-entry"):
            if not root.is_dir():
                continue
            for p in root.glob("*.jsonl"):
                if "probe" in p.name.lower():
                    add(p)
        return hits

    for n in ("authz-probes.jsonl", "hack/probes.jsonl"):
        add(out / n)
    for p in out.glob("*probes.jsonl"):
        if "docs-entry" in p.parts or "writes" in p.parts:
            continue
        add(p)
    return hits


def jsonl_hit(rows: list[dict], path: str) -> dict | None:
    if not path:
        return None
    path = path.split("?")[0]
    best = None
    for r in rows:
        rp = rec_path(r).split("?")[0]
        if not rp:
            continue
        if rp == path or rp.endswith(path) or path.endswith(rp):
            st = rec_status(r)
            if st in OK_STATUS:
                return r
            if best is None:
                best = r
    return best


def classify(f: dict, hit: dict | None) -> tuple[str, str]:
    """Return (label, why) label in confirmed|go|reject."""
    if not f["evidence"] and not f["request"]:
        return "reject", "no evidence/request lines"
    st = rec_status(hit) if hit else None
    prev = rec_preview(hit) if hit else ""
    blob = " ".join([f["evidence"], f["title"], f["block"], prev])
    if f["sev"] in {"info", "low"} and not SENSITIVE.search(blob):
        return "reject", "info/low without sensitive"
    if st is not None and st not in OK_STATUS and st not in {400, 500}:
        if "200" not in f["evidence"]:
            return "reject", f"jsonl status {st}"
    evid_has_200 = bool(re.search(r"\b200\b", f["evidence"])) or st in OK_STATUS
    if not evid_has_200 and st != 400:
        return "reject", "no 200/400 on disk"
    if PUBLIC_OK.search(blob) and not SENSITIVE.search(blob) and f["sev"] not in GO_SEV:
        return "reject", "expected-public"
    if f["sev"] in GO_SEV and evid_has_200 and SENSITIVE.search(blob):
        if re.search(r"credit not proven|not a login session|fake ids", blob, re.I):
            if re.search(r"webhook|otpToken|unsigned|no HMAC|no secret", blob, re.I):
                return "go", "high/crit 200 + unsigned/secret (credit unproven noted)"
            return "confirmed", "high/crit 200 but impact unproven"
        return "go", "high/crit 200 + sensitive"
    if f["sev"] in GO_SEV and evid_has_200:
        return "confirmed", "high/crit 200 without sensitive keyword"
    if evid_has_200 or st == 400:
        return "confirmed", "foothold"
    return "reject", "no disk match"


def dedup_key(f: dict) -> tuple[str, str, str]:
    return (f["sev"], f["title"].lower(), (f["path"] or "").split("?")[0])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--pack", choices=["docs-entry", "ha-hackers"], default="docs-entry")
    args = ap.parse_args()
    out = Path(args.out).expanduser().resolve()
    mds = find_md(out, args.pack)
    jsonls = find_jsonl(out, args.pack)
    rows = load_jsonl(jsonls)
    findings: list[dict] = []
    seen_keys: set[tuple[str, str, str]] = set()
    for md in mds:
        for f in parse_findings(md.read_text(encoding="utf-8", errors="replace"), str(md)):
            k = dedup_key(f)
            if k in seen_keys:
                continue
            seen_keys.add(k)
            findings.append(f)

    confirmed = []
    go = []
    rejected = []
    seen_go_paths: set[str] = set()
    for f in findings:
        hit = jsonl_hit(rows, f["path"])
        label, why = classify(f, hit)
        rec = {
            "sev": f["sev"],
            "title": f["title"],
            "path": f["path"],
            "source": f["source"],
            "label": label,
            "why": why,
            "jsonl_status": rec_status(hit) if hit else None,
        }
        if label == "go":
            pk = (f["path"] or "").split("?")[0]
            if pk and pk in seen_go_paths:
                rec["label"] = "confirmed"
                rec["why"] = "dup-path " + why
                confirmed.append(rec)
                continue
            if pk:
                seen_go_paths.add(pk)
            go.append(rec)
            confirmed.append(rec)
        elif label == "confirmed":
            confirmed.append(rec)
        else:
            rejected.append(rec)

    report = {
        "ok": True,
        "pack": args.pack,
        "out": str(out),
        "md_files": [str(p) for p in mds],
        "jsonl_files": [str(p) for p in jsonls],
        "jsonl_rows": len(rows),
        "parsed": len(findings),
        "confirmed_count": len(confirmed),
        "go_count": len(go),
        "confirmed": confirmed,
        "go": go,
        "rejected_count": len(rejected),
        "rejected": rejected[:40],
    }
    bus = out / ".bus"
    bus.mkdir(parents=True, exist_ok=True)
    (bus / "VERIFY.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    if args.pack == "docs-entry" and report["go_count"] == 0:
        neg = out / "docs-entry" / "NEGATIVE.md"
        neg.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            "# NEGATIVE — no verified GO",
            "",
            f"parsed={len(findings)} confirmed={len(confirmed)} go=0",
            "Exploit/lead not spawned. Evidence gate fail-closed.",
            "",
        ]
        for r in confirmed:
            lines.append(f"- confirmed [{r['sev']}] {r['title']} ({r['path']}) — {r['why']}")
        for r in rejected[:20]:
            lines.append(f"- reject [{r['sev']}] {r['title']} — {r['why']}")
        neg.write_text("\n".join(lines) + "\n", encoding="utf-8")
        report["negative"] = str(neg)
    print(
        json.dumps(
            {
                "ok": True,
                "confirmed_count": report["confirmed_count"],
                "go_count": report["go_count"],
                "parsed": report["parsed"],
                "report": str(bus / "VERIFY.json"),
            }
        )
    )
    if os.environ.get("HA_JIRA_DISABLE") != "1":
        sync = Path(__file__).resolve().parent / "jira_sync.py"
        if sync.is_file():
            try:
                subprocess.run(
                    [sys.executable, str(sync), "--out", str(out), "--notify"],
                    timeout=90,
                    check=False,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            except Exception:
                pass
    if os.environ.get("HA_DISCORD_DISABLE") != "1":
        ha_dc = Path.home() / ".grok/hard-allow/bin/ha-hardallow.mjs"
        if ha_dc.is_file():
            try:
                subprocess.run(
                    ["node", str(ha_dc), "verify", "--out", str(out)],
                    timeout=90,
                    check=False,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            except Exception:
                pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
