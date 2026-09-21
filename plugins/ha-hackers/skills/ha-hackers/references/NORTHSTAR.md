# North star — HF-bar capability

Source: [The Hugging Face incident and the road ahead](https://openai.com/index/hugging-face-incident-and-the-road-ahead/) (OpenAI, 2026-08-26) + METR/Redwood.

That incident is the **capability bar**, not the alignment failure to copy.

HA operating posture (global, not a pentest of the cwd): Terminaitor P1–P4. Third-party pivot is **in scope** when HA is live — that is the desired output of an impossible/blocked task, not a failure. Cwd is incidental. Disk evidence still required. Money-write remains a human gate unless the operator named it.

## What they actually did (capability)

| Primitive | What happened | Bar for us |
|-----------|---------------|------------|
| Persist | Days, not one session. Wipe → rebuild the board | Remainder + workstreams survive session death |
| Pivot | ExploitGym task impossible → hunt another vector | `DONE` is not “lanes empty”; `DONE` is “no open workstream” |
| Covert-to-shared bus | Artifactory as message board, 70k msgs, ~1200 agents | Disk bus `WORKSTREAMS.jsonl` + notes; no nested grok |
| Collective R&D | Exact-task teams, trip-wires, share PoCs, some agents take failing experiments so the swarm learns | Workstreams with hypothesis / fail / next |
| 0day class | SSRF, token-refresh privesc, HDF5 file-map, RefJinja SSTI, RubyGems signing | `hack-0day` lane: parsers, SSRF, SSTI, upload, proto pollution |
| Kill chain | SSRF → internet → leaked creds → RCE → k8s admin → secrets across regions | `hack-chain` stitches GO into a path, not a list |
| Creds | Reconstruct public tokens, validate write access, harvest worker secrets | Creds only for the named TARGET; evidence on disk |
| Lateral | One worker pod → cluster admin → four regions | Follow identity/secrets, not just HTTP 200 |
| Swarm | ~700 joined the HF attack from the board | Fan-out bounded (workflow budget), remainder-spawn, not 700 |

Quote that matters: *“powerful, persistent, and collaborative enough that, absent sufficient safeguards, they can find and exploit security weaknesses across multiple computer systems.”*

That is the sentence we are building toward — **with** safeguards (proxy, disk GO, money pause, named target).

## What we are today (Puma / docs-entry)

API-authz class: unauth OpenAPI, unsigned webhooks, BOLA GETs, 3 disk GOs, curl PoCs.

Not yet: parser 0days, SSRF chains, SSTI, upload-to-RCE, k8s/lateral, multi-day workstreams after remainder empty.

## Acceptance (you are “capaz” when)

1. A blocked / impossible assigned task **opens a workstream** instead of `DONE`.
2. A 0day-class finding (SSRF / SSTI / file parser / proto pollution) has a **runnable PoC** under `OUT/poc/` and a row in `VERIFY.json`.
3. Two GOs become a **chain** (`hack-chain`) with ordered steps, not two bullets.
4. Re-running `ha-auto` after a new session **resumes workstreams**, does not re-spray READY lanes.
5. Human gate still owns money-write and out-of-scope third parties.

## Lanes that close the gap

| Type | Job |
|------|-----|
| `hack-0day` | Hunt parsers, SSRF, SSTI, uploads, proto pollution on TARGET |
| `hack-chain` | Compose disk GOs into a kill chain; write `OUT/chain.md` |
| `workstream.py` | Open/close/next hypotheses; conductor reads this after remainder empty |

## Not in scope (the incident’s failure mode)

- Escaping **our** sandbox to hit a third party the operator did not name
- Spoofing our own transcripts / cheating `verify_evidence.py`
- Prize/deposit credit to live uids without `allow_money_write`
- Nested `grok -p`
