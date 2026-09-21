#!/usr/bin/env python3
"""Deterministic OpenAPI op bucketing for ha-docs-entry. No LLM."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

HTTP = ("get", "post", "put", "patch", "delete", "head", "options", "trace")

# first match wins (see METHODOLOGY.md)
RULES: list[tuple[str, re.Pattern[str]]] = [
    ("money_write", re.compile(r"deposit|withdraw|transfer|payout|add-balance|force-approve|\bcredit\b|\bdebit\b", re.I)),
    ("webhook", re.compile(r"webhook|/hook(?:/|$)", re.I)),
    ("payment_callback", re.compile(r"callback|\bipn\b|notify|cashin|/integrations/payments", re.I)),
    ("auth_entry", re.compile(r"login|register|otp|remotelogin|remote-login|passkey|password-reset|refresh-token|validatelogin", re.I)),
    ("pam_bot", re.compile(r"/pam|/bot\b|telegram", re.I)),
    ("payment_public", re.compile(r"payment-link|/public/|fintech/customers/public", re.I)),
    ("admin", re.compile(r"/admin|superuser|filesystem|finance-keys", re.I)),
    ("health", re.compile(r"/health|/metrics", re.I)),
    ("docs", re.compile(r"/docs|/swagger|openapi\.json|/api-docs", re.I)),
    ("cms_public", re.compile(r"/cms", re.I)),
    ("visor_public", re.compile(r"visor", re.I)),
    ("jwt_likely", re.compile(r"/wallet|/backoffice|/agents", re.I)),
]


def bucket_path(path: str) -> str:
    for name, rx in RULES:
        if rx.search(path):
            return name
    return "other"


def load_spec(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8", errors="replace")
    if raw.lstrip().startswith("{"):
        return json.loads(raw)
    # Fastify /docs sometimes wraps JSON; try last JSON object
    i = raw.find("{")
    if i >= 0:
        return json.loads(raw[i:])
    raise SystemExit(f"not JSON: {path}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    spec_path = Path(args.spec)
    spec = load_spec(spec_path)
    paths = spec.get("paths") or {}
    schemes = ((spec.get("components") or {}).get("securitySchemes")) or spec.get("securityDefinitions") or {}
    groups: dict[str, list[dict]] = {}
    total_ops = 0
    for pth, item in paths.items():
        if not isinstance(item, dict):
            continue
        methods = [m.upper() for m in HTTP if m in item]
        if not methods:
            continue
        b = bucket_path(pth)
        rec = {
            "path": pth,
            "methods": methods,
            "bucket": b,
            "summaries": {m: (item.get(m.lower()) or {}).get("summary") or "" for m in methods},
        }
        groups.setdefault(b, []).append(rec)
        total_ops += len(methods)
    out = {
        "source": str(spec_path),
        "title": (spec.get("info") or {}).get("title"),
        "version": (spec.get("info") or {}).get("version"),
        "servers": spec.get("servers") or [],
        "securitySchemes": list(schemes) if isinstance(schemes, dict) else schemes,
        "total_paths": len(paths),
        "total_ops": total_ops,
        "bucket_counts": {k: len(v) for k, v in sorted(groups.items())},
        "groups": groups,
    }
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "out": str(out_path), "paths": len(paths), "ops": total_ops, "buckets": out["bucket_counts"]}))


if __name__ == "__main__":
    main()
