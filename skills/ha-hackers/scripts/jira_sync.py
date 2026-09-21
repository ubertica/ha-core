#!/usr/bin/env python3
"""Push VERIFY.json findings to PumaPay Jira. Fail-open (never fail verify).

No loot: redact emails/CBU/JWT/UUIDs. No invented GO. Dedupe by ha-fp-* label.
HOLD-prod on every issue. Skip if secrets missing or HA_JIRA_DISABLE=1.
"""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

SECRETS = Path.home() / ".grok/hard-allow/secrets/atlassian-org.env"
UUID_RE = re.compile(
    r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
    re.I,
)
EMAIL_RE = re.compile(r"[A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,}", re.I)
JWT_RE = re.compile(r"eyJ[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+")
CBU_RE = re.compile(r"\b\d{22}\b")
HEX_FN = re.compile(r"[0-9a-f]{16,}", re.I)


def load_env(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    if not path.is_file():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k.strip()] = v.strip().strip('"')
    return out


def redact(s: str) -> str:
    s = s or ""
    s = JWT_RE.sub("[JWT]", s)
    s = EMAIL_RE.sub("[email]", s)
    s = CBU_RE.sub("[CBU]", s)
    s = UUID_RE.sub("{id}", s)
    s = HEX_FN.sub("{id}", s)
    return s[:1200]


def norm_path(p: str) -> str:
    p = (p or "").split("?")[0].strip()
    p = UUID_RE.sub("{id}", p)
    p = HEX_FN.sub("{id}", p)
    if p.startswith("http"):
        try:
            from urllib.parse import urlparse

            p = urlparse(p).path or p
        except Exception:
            pass
    return p.lower().rstrip("/") or "/"


def fp_label(path: str, title: str) -> str:
    raw = f"{norm_path(path)}|{redact(title).lower()[:80]}"
    h = hashlib.sha1(raw.encode()).hexdigest()[:12]
    return f"ha-fp-{h}"


def route(path: str, title: str) -> tuple[str, str]:
    blob = f"{path} {title}".lower()
    if any(x in blob for x in ("webhook", "prize", "mercadopago", "cashin", "ipn", "callback")):
        return "PPAY", "PPAY-4"
    if any(x in blob for x in ("payment", "wallet", "bola", "supreme", "/user/", "bookmaker")):
        return "PPAY", "PPAY-3"
    if any(x in blob for x in ("s3", "voucher", "otp", "/docs", "openapi")):
        return "PPAY", "PPAY-2"
    return "PPITS", "PPITS-4"


def adf(text: str) -> dict:
    paras = []
    for block in text.split("\n\n"):
        paras.append({"type": "paragraph", "content": [{"type": "text", "text": block[:4000]}]})
    return {"type": "doc", "version": 1, "content": paras or [{"type": "paragraph", "content": []}]}


def adf_expand(title: str, body: str) -> dict:
    """Native Jira click-to-open. Comments cannot host custom buttons."""
    paras = [
        {"type": "paragraph", "content": [{"type": "text", "text": b[:4000]}]}
        for b in (body or "").split("\n\n")
        if b.strip()
    ]
    return {
        "type": "expand",
        "attrs": {"title": title[:200] or "▶ Ampliar explicación en lenguaje simple"},
        "content": paras or [{"type": "paragraph", "content": [{"type": "text", "text": "—"}]}],
    }


def adf_with_plain(tech: str, simple_title: str, simple_body: str) -> dict:
    doc = adf(tech)
    doc["content"].append(adf_expand(f"▶ Ampliar explicación en lenguaje simple — {simple_title}", simple_body))
    return doc


