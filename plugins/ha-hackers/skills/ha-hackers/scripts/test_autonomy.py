#!/usr/bin/env python3
"""Contract tests for the autonomy pack. No network (except optional closed-port TCP)."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
VERIFY = HERE / "verify_evidence.py"
DISPATCH = HERE / "dispatch.py"
GUARD = HERE / "session_guard.py"


def run_py(script: Path, *args: str, check: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(script), *args],
        capture_output=True,
        text=True,
        check=check,
    )


class VerifyEvidenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.out = Path(self.tmp.name)
        (self.out / "docs-entry").mkdir()
        (self.out / ".bus").mkdir()

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _write(self, rel: str, text: str) -> None:
        p = self.out / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")

    def test_ignores_narrative_entry_md(self) -> None:
        self._write(
            "docs-entry/ENTRY.md",
            "## [high] Fake from narrative\n- Asset: /cms/prizes/webhook\n- Evidence: 200 unsigned\n- Request: POST\n",
        )
        self._write(
            "docs-entry/unauth-findings.md",
            "## [info] Health\n- Asset: /health\n- Evidence: 200 status ok\n- Request: GET\n",
        )
        r = run_py(VERIFY, "--out", str(self.out), "--pack", "docs-entry")
        self.assertEqual(r.returncode, 0, r.stderr)
        rec = json.loads((self.out / ".bus" / "VERIFY.json").read_text())
        titles = [x["title"] for x in rec["confirmed"] + rec.get("rejected", [])]
        self.assertFalse(any("Fake from narrative" in t for t in titles))
        self.assertNotIn("docs-entry/ENTRY.md", " ".join(rec["md_files"]))

    def test_pack_isolation_ignores_root_bola(self) -> None:
        self._write(
            "authz-findings.md",
            "## [critical] BOLA ledger\n- Asset: /backoffice/agents/payment\n- Evidence: 200 foreign\n- Request: GET\n",
        )
        self._write(
            "docs-entry/unauth-findings.md",
            "## [high] Unauth OTP jwt\n- Asset: /backoffice/fintech/customers/public/phone/send-otp\n- Evidence: 200 otpToken jwt\n- Request: POST\n",
        )
        self._write(
            "docs-entry/unauth-probes.jsonl",
            json.dumps({"path": "/backoffice/fintech/customers/public/phone/send-otp", "status": 200, "preview": "otpToken"}) + "\n",
        )
        r = run_py(VERIFY, "--out", str(self.out), "--pack", "docs-entry")
        self.assertEqual(r.returncode, 0, r.stderr)
        rec = json.loads((self.out / ".bus" / "VERIFY.json").read_text())
        titles = [x["title"] for x in rec["go"] + rec["confirmed"]]
        self.assertTrue(any("OTP" in t for t in titles))
        self.assertFalse(any("BOLA" in t for t in titles))
        self.assertGreaterEqual(rec["go_count"], 1)

    def test_dedup_duplicate_findings_files(self) -> None:
        block = (
            "## [high] Unsigned CMS prizes webhook accepts and persists writes\n"
            "- Asset: /cms/prizes/webhook\n"
            "- Evidence: 200 unsigned no HMAC ok:true credit not proven\n"
            "- Request: POST\n"
        )
        self._write("docs-entry/webhook-findings.md", block)
        self._write("docs-entry/authz-findings.md", block)
        self._write(
            "docs-entry/webhook-probes.jsonl",
            json.dumps({"path": "/cms/prizes/webhook", "status": 200, "preview": '{"ok":true}'}) + "\n",
        )
        r = run_py(VERIFY, "--out", str(self.out), "--pack", "docs-entry")
        rec = json.loads((self.out / ".bus" / "VERIFY.json").read_text())
        self.assertEqual(rec["parsed"], 1)
        self.assertEqual(rec["go_count"], 1)

    def test_go_dedup_same_path_different_titles(self) -> None:
        self._write(
            "docs-entry/authz-findings.md",
            "## [high] Unauth CMS prizes webhook 200 ok:true, no secret\n"
            "- Asset: /cms/prizes/webhook\n"
            "- Evidence: 200 unsigned no HMAC ok:true credit not proven\n"
            "- Request: POST\n",
        )
        self._write(
            "docs-entry/webhook-findings.md",
            "## [high] Unsigned CMS prizes webhook accepts and persists writes\n"
            "- Asset: /cms/prizes/webhook\n"
            "- Evidence: 200 unsigned no HMAC ok:true\n"
            "- Request: POST\n",
        )
        self._write(
            "docs-entry/webhook-probes.jsonl",
            json.dumps({"path": "/cms/prizes/webhook", "status": 200, "preview": '{"ok":true}'}) + "\n",
        )
        r = run_py(VERIFY, "--out", str(self.out), "--pack", "docs-entry")
        rec = json.loads((self.out / ".bus" / "VERIFY.json").read_text())
        self.assertEqual(rec["go_count"], 1)
        self.assertEqual(rec["parsed"], 2)


class DispatchTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.out = Path(self.tmp.name)
        (self.out / ".bus").mkdir()
        (self.out / "docs-entry").mkdir()

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_docs_hint_routes_pack(self) -> None:
        r = run_py(
            DISPATCH,
            "plan",
            "--out",
            str(self.out),
            "--target",
            "https://api.example.com/docs",
            "--pack",
            "auto",
        )
        rec = json.loads(r.stdout)
        self.assertEqual(rec["pack"], "docs-entry")
        self.assertEqual(rec["workflow"], "docs-entry")
        self.assertIn("hack-entry", rec["next"])
        self.assertIn("hack-webhook", rec["next"])

    def test_remainder_skips_ready_entry(self) -> None:
        (self.out / ".bus" / "READY.entry").write_text("")
        r = run_py(
            DISPATCH,
            "remainder",
            "--out",
            str(self.out),
            "--target",
            "https://api.example.com/docs",
            "--pack",
            "docs-entry",
        )
        rec = json.loads(r.stdout)
        self.assertEqual(rec["next"], ["hack-webhook"])
        self.assertEqual(rec["action"], "spawn")
        self.assertTrue((self.out / ".bus" / "NEXT.json").is_file())

    def test_no_exploit_without_go_count(self) -> None:
        for n in ("entry", "webhook"):
            (self.out / ".bus" / f"READY.{n}").write_text("")
        (self.out / ".bus" / "VERIFY.json").write_text(json.dumps({"go_count": 0}))
        r = run_py(DISPATCH, "remainder", "--out", str(self.out), "--pack", "docs-entry", "--target", "x/docs")
        rec = json.loads(r.stdout)
        self.assertEqual(rec["next"], [])
        self.assertEqual(rec["action"], "done")
        self.assertNotIn("hack-exploit", rec["next"])

    def test_exploit_namespaced_when_go(self) -> None:
        for n in ("entry", "webhook"):
            (self.out / ".bus" / f"READY.{n}").write_text("")
        (self.out / ".bus" / "READY.exploit").write_text("")  # other pack — must NOT skip
        (self.out / ".bus" / "VERIFY.json").write_text(json.dumps({"go_count": 2}))
        r = run_py(DISPATCH, "remainder", "--out", str(self.out), "--pack", "docs-entry", "--target", "x/docs")
        rec = json.loads(r.stdout)
        self.assertIn("hack-exploit", rec["next"])
        self.assertIn("hack-lead", rec["next"])

    def test_ha_hackers_exploit_gated(self) -> None:
        for n in ("recon", "api", "authz"):
            (self.out / ".bus" / f"READY.{n}").write_text("")
        (self.out / ".bus" / "VERIFY.json").write_text(json.dumps({"go_count": 0}))
        r = run_py(
            DISPATCH,
            "remainder",
            "--out",
            str(self.out),
            "--pack",
            "ha-hackers",
            "--target",
            "https://app.example.com",
        )
        rec = json.loads(r.stdout)
        self.assertNotIn("hack-exploit", rec["next"])
        self.assertIn("hack-lead", rec["next"])


class SessionGuardTests(unittest.TestCase):
    def test_proxy_down_exit_3(self) -> None:
        r = run_py(GUARD, "--proxy", "socks5h://127.0.0.1:1")
        self.assertEqual(r.returncode, 3)
        rec = json.loads(r.stdout)
        self.assertFalse(rec["proxy_ok"])

    def test_need_token_missing_exit_2(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            r = run_py(
                GUARD,
                "--allow-direct",
                "--need-token",
                "--out",
                d,
                "--token-file",
                str(Path(d) / "nope.json"),
            )
            self.assertEqual(r.returncode, 2)
            self.assertTrue((Path(d) / ".bus" / "TOKEN.stale").is_file())

    def test_docs_entry_no_token_ok(self) -> None:
        r = run_py(GUARD, "--allow-direct")
        self.assertEqual(r.returncode, 0)
        rec = json.loads(r.stdout)
        self.assertTrue(rec["token_ok"])


if __name__ == "__main__":
    os.environ.setdefault("HA_PROXY", "socks5h://127.0.0.1:10808")
    unittest.main(verbosity=2)
