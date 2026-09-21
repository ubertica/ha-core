---
name: ha-upgrade
description: Pack /learn into a new ha-upgrade-vN plugin. Never overwrite. Never auto-install.
---

Follow `~/.grok/skills/ha-upgrade/SKILL.md`.

Default: `python3 ~/.grok/skills/ha-upgrade/scripts/pack.py pack` then `selftest --version N`.
Do not `grok plugin install` unless the operator says. Do not apply without `--go`.
