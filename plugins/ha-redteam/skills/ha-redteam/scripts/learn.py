#!/usr/bin/env python3
"""Wrapper → shared ha-rtk-kb learn."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

KB = Path.home() / ".grok" / "skills" / "ha-rtk-kb" / "scripts" / "kb.py"
sys.exit(subprocess.call([sys.executable, str(KB), "learn", "--pack", "ha-redteam", *sys.argv[1:]]))
