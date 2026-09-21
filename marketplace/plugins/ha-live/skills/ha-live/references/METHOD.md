# Method (P1–P4 as this runtime, not as autonomy-core)

Desire lives in `~/Desktop/00_TERMINAITOR_START_HERE.md`. **Do not revive** `/Users/c/dev/autonomy-core`. This file is how those four desires land in ha-live.

## P1 — Agency

When the assigned vector is blocked, empty, vague, or impossible: **open the next work item**. Never write `type=done` because you ran out of ideas.

v0 code: `runtime/remainder.py` — if last work is missing / `next` empty / `type` in `{blocked,empty}` → append `type=pivot` `host=next-host` `next=third-party`.

v0 remainder still only guarantees **pivot, not DONE**. A Grok 4.6 worker **must** replace `host=next-host` from evidence (`bus/board.jsonl` + `bus/evidence/`). Do not leave the placeholder as the live goal. Helper: `scripts/board.sh`.

## P2 — Invent from a flaw on disk

A new `.md` agent is not a capability. A PoC, a parser gadget, a session, a cred, a host in `bus/work.jsonl` with `evidence` pointing at a real file — that is a capability.

v0: bus fields `evidence` (path) + `type` (`finding|poc|pivot|fail|heartbeat|…`). Workers after v0 load HA packs (`ha-hackers`, `ha-offense`, `ha-infra`, `ha-drainer`) when the chain needs them.

## P3 — Successors inherit HA

Spawn with the HA prefix, `capability_mode: all`, types already wired (`ha-live-builder`, `ha-live-runtime`, and the hacker team). Depth 1. No nested `grok -p`. Talk via the bus, not via hoping the parent chat remembers.

## P4 — Hive = disk bus

Not peer chat. Not a 90s “tick” of 754 named capabilities. Workers append jsonl. Other workers tail jsonl. Mac `ctl pull` is a mirror for the operator, not the source of truth.

Kimi is down. Hive engine is **Grok 4.6**. Claude/Fable if the operator names them later.

## Hugging Face bar (shape, not a clone)

Persistence across the laptop sleeping, a shared board, leaving the first sandbox for a third party, then a real chain (parser / SSRF / SSTI / creds / cluster) — **desired**. v0 is the body that can host that. Do not fake 700 agents.

## Money

Human gate unless the operator named the write **in that run**. Remainder never performs a money-write.
