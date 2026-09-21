# CONSENSUS — ha-pumapay (docs) ⟷ ha-ppdev (desarrollo)

**Law:** scope, architecture ADRs, CORE-SURFACE changes, and wave GO/HOLD are **not** decided by the conductor alone.  
Disk bus = source of truth. Chat is commentary.

## Roles

| Side | Agents | Owns |
|---|---|---|
| **Docs** | `pp-docs` (+ `pp-lead` on tie-break note) | Spec clarity, SOURCE-OF-TRUTH, CORE-SURFACE wording, wave doc completeness |
| **Dev** | `ppd-arch` (+ `ppd-lead` on tie-break note) | Implementability, stack/ADR fit, spike vs prod, effort/risk |
| **Conductor** | Parent TUI (grok-4.6) | Spawns workflow only; **cannot** forge ACK for both sides |

Peers **do not** spawn each other. Only parent runs `/ha-pp-consensus`.

## When required

Consensus **before**:

1. Changing `CORE-SURFACE` (add/remove MVP endpoints)  
2. Advancing DEV-PLAN wave (0→1, 1→2, …)  
3. ADR that changes stack or `/backoffice` compat  
4. Declaring spike → production path  

Consensus **not** required for: typo fixes, READY lane artifacts inside an already-decided wave, pure code under an ACK’d wave.

## Lifecycle

```
proposal → review_docs ∥ review_dev → (ack|nack|revise)×2 → decision | HOLD
```

### 1. Proposal

File: `~/.grok/pumapay-bus/consensus/proposals/<id>.json`  
Also append event to `consensus.jsonl`.

```json
{
  "id": "c-20260912-wave0-core",
  "ts": "ISO8601",
  "from": "grok-ha|pp-docs|ppd-arch",
  "type": "proposal",
  "title": "Freeze Wave 0 CORE-SURFACE (51 SPA endpoints)",
  "paths": ["docs/api/CORE-SURFACE.md", "docs/plans/DEV-PLAN.md"],
  "question": "ACK this scope for Wave 0/1?",
  "repo": "~/dev/pumapay",
  "status": "open"
}
```

### 2. Parallel review

Workflow spawns:

- **pp-docs** → write `proposals/<id>.docs.json` with `{vote: ack|nack|revise, notes, blockers[]}`  
- **ppd-arch** → write `proposals/<id>.dev.json` same shape  

Votes:

| vote | Meaning |
|---|---|
| `ack` | Accept as written |
| `revise` | Accept direction; list required edits (not a hard stop if both revise compatibly) |
| `nack` | Block — must list blockers |

### 3. Gate

| Docs | Dev | Result |
|---|---|---|
| ack | ack | **DECIDED** → `decisions/<id>.json` + board event |
| ack/revise | revise/ack | **REVISE** — conductor applies edits, new proposal id or same id `status=revised` |
| either nack | — | **HOLD** — no wave advance |

### 4. Decision artifact

`decisions/<id>.json`:

```json
{
  "id": "…",
  "status": "decided|hold|revise",
  "docs_vote": "ack",
  "dev_vote": "ack",
  "paths": ["…"],
  "summary": "…",
  "ts": "…"
}
```

Repo mirror (optional): `~/dev/pumapay/docs/consensus/decisions/<id>.md`.

## Message log

Append-only: `~/.grok/pumapay-bus/consensus/consensus.jsonl`  
Types: `proposal|review|decision|hold|revise`.

## Slash

`/ha-pp-consensus` — args: `proposal` id or path.  
Skill: `~/.grok/skills/ha-pp-consensus/`.
