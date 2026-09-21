#!/usr/bin/env python3
"""Apply or rollback ha-upgrade-v1. Thin wrapper around pack.py."""
import runpy
import sys
from pathlib import Path

sys.argv = [
    "pack.py",
    sys.argv[1] if len(sys.argv) > 1 else "apply",
    "--version",
    "1",
    *sys.argv[2:],
]
runpy.run_path(str(Path.home() / ".grok" / "skills" / "ha-upgrade" / "scripts" / "pack.py"), run_name="__main__")
