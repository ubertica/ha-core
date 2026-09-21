---
name: ha-pp-consensus-tick
description: >
  Periodic status tick for ha-pp-consensus. Lists open proposals and missing
  votes. NEVER proposes, NEVER ACKs, NEVER writes decisions. Structure r1 closed.
---

# ha-pp-consensus-tick

Canonical protocol: `$PUMAPAY_ROOT/bus/consensus/CONSENSUS.md`  
Live bus: `$PUMAPAY_BUS/consensus`  
Ctl: `$GROK_HOME/skills/ha-pp-consensus/scripts/ctl.sh tick`

## What tick does

1. `ctl.sh tick` → `consensus.py status` (read-only).
2. Print closed ids (`c-20260912-repo-estructura-r1`, `c-20260912-wave0-core-r1`).
3. List open proposals / missing `.docs.json` / `.dev.json` if any.
4. Do **not** spawn `pp-docs` or `ppd-arch`.
5. Do **not** write ACK/NACK/REVISE.
6. Do **not** create a new proposal id.

## CLI

```bash
source "$PUMAPAY_ROOT/equipos/lib/paths.sh"
bash "$GROK_HOME/skills/ha-pp-consensus/scripts/ctl.sh" tick
```

There is no remainder-lane table. This pack is a **gate tool**, not a product wave.

## Always / never

- Always: status + reminder that conductor cannot forge ACK×2.
- Never: nested `grok -p`, invented GO, reopening structure r1, live paths `/Users/<op>` or `docs/pumapay-v2`.

See `/ha-pp-consensus` for propose/auto/verify when the **operator** asks for a vote.
