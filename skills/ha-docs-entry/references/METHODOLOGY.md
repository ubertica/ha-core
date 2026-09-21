# OAE — OpenAPI-as-entry methodology

Use this when the attack surface **is** an unauthenticated OpenAPI/Swagger document (`/docs`, `/openapi.json`, `/swagger.json`, `/api-docs`) with missing/empty `securitySchemes` or ops without `security`.

Do **not** dispatch the standard 5-lane `ha-hackers` recon→authz→exploit for this question. The spec **is** the inventory. The question is: which documented ops are callable **without** a session.

Parent: `ha-docs-entry` skill. Lanes: `hack-entry` (waves 0–2), `hack-webhook` (wave 3). Exploit/lead only after confirmed GO (wave 4).

## Wave 0 — Fetch + integrity

- GET the live spec. Save `OUT/docs-entry/openapi-live.json`.
- Record: bytes, sha256, `info.title/version`, `servers[]`, path count, op count, `components.securitySchemes` (often `{}`).
- `/docs` 200 JSON is itself an **info** finding (full attack map), not yet a money GO.

## Wave 1 — Bucket (deterministic)

Run `scripts/bucket_openapi.py`. Do not LLM-classify 1000+ ops.

Primary bucket priority (first match wins):

| Priority | Bucket | Match |
|----------|--------|--------|
| 1 | `money_write` | deposit, withdraw, transfer, payout, add-balance, force-approve, credit, debit |
| 2 | `webhook` | webhook, hook (path) |
| 3 | `payment_callback` | callback, ipn, notify, cashin, `/integrations/payments` |
| 4 | `auth_entry` | login, register, otp, remotelogin, passkey, password-reset, refresh-token |
| 5 | `pam_bot` | `/pam`, `/bot`, telegram |
| 6 | `payment_public` | payment-link, `/public/`, fintech/customers/public |
| 7 | `admin` | `/admin`, superuser, filesystem, finance-keys |
| 8 | `health` | `/health`, `/metrics` |
| 9 | `docs` | `/docs`, `/swagger`, openapi.json |
| 10 | `cms_public` | `/cms` |
| 11 | `visor_public` | visor, iframe game |
| 12 | `jwt_likely` | `/wallet`, `/backoffice`, `/agents` (except payment-link) |
| 13 | `other` | leftover |

An op may list extra tags; **primary** decides probe policy.

## Wave 2 — Unauth probe (`hack-entry`)

Rules:

- No `Authorization`. No stolen JWT unless parent said dual-run.
- GET / HEAD / OPTIONS first.
- Empty JSON POST **only** on `auth_entry`. Never POST `money_write`.
- Path params: spec `example`, else sentinel `test`.
- Cap: 150 paths / 400 jobs unless parent raises it.
- Egress: SOCKS/AMS when OPSEC says so (never Mac ISP IP → third-party target).
- Record jsonl: method, spec_path, status, size, content-type, preview[:500], CORS ACAO/ACAC, elapsed.

Verdict:

| Status + body | Label | Finding? |
|---------------|-------|----------|
| 200/206 + sensitive data (PII, balances, pending money, secrets, other-user objects) | unauth-read | **GO** |
| 200 + public CMS/health/ok | expected-public | info |
| 400 + schema/missing-field oracle | reachable-unauth | info foothold |
| 401/403 | gated | not a finding |
| 404 | dead / method-mismatch | skip |
| 5xx + stack/property leak | error-oracle | low/info |
| OPTIONS 204 + ACAO reflect + ACAC true | CORS | already tracked separately; note if new origin |

## Wave 3 — Webhook (`hack-webhook`)

For `webhook` + `payment_callback` + `/bot/` + telegram:

1. POST unsigned: `{}` / `[]` / empty / form.
2. Header variants: none, `X-Signature: test`, `X-Hub-Signature-256: sha256=00`, `Stripe-Signature: t=1,v1=00`.
3. Telegram/PAM: dummy `update_id`, empty message. Record `processed` / reason.
4. **Do not** send a body that credits an account, approves a voucher, or pays out unless the parent named that payload.

Verdict:

| Result | Label | Finding? |
|--------|-------|----------|
| 200 on unsigned mutating webhook (prize, cashin, deposit callback, credit) | unsigned-accept | **GO** |
| 200 `processed:false` / NO_LINK_CODE | reachable, not mutating | info |
| 400 missing field names | unsigned-reachable + oracle | info / candidate |
| 401/403 invalid signature | gated | not a finding |
| 5xx on undefined `.split` | crash oracle | low |

## Wave 4 — Exploit gate (disk)

Run `python3 ~/.grok/skills/ha-hackers/scripts/verify_evidence.py --out OUT --pack docs-entry`.

Spawn `hack-exploit` + `hack-lead` **only if** `OUT/.bus/VERIFY.json` `go_count > 0`.

If none: script writes `OUT/docs-entry/NEGATIVE.md`. Do not invent GO. Do not spawn unused standard lanes. Do not trust the prober's `confirmed_count`.

## Disk bus

| Flag | Meaning |
|------|---------|
| `OUT/.bus/READY.entry` | ENTRY.md + buckets + unauth jsonl done |
| `OUT/.bus/READY.webhook` | WEBHOOK.md + webhook jsonl done |
| `OUT/.bus/READY.docs-api` | optional: hack-api classified the spec |
| `OUT/.bus/READY.docs-authz` | optional: hack-authz probed PAM/bot/public |
| `OUT/.bus/VERIFY.json` | disk gate (go_count) |
| `OUT/.bus/PLAN.json` | pack router |
| `OUT/.bus/EGRESS.json` | proxy/JWT preflight |
| `OUT/.bus/TOKEN.stale` | JWT expired and Chrome refresh failed |

Notes: append `OUT/.bus/notes.jsonl` `{from,to,type,path,msg}`.

## Finding block

Same as ha-hackers CONTRACT:

```
## [critical|high|medium|low|info] title
- Asset:
- Request:
- Evidence:
- Impact:
- Next:
```

Evidence = request + status + body preview on disk. No evidence → not a finding.
