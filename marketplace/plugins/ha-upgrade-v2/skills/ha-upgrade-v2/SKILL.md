---
name: ha-upgrade-v2
description: >
  Apply HA upgrade plugin v2 (frozen /learn actions). Use when the operator
  says apply upgrade v2, instalar ha-upgrade-v2, or rollback that version.
---

# ha-upgrade-v2

This folder is a **frozen pack**. Do not edit it to make v3; pack a new plugin.

## Apply

```bash
python3 ~/.grok/skills/ha-upgrade/scripts/pack.py apply --version 2 --go
```

Without `--go`: selftest only.

## Rollback

```bash
python3 ~/.grok/skills/ha-upgrade/scripts/pack.py rollback --version 2 --go
```

Consent rules are the same as `/learn` step 4: no apply of `requires_confirmation` without a pick.
