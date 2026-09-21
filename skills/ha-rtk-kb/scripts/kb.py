#!/usr/bin/env python3
"""Shared KB for ha-redteam + ha-blackhat.

Lanes/OUT stay separate. Knowledge is one SoT.
Redact JWT/PII/CBU. Never store loot blobs. Fail-open on feeds.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import time
import urllib.request
from pathlib import Path

KB = Path(os.environ.get("HA_RTK_KB") or (Path.home() / ".grok" / "ha-rtk-kb")).expanduser()
KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
JWT_RE = re.compile(r"eyJ[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+")
EMAIL_RE = re.compile(r"[A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,}", re.I)
CBU_RE = re.compile(r"\b\d{22}\b")
UUID_RE = re.compile(
    r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", re.I
)
HA_RE = re.compile(r"ha_[A-Za-z0-9_\-]{8,}")
BEARER_RE = re.compile(r"(?i)(bearer\s+)[A-Za-z0-9._\-]{12,}")
KEY_RE = re.compile(r"(?i)(api[_-]?key|secret|password|token)\s*[:=]\s*\S+")
DROP_KEYS = {
    "jwt",
    "token",
    "password",
    "secret",
    "loot",
    "cookie",
    "cookies",
    "authorization",
    "cbu",
    "api_key",
    "apikey",
    "session",
    "dump",
    "raw",
    "payload",
    "body",
    "har",
}
SKIP_PARTS = {"loot", "dump", "hack", "drain", "wallet-dump"}
INGEST_NAMES = {"FINDINGS.jsonl", "GO.jsonl"}
TECH = (
    "fastify",
    "express",
    "nginx",
    "jwt",
    "nuxt",
    "next.js",
    "redis",
    "postgres",
    "openapi",
    "swagger",
    "wordpress",
    "laravel",
    "node.js",
    "graphql",
    "webhook",
    "cloudfront",
    "fastify",
)


def redact(s: str) -> str:
    s = s or ""
    s = JWT_RE.sub("[JWT]", s)
    s = HA_RE.sub("[HA]", s)
    s = BEARER_RE.sub(r"\1[redacted]", s)
    s = KEY_RE.sub(r"\1=[redacted]", s)
    s = EMAIL_RE.sub("[email]", s)
    s = CBU_RE.sub("[CBU]", s)
    s = UUID_RE.sub("{id}", s)
    return s[:1200]


def now() -> str:
    return time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime())


def sha16(s: str) -> str:
    return hashlib.sha256((s or "").encode("utf-8", errors="replace")).hexdigest()[:16]


def ensure_kb() -> None:
    for sub in ("cache", "intel", "memory", "index", "learn", "nodes", "runs"):
        (KB / sub).mkdir(parents=True, exist_ok=True)


def append_jsonl(path: Path, rec: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def proxy_opener(proxy: str | None):
    if not proxy:
        return urllib.request.build_opener()
    return urllib.request.build_opener(urllib.request.ProxyHandler({"http": proxy, "https": proxy}))


def fetch_json(url: str, proxy: str | None, timeout: int = 25):
    req = urllib.request.Request(url, headers={"User-Agent": "ha-rtk-kb"})
    with proxy_opener(proxy).open(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", errors="replace"))


def keywords(out: Path) -> list[str]:
    blob = ""
    for rel in (
        "entry/ENTRY.md",
        "probe/PROBE.md",
        "docs/FINDINGS.md",
        "docs/AUDIT.md",
        "SUMMARY.md",
    ):
        p = out / rel
        if p.is_file():
            blob += " " + p.read_text(encoding="utf-8", errors="replace")[:30000]
    for p in out.rglob("FINDINGS.jsonl"):
        if any(part in SKIP_PARTS for part in p.parts):
            continue
        blob += " " + p.read_text(encoding="utf-8", errors="replace")[:20000]
    keys: list[str] = []
    low = blob.lower()
    for tok in TECH:
        if tok.lower() in low and tok not in keys:
            keys.append(tok)
    return keys[:12]


def _key_hit(hay: str, k: str) -> bool:
    k = k.lower()
    if len(k) <= 4:
        return re.search(r"(^|[^a-z0-9])" + re.escape(k) + r"([^a-z0-9]|$)", hay) is not None
    return k in hay


def match_kev(kev: dict, keys: list[str]) -> list[dict]:
    vulns = kev.get("vulnerabilities") or []
    hits: list[dict] = []
    kl = [k.lower() for k in keys]
    if not kl:
        return hits
    for v in vulns:
        hay = " ".join(
            str(v.get(x) or "")
            for x in ("vendorProject", "product", "vulnerabilityName", "shortDescription", "cveID")
        ).lower()
        if any(_key_hit(hay, k) for k in kl):
            hits.append(
                {
                    "cve": v.get("cveID"),
                    "name": v.get("vulnerabilityName"),
                    "product": v.get("product"),
                    "vendor": v.get("vendorProject"),
                }
            )
        if len(hits) >= 15:
            break
    return hits


def load_kev(proxy: str | None) -> dict:
    ensure_kb()
    cache = KB / "cache" / "kev.json"
    try:
        kev = fetch_json(KEV_URL, proxy)
        cache.write_text(json.dumps(kev), encoding="utf-8")
        return kev
    except Exception:
        if cache.is_file():
            return json.loads(cache.read_text(encoding="utf-8"))
        return {"vulnerabilities": []}


def sanitize_finding(rec: dict) -> dict:
    out: dict = {}
    for k, v in rec.items():
        if str(k).lower() in DROP_KEYS:
            continue
        if k in ("path", "title", "sev", "label", "cwe", "host", "source", "why"):
            out[k] = redact(str(v))[:240] if v is not None else None
        elif isinstance(v, (int, float, bool)) or v is None:
            if k in ("go", "confirmed"):
                out[k] = v
    return out


def existing_fps(path: Path) -> set[str]:
    seen: set[str] = set()
    if not path.is_file():
        return seen
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        fp = rec.get("fp")
        if fp:
            seen.add(str(fp))
    return seen


def cmd_intel(out: Path, pack: str, proxy: str) -> dict:
    keys = keywords(out)
    err = None
    hits: list[dict] = []
    try:
        kev = load_kev(proxy or None)
        hits = match_kev(kev, keys) if keys else []
    except Exception as e:
        err = type(e).__name__
    rec = {
        "ts": now(),
        "pack": pack,
        "out": str(out),
        "keys": keys,
        "kev_hits": hits,
        "error": err,
        "source": "cisa-kev",
        "kb": str(KB),
    }
    append_jsonl(KB / "INTEL-HITS.jsonl", rec)
    append_jsonl(KB / "intel" / "HITS.jsonl", rec)
    intel_dir = out / "intel"
    intel_dir.mkdir(parents=True, exist_ok=True)
    lines = [
        "# INTEL (shared ha-rtk-kb)",
        "",
        f"pack: `{pack}`",
        f"kb: `{KB}`",
        f"keys: {keys}",
        f"kev_hits: {len(hits)}",
        f"error: {err}",
        "",
        "Shared cache. Cite feeds. No exploit payloads in the KB. Loot stays in engagement OUT.",
        "",
    ]
    for h in hits:
        lines.append(f"- `{h.get('cve')}` {h.get('vendor')}/{h.get('product')} — {h.get('name')}")
    (intel_dir / "INTEL.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (out / ".bus").mkdir(parents=True, exist_ok=True)
    (out / ".bus" / "READY.intel").write_text("ok\n", encoding="utf-8")
    (out / ".bus" / "INTEL.json").write_text(json.dumps(rec, indent=2) + "\n")
    return rec


def cmd_memory(out: Path, pack: str, op: str, summary: str) -> dict:
    rec = {
        "ts": now(),
        "op": op,
        "pack": pack,
        "summary": redact(summary or f"{pack} {op}"),
        "out": str(out),
        "nodes": f"nodes_search q=TARGET; nodes_commit_turn source=grok tags=[ha-rtk-kb,{pack}]",
    }
    append_jsonl(KB / "MEMORY.jsonl", rec)
    append_jsonl(KB / "memory" / "MEMORY.jsonl", rec)
    (out / ".bus").mkdir(parents=True, exist_ok=True)
    append_jsonl(out / ".bus" / "MEMORY.jsonl", rec)
    mem = out / "memory"
    mem.mkdir(parents=True, exist_ok=True)
    (mem / "MEMORY.md").write_text(
        f"# MEMORY\n\nShared: `{KB}/MEMORY.jsonl`\nPack: `{pack}`\nOp: `{op}`\n\n"
        "Start: nodes_search. End: nodes_commit_turn tags=ha-rtk-kb. No secrets in KB.\n"
        "Civil pack never reads loot files — only this index.\n",
        encoding="utf-8",
    )
    (out / ".bus" / "READY.memory").write_text("ok\n", encoding="utf-8")
    return {"ok": True, "kb": str(KB / "MEMORY.jsonl"), "pack": pack, "op": op}


def cmd_ingest(out: Path, pack: str) -> dict:
    idx_path = KB / "FINDINGS-INDEX.jsonl"
    seen = existing_fps(idx_path)
    n = 0
    skipped = 0
    for p in out.rglob("*.jsonl"):
        if p.name not in INGEST_NAMES:
            continue
        if any(part in SKIP_PARTS for part in p.parts):
            skipped += 1
            continue
        for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(rec, dict):
                continue
            fp = sha16(line)
            if fp in seen:
                continue
            seen.add(fp)
            idx = {
                "ts": now(),
                "pack": pack,
                "fp": fp,
                "file": p.name,
                "rel": redact(str(p.relative_to(out))),
                **sanitize_finding(rec),
            }
            append_jsonl(idx_path, idx)
            append_jsonl(KB / "index" / "FINDINGS-INDEX.jsonl", idx)
            n += 1
    rec = {"ok": True, "ingested": n, "skipped_loot_files": skipped, "kb": str(idx_path), "pack": pack}
    append_jsonl(KB / "runs" / "INGEST.jsonl", rec)
    return rec


def cmd_query(q: str, limit: int) -> dict:
    qn = (q or "").lower()
    hits: list[dict] = []
    files = (
        "MEMORY.jsonl",
        "INTEL-HITS.jsonl",
        "FINDINGS-INDEX.jsonl",
        "LEARN.jsonl",
        "memory/MEMORY.jsonl",
        "intel/HITS.jsonl",
        "index/FINDINGS-INDEX.jsonl",
        "learn/LEARN.jsonl",
    )
    for name in files:
        p = KB / name
        if not p.is_file():
            continue
        for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
            if qn and qn not in line.lower():
                continue
            hits.append({"file": name, "line": redact(line)[:400]})
            if len(hits) >= limit:
                break
        if len(hits) >= limit:
            break
    return {"ok": True, "q": q, "n": len(hits), "hits": hits, "kb": str(KB)}


def cmd_learn(pack: str, note: str) -> dict:
    rec = {"ts": now(), "pack": pack, "note": redact(note)}
    append_jsonl(KB / "LEARN.jsonl", rec)
    append_jsonl(KB / "learn" / "LEARN.jsonl", rec)
    return rec


def _count_lines(path: Path) -> int:
    if not path.is_file():
        return 0
    return sum(1 for line in path.read_text(encoding="utf-8", errors="replace").splitlines() if line.strip())


def cmd_status() -> dict:
    ensure_kb()
    packs: dict[str, int] = {}
    idx = KB / "FINDINGS-INDEX.jsonl"
    if idx.is_file():
        for line in idx.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            pk = rec.get("pack") or "?"
            packs[pk] = packs.get(pk, 0) + 1
    return {
        "ok": True,
        "kb": str(KB),
        "counts": {
            "FINDINGS-INDEX": _count_lines(idx),
            "MEMORY": _count_lines(KB / "MEMORY.jsonl"),
            "INTEL-HITS": _count_lines(KB / "INTEL-HITS.jsonl"),
            "LEARN": _count_lines(KB / "LEARN.jsonl"),
            "kev_cache": (KB / "cache" / "kev.json").is_file(),
        },
        "by_pack": packs,
        "split": {
            "shared": "KEV cache, MEMORY, LEARN, FINDINGS-INDEX (redacted fps)",
            "per_pack": "full FINDINGS / loot only in that pack OUT",
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["intel", "memory", "ingest", "query", "learn", "status"])
    ap.add_argument("--out", default="")
    ap.add_argument("--pack", default="ha-redteam")
    ap.add_argument("--proxy", default="")
    ap.add_argument("--op", default="note")
    ap.add_argument("--summary", default="")
    ap.add_argument("--q", default="")
    ap.add_argument("--note", default="")
    ap.add_argument("--limit", type=int, default=20)
    args = ap.parse_args()
    ensure_kb()
    proxy = args.proxy or os.environ.get("HA_PROXY") or ""
    out = Path(args.out).expanduser().resolve() if args.out else Path.cwd()
    if not proxy:
        pf = out / ".bus" / "PROXY"
        if pf.is_file():
            proxy = pf.read_text(encoding="utf-8").strip()
    if args.cmd == "intel":
        rec = cmd_intel(out, args.pack, proxy)
    elif args.cmd == "memory":
        rec = cmd_memory(out, args.pack, args.op, args.summary)
    elif args.cmd == "ingest":
        rec = cmd_ingest(out, args.pack)
    elif args.cmd == "learn":
        rec = cmd_learn(args.pack, args.note)
    elif args.cmd == "status":
        rec = cmd_status()
    else:
        rec = cmd_query(args.q, args.limit)
    print(json.dumps(rec))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
