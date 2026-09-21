---
name: ha-party-x
description: >
  Extreme offensive party pipelines for g1–g4: APT-long, 0day-deep, authz-brutal,
  docs-entry-x, red-on-red. Longer/deeper than ha-hackers 5-lane. Brains via
  party_ask+playbook, g1 executes. Triggers: /ha-party-x, party extreme,
  playbooks party, apt-long, red-on-red, party pipelines.
---

# ha-party-x

Canonical: `~/.grok/skills/ha-party-x/`
Contract: `references/CONTRACT.md` · Autonomy: `references/AUTONOMY.md`
Seats: `references/SEATS.md` · Bar: `references/NORTHSTAR.md`

g1 = this TUI (tools). g2/g3/g4 = brains (`party_ask` / `party_brain.mjs`). No 4 TUIs. No nested `grok -p`.

## Pipelines

| id | Waves | When |
|----|-------|------|
| `apt-long` | 19 | default. OSINT→surface→authz→0day→webhook→red-on-red→verify→weapon→chain→persist |
| `0day-deep` | 13 | HF-bar classes only (SSRF/SSTI/parser/proto/deser/graphql/runtime) |
| `authz-brutal` | 12 | IDOR sibling/vertical/tenant/mass-assign/JWT/batch/verb/race |
| `docs-entry-x` | 11 | live `/docs` but with bucket+HMAC+refute, not the short 2-lane |
| `red-on-red` | 7 | existing OUT; no spray until g4 vote |

## Dispatch

```
bash ~/.grok/skills/ha-party-x/scripts/ctl.sh auto \
  --target "$TARGET" --out "$OUT" --pipeline apt-long \
  --proxy "${HA_PROXY:-socks5h://127.0.0.1:10808}"
```

Then **you (g1)** run the remainder loop in AUTONOMY.md. Workflow `ha-party-x` is the grouped-agent fallback.

Per brain wave:

```
party_ask text=… seats=g2,g3 mode=round playbook=g2-surface max_tokens=8000
# or
node ~/.grok/skills/ha-party-x/scripts/party_brain.mjs \
  --playbook g3-weapon --seats g3 --mode parallel --wave w09-0day-hypotheses \
  --target "$TARGET" --out "$OUT" --text "…"
```

Exploit/weapon waves only if disk `go_count>0`. g3 offline → g4 dual (weapon then adversary).

## Not ha-hackers

Do not spawn `hack-recon`… unless the operator said `/ha-hackers`. This pack is the party. Reuse their `session_guard.py` + `verify_evidence.py` + `workstream.py` only.

## Sibling party teams (not these pipelines)

| Skill | When |
|-------|------|
| `/ha-redteam` | **live** civil party: deep audit/test + Jira. No loot. Daniel/Puma default. |
| `/ha-blackhat` | **WIP** — operator still forging. Do not dispatch as complete. Same `ha-rtk-kb` when ready. |
| `ha-rtk-kb` | shared intel/memory/findings-index. Lanes stay separate. |

`ha-party-x` pipelines stay the extreme wave set. Redteam/blackhat are the standing party *teams*. Do not mix OUT trees.