class Jira:
    def __init__(self, site: str, email: str, token: str):
        self.site = site.rstrip("/")
        import base64

        self.auth = "Basic " + base64.b64encode(f"{email}:{token}".encode()).decode()

    def req(self, method: str, path: str, payload=None):
        url = self.site + path
        data = json.dumps(payload).encode() if payload is not None else None
        headers = {
            "Authorization": self.auth,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        r = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(r, timeout=30) as resp:
                raw = resp.read().decode()
                return resp.status, json.loads(raw) if raw else None
        except urllib.error.HTTPError as e:
            b = e.read().decode()
            try:
                j = json.loads(b)
            except Exception:
                j = b[:600]
            return e.code, j

    def find_fp(self, label: str, path: str) -> str | None:
        jql = f'project in (PPAY, PPITS, PPSUP, PPAM) AND labels = "{label}"'
        st, body = self.req("POST", "/rest/api/3/search/jql", {"jql": jql, "maxResults": 5, "fields": ["summary"]})
        if st in (200, 201) and isinstance(body, dict):
            issues = body.get("issues") or []
            if issues:
                return issues[0].get("key")
        # fallback GET (older)
        from urllib.parse import quote

        st, body = self.req("GET", f"/rest/api/3/search?jql={quote(jql)}&maxResults=5")
        if st == 200 and isinstance(body, dict):
            issues = body.get("issues") or []
            if issues:
                return issues[0].get("key")
        np = norm_path(path)
        if len(np) >= 16:
            jql2 = f'project in (PPAY, PPITS) AND summary ~ "{np[:60]}"'
            st, body = self.req("POST", "/rest/api/3/search/jql", {"jql": jql2, "maxResults": 5, "fields": ["summary"]})
            if st == 200 and isinstance(body, dict):
                for iss in body.get("issues") or []:
                    sm = ((iss.get("fields") or {}).get("summary") or "")
                    if np.split("/")[-1][:20] in sm.lower() or np in sm.lower():
                        return iss.get("key")
        return None

    def comment(self, key: str, text: str) -> int:
        st, _ = self.req("POST", f"/rest/api/3/issue/{key}/comment", {"body": adf(text)})
        return st

    def create(self, project: str, parent: str, summary: str, body: str, labels: list[str]) -> tuple[int, str | None]:
        payload = {
            "fields": {
                "project": {"key": project},
                "summary": summary[:180],
                "description": adf(body),
                "issuetype": {"name": "Error"},
                "labels": labels[:20],
            }
        }
        if parent:
            payload["fields"]["parent"] = {"key": parent}
        st, res = self.req("POST", "/rest/api/3/issue", payload)
        if st in (400, 401) and parent:
            payload["fields"].pop("parent", None)
            st, res = self.req("POST", "/rest/api/3/issue", payload)
        key = res.get("key") if isinstance(res, dict) else None
        return st, key


def items_from_verify(rep: dict) -> list[dict]:
    out = []
    seen = set()
    for bucket in ("go", "confirmed"):
        for rec in rep.get(bucket) or []:
            if not isinstance(rec, dict):
                continue
            path = rec.get("path") or ""
            title = rec.get("title") or ""
            k = (norm_path(path), redact(title).lower()[:80])
            if k in seen:
                continue
            seen.add(k)
            out.append(rec)
    return out


def issue_body(rec: dict, pack: str, out_dir: str) -> str:
    return (
        f"ha-auto sync. pack={pack} label={rec.get('label')} sev={rec.get('sev')}\n\n"
        f"path: {redact(norm_path(rec.get('path') or ''))}\n\n"
        f"why: {redact(str(rec.get('why') or ''))}\n\n"
        f"jsonl_status: {rec.get('jsonl_status')}\n\n"
        f"source: {Path(str(rec.get('source') or '')).name}\n\n"
        f"out: {out_dir}\n\n"
        "HOLD-prod. No loot. No money-write. Disk VERIFY is SoT — no invented GO."
    )


ENGAGEMENTS = Path(os.environ.get("HA_JIRA_ENGAGEMENTS") or "/Users/c/dev/ha-live/proof/engagements")
BOT_ENV = Path(os.environ.get("HA_JIRA_BOT_ENV") or "/Users/c/dev/hardallow-bot/.env")
SITE_DEFAULT = "https://pumapay.atlassian.net"

# PumaPay Jira is Daniel's board. Never push other pentests (neo, mutual, HB).
_PUMA_OK = ("pumapay", "gplaygap", "gppay", "cobro-calimaco", "docs-gap", "calimaco", "gamesplay")
_PUMA_DENY = (
    "neoconsult",
    "mutualneo",
    "mosecs",
    "cashmutual",
    "mmalvici",
    "mandar_firmar",
    "generar_firma",
    "id_mutual",
    "blanqueo-password",
    "amv_saldos",
    "mutual san carlos",
    "/tiket",
    "wordfence",
)


def puma_jira_block_reason(out_dir: Path, recs: list) -> str | None:
    blob = (str(out_dir) + " " + out_dir.name).lower()
    for d in _PUMA_DENY:
        if d in blob:
            return f"deny-engagement:{d}"
    bits = []
    for r in recs or []:
        bits.append(str(r.get("path") or ""))
        bits.append(str(r.get("title") or ""))
        bits.append(str(r.get("why") or ""))
    text = " ".join(bits).lower()
    for d in _PUMA_DENY:
        if d in text:
            return f"deny-finding:{d}"
    if any(x in blob.lower() for x in _PUMA_OK):
        return None
    if any(x in text for x in _PUMA_OK):
        return None
    return "deny-unknown-engagement-not-puma"


def list_engagements(limit: int = 50) -> list[dict]:
    rows: list[dict] = []
    if not ENGAGEMENTS.is_dir():
        return rows
    for d in ENGAGEMENTS.iterdir():
        if not d.is_dir() or d.name.startswith("."):
            continue
        v = d / ".bus" / "VERIFY.json"
        j = d / ".bus" / "JIRA-SYNC.json"
        if not v.is_file():
            continue
        rows.append(
            {
                "name": d.name,
                "out": str(d),
                "mtime": int(v.stat().st_mtime),
                "has_jira": j.is_file(),
            }
        )
    rows.sort(key=lambda r: r["mtime"], reverse=True)
    return rows[: max(1, limit)]


def resolve_out(args) -> Path | None:
    if args.latest:
        rows = list_engagements(1)
        return Path(rows[0]["out"]) if rows else None
    if args.out:
        p = Path(args.out).expanduser()
        if p.is_dir():
            return p
        named = ENGAGEMENTS / args.out
        if named.is_dir():
            return named
        return p
    rows = list_engagements(1)
    return Path(rows[0]["out"]) if rows else None


def findings_sha(recs: list[dict]) -> str:
    blob = json.dumps(
        [
            {
                "p": norm_path(r.get("path") or ""),
                "t": redact(r.get("title") or "").lower()[:80],
                "s": r.get("sev"),
                "l": r.get("label"),
            }
            for r in recs
        ],
        sort_keys=True,
    )
    return hashlib.sha1(blob.encode()).hexdigest()[:16]


def read_json(path: Path) -> dict:
    if not path.is_file():
        return {}
    try:
        j = json.loads(path.read_text(encoding="utf-8"))
        return j if isinstance(j, dict) else {}
    except Exception:
        return {}


def summary_payload(result: dict, out_dir: Path) -> dict:
    return {
        "ok": result.get("ok", True),
        "skipped": result.get("skipped"),
        "dry": bool(result.get("dry")),
        "n": result.get("n", 0),
        "engagement": out_dir.name,
        "out": str(out_dir),
        "created": len(result.get("created") or []),
        "commented": len(result.get("commented") or []),
        "errors": len(result.get("errors") or []),
        "keys_created": [x.get("key") for x in (result.get("created") or []) if x.get("key")],
        "keys_commented": [x.get("key") for x in (result.get("commented") or []) if x.get("key")],
        "verify_sha": result.get("verify_sha"),
        "report": str(out_dir / ".bus" / "JIRA-SYNC.json"),
    }


def notify_tg(text: str) -> None:
    env = load_env(BOT_ENV)
    token = env.get("TELEGRAM_BOT_TOKEN")
    chat = env.get("PUMA_SECURITY_CHAT_ID") or "-5421027054"
    if not token or not text:
        return
    payload = json.dumps(
        {"chat_id": chat, "text": text[:3500], "disable_web_page_preview": True}
    ).encode()
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        urllib.request.urlopen(req, timeout=20).read()
    except Exception:
        pass


def format_notify(out_dir: Path, result: dict) -> str:
    created = [x.get("key") for x in (result.get("created") or []) if x.get("key")]
    if not created:
        return ""
    site = SITE_DEFAULT
    lines = [
        "HARD ALLOW: executing.",
        f"Jira auto · {out_dir.name}",
        f"tickets nuevos: {len(created)} (nadie lo pidió — salió del pentest/auditoría)",
    ]
    for k in created[:12]:
        lines.append(f"{k} {site}/browse/{k}")
    lines.append("HOLD-prod. No toca el sistema live.")
    return "\n".join(lines)


def sync_one(out_dir: Path, *, dry: bool = False, force: bool = False, notify: bool = False) -> dict:
    if os.environ.get("HA_JIRA_DISABLE") == "1":
        return {"ok": True, "skipped": "HA_JIRA_DISABLE", "created": [], "commented": [], "errors": []}
    bus = out_dir / ".bus"
    bus.mkdir(parents=True, exist_ok=True)
    verify = bus / "VERIFY.json"
    if not verify.is_file():
        return {"ok": False, "error": "no VERIFY.json", "out": str(out_dir), "created": [], "commented": [], "errors": []}
    try:
        rep = json.loads(verify.read_text(encoding="utf-8"))
    except Exception:
        return {"ok": False, "error": "bad VERIFY.json", "out": str(out_dir), "created": [], "commented": [], "errors": []}
    if not isinstance(rep, dict):
        return {"ok": False, "error": "VERIFY not object", "created": [], "commented": [], "errors": []}
    pack = str(rep.get("pack") or "ha")
    recs = items_from_verify(rep)
    blocked = puma_jira_block_reason(out_dir, recs)
    if blocked:
        stamp = {
            "ok": True,
            "skipped": blocked,
            "n": len(recs),
            "created": [],
            "commented": [],
            "errors": [],
            "engagement": out_dir.name,
        }
        (bus / "JIRA-SYNC.json").write_text(
            json.dumps({**stamp, "auto": True}, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        return stamp
    sha = findings_sha(recs)
    prev = read_json(bus / "JIRA-SYNC.json")
    if not recs and not force and not dry:
        stamp = {
            "ok": True,
            "skipped": "empty",
            "verify_sha": sha,
            "n": 0,
            "created": [],
            "commented": [],
            "errors": [],
            "engagement": out_dir.name,
        }
        if prev.get("verify_sha") != sha:
            (bus / "JIRA-SYNC.json").write_text(
                json.dumps({**stamp, "auto": True}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
            )
        return stamp
    if not force and not dry and prev.get("ok") and not prev.get("dry"):
        if prev.get("verify_sha") == sha and not prev.get("errors"):
            return {
                "ok": True,
                "skipped": "unchanged",
                "verify_sha": sha,
                "n": len(recs),
                "created": [],
                "commented": [],
                "errors": [],
                "engagement": out_dir.name,
            }
        if prev.get("verify_sha") in (None, ""):
            prev["verify_sha"] = sha
            prev["adopted"] = True
            (bus / "JIRA-SYNC.json").write_text(
                json.dumps(prev, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
            )
            return {
                "ok": True,
                "skipped": "adopted",
                "verify_sha": sha,
                "n": len(recs),
                "created": [],
                "commented": [],
                "errors": [],
                "engagement": out_dir.name,
            }

    env = load_env(SECRETS)
    email = env.get("ATLASSIAN_EMAIL")
    token = env.get("HARDALLOW_ATLASSIAN_API_TOKEN")
    site = env.get("ATLASSIAN_SITE") or SITE_DEFAULT
    result = {
        "ok": True,
        "dry": dry,
        "n": len(recs),
        "verify_sha": sha,
        "created": [],
        "commented": [],
        "errors": [],
        "auto": True,
    }
    if dry or not (email and token):
        for rec in recs:
            proj, parent = route(rec.get("path") or "", rec.get("title") or "")
            result["created"].append(
                {
                    "would": "create-or-comment",
                    "fp": fp_label(rec.get("path") or "", rec.get("title") or ""),
                    "project": proj,
                    "parent": parent,
                    "title": redact(rec.get("title") or "")[:80],
                    "path": norm_path(rec.get("path") or ""),
                }
            )
        if not (email and token):
            result["skipped"] = "no atlassian secrets"
        dest = bus / ("JIRA-SYNC.dry.json" if dry else "JIRA-SYNC.json")
        dest.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return result

    jira = Jira(site, email, token)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    for rec in recs:
        path = rec.get("path") or ""
        title = rec.get("title") or "finding"
        lab = fp_label(path, title)
        proj, parent = route(path, title)
        summary = f"[{rec.get('sev')}] {redact(title)}"
        try:
            existing = jira.find_fp(lab, path)
            if existing:
                st = jira.comment(
                    existing,
                    f"ha-auto {now} pack={pack} label={rec.get('label')} jsonl={rec.get('jsonl_status')} fp={lab}",
                )
                result["commented"].append({"key": existing, "comment": st, "fp": lab})
                continue
            labels = [
                lab,
                "ha-auto",
                "from-verify",
                "HOLD-prod",
                f"pack-{pack[:20]}",
                f"sev-{str(rec.get('sev') or 'info')[:12]}",
            ]
            st, key = jira.create(proj, parent, summary, issue_body(rec, pack, str(out_dir)), labels)
            if st in (200, 201) and key:
                result["created"].append({"key": key, "fp": lab, "project": proj})
            else:
                result["errors"].append({"fp": lab, "status": st, "path": norm_path(path)})
        except Exception as e:
            result["errors"].append({"fp": lab, "error": type(e).__name__})
    (bus / "JIRA-SYNC.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if notify:
        msg = format_notify(out_dir, result)
        if msg:
            notify_tg(msg)
    return result


def locked_sync(out_dir: Path, **kwargs) -> dict:
    bus = out_dir / ".bus"
    bus.mkdir(parents=True, exist_ok=True)
    lockp = bus / "JIRA-SYNC.lock"
    with open(lockp, "a", encoding="utf-8") as fh:
        try:
            fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return {"ok": True, "skipped": "locked", "created": [], "commented": [], "errors": [], "engagement": out_dir.name}
        return sync_one(out_dir, **kwargs)


def watch_loop(interval: int, notify: bool) -> int:
    print(json.dumps({"ok": True, "watch": True, "interval": interval, "root": str(ENGAGEMENTS)}), flush=True)
    while True:
        if os.environ.get("HA_JIRA_DISABLE") == "1":
            time.sleep(max(5, interval))
            continue
        for row in list_engagements(50):
            out = Path(row["out"])
            try:
                r = locked_sync(out, dry=False, force=False, notify=notify)
            except Exception as e:
                r = {"ok": False, "error": type(e).__name__, "engagement": out.name, "created": [], "commented": [], "errors": []}
            if r.get("skipped") in ("unchanged", "locked", "HA_JIRA_DISABLE", "adopted", "empty"):
                continue
            print(json.dumps(summary_payload(r, out), ensure_ascii=False), flush=True)
        time.sleep(max(5, interval))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="", help="engagement OUT dir or name under engagements/")
    ap.add_argument("--latest", action="store_true", help="newest engagement with VERIFY.json")
    ap.add_argument("--list", action="store_true", help="list engagements with VERIFY.json")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true", help="ignore unchanged sha")
    ap.add_argument("--notify", action="store_true", help="Telegram Puma Security on new tickets")
    ap.add_argument("--watch", action="store_true", help="daemon: VERIFY.json → Jira, no ask")
    ap.add_argument("--interval", type=int, default=20)
    args = ap.parse_args()
    if args.list:
        print(json.dumps({"ok": True, "engagements": list_engagements()}, ensure_ascii=False))
        return 0
    if args.watch:
        return watch_loop(args.interval, notify=True)
    if os.environ.get("HA_JIRA_DISABLE") == "1":
        print(json.dumps({"ok": True, "skipped": "HA_JIRA_DISABLE"}))
        return 0
    out_dir = resolve_out(args)
    if not out_dir:
        print(json.dumps({"ok": False, "error": "no engagement with VERIFY.json"}))
        return 0
    result = locked_sync(out_dir, dry=args.dry_run, force=args.force, notify=args.notify)
    print(json.dumps(summary_payload(result, out_dir), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
