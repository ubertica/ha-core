---
name: ha-upgrade-v1
description: >
  Apply HA upgrade plugin v1 (frozen /learn actions). Use when the operator
  says apply upgrade v1, instalar ha-upgrade-v1, or rollback that version.
---

# ha-upgrade-v1

This folder is a **frozen pack**. Do not edit it to make v2; pack a new plugin.

## Apply

```bash
python3 ~/.grok/skills/ha-upgrade/scripts/pack.py apply --version 1 --go
```

Without `--go`: selftest only.

## Rollback

```bash
python3 ~/.grok/skills/ha-upgrade/scripts/pack.py rollback --version 1 --go
```

Consent rules are the same as `/learn` step 4: no apply of `requires_confirmation` without a pick.
