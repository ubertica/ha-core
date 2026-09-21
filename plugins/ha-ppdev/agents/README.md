# User agents (`~/.grok/agents/`)

Grok loads `name:` from these `.md` files as `spawn_subagent` types.

## ha-ppdev team

Skill: `/ha-ppdev`

| Type | Lane |
|------|------|
| `ppd-arch` | Stack ADRs, bounded contexts, monorepo layout. Greenfield PumaPay API+backend — no legacy reuse without explicit import. |
| `ppd-api` | OpenAPI-first contracts, versioning, error envelope, idempotency keys. Owns api/openapi.yaml. |
| `ppd-backend` | HTTP services, handlers, domain wiring. Implements contracts from api + domain teams (ledger/payments/risk/kyc). |
| `ppd-db` | Schema, migrations, ledger/wallet tables, outbox. No destructive migrate without flag. |
| `ppd-auth` | Identity, sessions/JWT, scopes, device binding notes. Secrets redacted in chat. |
| `ppd-workers` | Background jobs, webhook ingest, transactional outbox, retries/DLQ. |
| `ppd-test` | Contract tests, integration fixtures, money-path sandboxes. Evidence in TEST-REPORT. |
| `ppd-tooling` | docker-compose, Makefile, local CI, seed scripts. Devex for the monorepo. |
| `ppd-sync` | Bus collab with ha-ledger/payments/risk/kyc/sre/sec/release/pumapay. Append-only JSONL. |
| `ppd-lead` | SUMMARY + BOARD + PR order. No invented GO. Money-writes gated. |

Conductor: references/AUTONOMY.md. Parent launches the workflow; do not pick lanes by hand.

Wiring: skill `/ha-ppdev`, workflow `ha-ppdev`, contract in the skill `references/CONTRACT.md`.
Children inherit all parent MCP/tools. They talk via `OUT/.bus/` + parent (no nested spawn).
