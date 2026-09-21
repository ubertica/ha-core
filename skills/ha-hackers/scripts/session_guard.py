#!/usr/bin/env python3
"""JWT TTL + SOCKS egress invariant. No live money.

Exit 0 ok, 2 token stale, 3 proxy down.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

DEFAULT_PROXY = os.environ.get("HA_PROXY", "socks5h://127.0.0.1:10808")


def b64url(s: str) -> bytes:
    pad = "=" * (-len(s) % 4)
    return base64.urlsafe_b64decode(s + pad)


def jwt_payload(tok: str) -> dict:
    parts = tok.split(".")
    if len(parts) < 2:
        return {}
    try:
        return json.loads(b64url(parts[1]))
    except Exception:
        return {}


def extract_jwt(obj) -> str:
    if isinstance(obj, str) and obj.count(".") >= 2:
        return obj.strip()
    if not isinstance(obj, dict):
        return ""
    for k in ("jwt", "token", "access_token", "accessToken"):
        v = obj.get(k)
        if isinstance(v, str) and v.count(".") >= 2:
            return v
    auth = obj.get("auth")
    if isinstance(auth, dict):
        t = extract_jwt(auth)
        if t:
            return t
        hdrs = auth.get("headers") or {}
        if isinstance(hdrs, dict):
            a = hdrs.get("authorization") or hdrs.get("Authorization") or ""
            if isinstance(a, str) and a.lower().startswith("bearer "):
                cand = a.split(" ", 1)[1].strip()
                if cand.count(".") >= 2 and cand != "JWT":
                    return cand
    return ""


def proxy_hostport(proxy: str) -> tuple[str, int]:
    u = urlparse(proxy)
    host = u.hostname or "127.0.0.1"
    port = u.port or 1080
    return host, port


def tcp_up(host: str, port: int, timeout: float = 2.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def chrome_osascript(origin: str) -> str:
    if not origin:
        return ""
    needle = origin.replace("https://", "").replace("http://", "")
    script = f'''
tell application "Google Chrome"
  if (count of windows) is 0 then return ""
  repeat with w in windows
    repeat with t in tabs of w
      set u to URL of t
      if u contains "{needle}" then
        set js to "(() => {{ try {{ const keys=['token','jwt','authToken','access_token','accessToken']; for (const k of keys) {{ const v=localStorage.getItem(k); if (v && v.split('.').length>=3) return v; }} for (let i=0;i<localStorage.length;i++) {{ const k=localStorage.key(i); const v=localStorage.getItem(k)||''; if (v.indexOf('eyJ')===0 && v.split('.').length>=3) return v; if (v.length>20) {{ try {{ const o=JSON.parse(v); const t=o.token||o.jwt||(o.auth&&o.auth.jwt)||''; if (t && t.split('.').length>=3) return t; }} catch(e) {{}} }} }} return ''; }} catch(e) {{ return ''; }} }})()"
        return execute t javascript js
      end if
    end repeat
  end repeat
end tell
return ""
'''
    try:
        r = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True,
            timeout=8,
        )
        tok = (r.stdout or "").strip().strip('"')
        if tok.count(".") >= 2:
            return tok
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return ""
    return ""


def chrome_cdp(origin: str) -> str:
    try:
        with urllib.request.urlopen("http://127.0.0.1:9222/json/list", timeout=1.5) as resp:
            json.loads(resp.read().decode())
    except Exception:
        return ""
    _ = origin
    return ""


def write_jwt(token_file: Path, jwt: str) -> None:
    data = {}
    if token_file.is_file():
        try:
            data = json.loads(token_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = {}
    if not isinstance(data, dict):
        data = {}
    data.setdefault("auth", {})
    if isinstance(data["auth"], dict):
        data["auth"]["jwt"] = jwt
        data["auth"]["jwtPayload"] = jwt_payload(jwt)
    data["jwt"] = jwt
    data["dumpedAt"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    token_file.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def resolve_token_file(args: argparse.Namespace) -> Path | None:
    if args.token_file:
        return Path(args.token_file).expanduser()
    if not args.out:
        return None
    out = Path(args.out).expanduser()
    for c in (
        out / "session.json",
        out / "docs-entry" / "obtained-token.json",
        out / "OUT" / "session.json",
    ):
        if c.is_file():
            return c
    return None


def probe_bearer(url: str, jwt: str, proxy: str) -> int | None:
    """HTTP status via curl+SOCKS. None if curl missing/failed."""
    cmd = [
        "curl",
        "-sS",
        "-o",
        "/dev/null",
        "-w",
        "%{http_code}",
        "--max-time",
        "15",
        "-x",
        proxy,
    ]
    if jwt:
        cmd.extend(["-H", f"Authorization: Bearer {jwt}"])
    cmd.append(url)
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return None
    code = (r.stdout or "").strip()
    if code.isdigit():
        return int(code)
    return None


def _stale_flag(out: str, on: bool) -> None:
    if not out:
        return
    p = Path(out).expanduser() / ".bus" / "TOKEN.stale"
    p.parent.mkdir(parents=True, exist_ok=True)
    if on:
        p.write_text("stale\n", encoding="utf-8")
    elif p.is_file():
        p.unlink()


def _emit(out: str, report: dict) -> None:
    if not out:
        return
    bus = Path(out).expanduser() / ".bus"
    bus.mkdir(parents=True, exist_ok=True)
    (bus / "EGRESS.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--token-file")
    ap.add_argument("--proxy", default=DEFAULT_PROXY)
    ap.add_argument("--need-token", action="store_true")
    ap.add_argument("--allow-direct", action="store_true")
    ap.add_argument("--origin", default="", help="SPA origin for Chrome localStorage refresh")
    ap.add_argument("--probe-url", default="")
    ap.add_argument("--out", default="")
    ap.add_argument("--skew", type=int, default=120, help="seconds before exp to treat stale")
    args = ap.parse_args()

    report: dict = {
        "ok": True,
        "proxy": args.proxy,
        "token_ok": True,
        "proxy_ok": True,
        "refreshed": False,
    }

    if args.proxy and not args.allow_direct:
        host, port = proxy_hostport(args.proxy)
        report["proxy_host"] = f"{host}:{port}"
        if not tcp_up(host, port):
            report.update({"ok": False, "proxy_ok": False, "error": "proxy_down"})
            _emit(args.out, report)
            print(json.dumps(report))
            return 3

    jwt = ""
    tf = resolve_token_file(args)
    if tf:
        report["token_file"] = str(tf)
        if tf.is_file():
            try:
                jwt = extract_jwt(json.loads(tf.read_text(encoding="utf-8")))
            except json.JSONDecodeError:
                jwt = ""
    pay = jwt_payload(jwt) if jwt else {}
    exp = int(pay.get("exp") or 0)
    now = int(time.time())
    report["exp"] = exp
    report["now"] = now
    stale = bool(jwt) and exp and exp < now + args.skew
    missing = args.need_token and not jwt
    if stale or missing:
        origin = args.origin or ""
        fresh = chrome_osascript(origin) if origin else ""
        if not fresh:
            fresh = chrome_cdp(origin) if origin else ""
        if fresh and fresh != jwt:
            if tf:
                write_jwt(tf, fresh)
            jwt = fresh
            pay = jwt_payload(jwt)
            exp = int(pay.get("exp") or 0)
            report["refreshed"] = True
            report["exp"] = exp
            stale = bool(exp) and exp < now + args.skew
        if args.need_token and (not jwt or stale):
            report.update({"ok": False, "token_ok": False, "error": "token_stale"})
            _stale_flag(args.out, True)
            _emit(args.out, report)
            print(json.dumps(report))
            return 2

    if args.probe_url and jwt and args.proxy:
        code = probe_bearer(args.probe_url, jwt, args.proxy)
        report["probe_status"] = code
        if code == 401:
            report.update({"ok": False, "token_ok": False, "error": "token_401"})
            _stale_flag(args.out, True)
            _emit(args.out, report)
            print(json.dumps(report))
            return 2

    report["token_ok"] = (not args.need_token) or (bool(jwt) and not stale)
    if jwt:
        report["userid"] = pay.get("userid")
    if report["ok"]:
        _stale_flag(args.out, False)
    _emit(args.out, report)
    print(json.dumps(report))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
