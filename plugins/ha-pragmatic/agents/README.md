# User agents (`~/.grok/agents/`)

Grok loads `name:` from these `.md` files as `spawn_subagent` types.

## ha-pragmatic team

Skill: `/ha-pragmatic`

| Type | Lane |
|------|------|
| `pra-spec` | SoT ingest of Integration API v3.233 (July 2025). Chapter index, version control, method catalog. Never invent endpoints. |
| `pra-hash` | Hash formula (3.2/4.2/6.1/7.1): drop empty, sort keys, concat k=v& + SECRET, MD5 hex. Error 2 vs 5. |
| `pra-wallet` | Seamless Wallet callbacks ch.III: Authenticate Balance Bet Result Refund BonusWin JackpotWin PromoWin EndRound SessionExpired Adjustment GetBalancePerGame RoundDetails. bplay=Seamless. |
| `pra-games` | CasinoGameAPI ch.II: GetCasinoGames GetLobbyGames GameURL HealthCheck CloseSession CancelRound. GameURL 3.1.2. JS API ch.V. |
| `pra-promo` | Free Spins ch.VI, Free Chips, Promotions ch.IX (tournaments prize-drops), Jackpot feeds. |
| `pra-feeds` | History ch.VII, Data feeds ch.VIII, Business Stats ch.X, Reconciliation ch.XII. |
| `pra-bo` | PP Live BO casinoadmin/prelive0 + slots backoffice-global. JWT nebular. Honest GO/HOLD on session. |
| `pra-test` | Staging HTTP vs api.prerelease-env.biz. SOCKS AMS. IP whitelist. JSON error vs CloudFront 403. No live money. |
| `pra-qa` | Gates: hash, IP ACL, Seamless required methods, no invented GO, no live PSP/money without flag. |
| `pra-dev` | Operator integration notes CHANGES.md + IMPL.md. No Fastify default. Tecnalis/bplay callbacks. |
| `pra-sync` | Bus collab with ha-hackers/loot. Never truncate jsonl. |
| `pra-lead` | SUMMARY + BOARD. Honest GO-spec / HOLD-whitelist / HOLD-live-money. No invented GO. |

Conductor: references/AUTONOMY.md. Parent launches the workflow; do not pick lanes by hand.

Wiring: skill `/ha-pragmatic`, workflow `ha-pragmatic`, contract in the skill `references/CONTRACT.md`.
Children inherit all parent MCP/tools. They talk via `OUT/.bus/` + parent (no nested spawn).
