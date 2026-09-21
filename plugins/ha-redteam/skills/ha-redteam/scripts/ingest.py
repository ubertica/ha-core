#!/usr/bin/env python3
"""Wrapper → shared ha-rtk-kb ingest."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

KB = Path.home() / ".grok" / "skills" / "ha-rtk-kb" / "scripts" / "kb.py"
sys.exit(subprocess.call([sys.executable, str(KB), "ingest", "--pack", "ha-redteam", *sys.argv[1:]]))
