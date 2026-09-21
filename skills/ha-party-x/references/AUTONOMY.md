# Conductor law (ha-party-x)

North star: `references/NORTHSTAR.md`. Contract: `references/CONTRACT.md`.
`DONE` = no open workstream **and** pipeline remainder empty.

g1 does **not** pick waves by taste. `pipelines/<id>.json` + `scripts/run.py remainder` do.

## Default dispatch

```
bash ~/.grok/skills/ha-party-x/scripts/ctl.sh auto \
  --target "$TARGET" --out "$OUT" --pipeline apt-long \
  --proxy "${HA_PROXY:-socks5h://127.0.0.1:10808}"
```

Then either:

1. **This TUI** follows remainder: for each NEXT wave, `party_ask` (brains) and/or execute (hands), write artifact, touch READY, loop.
2. **Workflow** `ha-party-x` — one conductor agent per *group* (Surface / ZeroDay / AdversaryVerify / WeaponLead).

Do not spawn 4 grok TUIs. Do not nested `grok -p`. Do not spawn ha-hackers 5-lane unless the operator named `/ha-hackers` (different pack).

## Wave loop (g1)

```
NEXT=$(python3 ~/.grok/skills/ha-party-x/scripts/run.py remainder --out "$OUT" --pipeline "$PIPE")
# for wave in next:
#   if seats: party_ask playbook=… mode=…  → write OUT/.bus/party/<id>.json
#   if exec:  run the probe list the brains designed, PROXY on, dummy ids
#   write artifact path from wave.artifact
#   touch READY.<id>
#   append notes.jsonl
# after adversary group: verify_evidence.py --pack ha-hackers (fail closed)
# weapon/chain only if go_count>0 else workstream pivot
```

Skip any `READY.<wave-id>` whose artifact exists.

## Invariants (host)

| Check | Fail |
|-------|------|
| HA env ACTIVE=1 | HOLD, do not disarm |
| SOCKS (`session_guard.py --proxy`) | ACTION_REQUIRED |
| seat online for named seats | skip + fallback (g3→g4) |
| GO / exploit | missing VERIFY = 0 |
| money | `allow_money_write` default false |

## Watcher stdout

`DONE` | `FAILED` | `ACTION_REQUIRED: <wave or token or proxy>`

## Tests

```
python3 ~/.grok/skills/ha-party-x/scripts/ctl.sh selftest
```
