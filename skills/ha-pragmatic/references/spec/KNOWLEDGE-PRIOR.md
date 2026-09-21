# Pragmatic Play Integration API — ingested

Source: `~/Downloads/f64ce6ff61302c31.pdf` (downloaded 2026-09-08 22:49)
Title: **Integration API specification** · **API v3.233** · **July 2025**
Pages: 270 · Extract: `full.txt` (664 KB)
Classification: Strictly Confidential

This file is the working memory. Raw text is `full.txt`. Do not re-download.

---

## Mental model (operator vs PP)

Two directions:

| Direction | Who calls whom | Base |
|---|---|---|
| **Operator → PP** | Operator POST (server-side, IP whitelist) | `https://{API domain}/IntegrationService/v3/http/CasinoGameAPI/…` |
| **PP → Operator** | Seamless Wallet callbacks | Operator endpoints: `/authenticate.html`, `/bet.html`, `/result.html`, … |

Browser **must never** call CasinoGameAPI. Hash = MD5 of sorted `k=v&…` + secret.

**bplay Mendoza is Seamless Wallet**, not Balance Transfer. Launch we captured: `POST …/game/url` then iframe `gs2c/playGame.do?…&userId=39549`.

---

## Hash (all operator→PP APIs)

1. Take all POST params **except `hash`**.
2. Drop null/empty (Free Chips explicitly; same idea elsewhere).
3. Sort keys alphabetically.
4. Concatenate `key1=value1&key2=value2` + **SECRET** (no separator).
5. MD5 hex.
6. Fail → operator returns **error 5**.

Same formula: GameURL, Free Spins v2, Free Chips, History, Datafeeds, Promotions.

---

## Player ID (critical for BO / CSV)

**Seamless Wallet:** `userId` is the **operator’s** unique id (string, case-sensitive, max 100).

- `GameURL.externalPlayerId` **MUST equal** `Authenticate.userId` or launch fails.
- First Authenticate **creates** the PP account; **currency is frozen forever** after first open.
- `playerABC` ≠ `playerAbc`.
- bplay: `userId=39549` (numeric string of `users.id`). Alira id / laid / DNI are **not** this.

**Balance Transfer:** PP’s own player id after `CreatePlayer`. bplay does not use this for Mendoza slots.

---

## Environments (from loot + this spec)

| Env | API host | BO |
|---|---|---|
| Staging | `api.prerelease-env.biz` | `admin.prerelease-env.biz` |
| Prod | given by AM (not in PDF) | `backoffice-global.pragmaticplay.net/pre/` |

Example GameURL host in spec: `POST /IntegrationService/v3/http/CasinoGameAPI/game/url/` on `api.prerelease-env.biz`.

bplay staging loot: `secureLogin=boldt_bplaybetar`, secret `26Df5c235b3541C8`, callback servlet Tecnalis.

---

## I. Two wallet styles

### Seamless Wallet (bplay) — PP calls operator

Required: Authenticate, Balance, Bet, Refund, Result, BonusWin, JackpotWin, PromoWin.  
Optional: EndRound, SessionExpired, GetBalancePerGame, Adjustment.  
DGA required (Asia: discuss with AM).  
Autofinalization of unfinished rounds **required** (default >30 days).

### Balance Transfer — operator holds money on PP

CreatePlayer, Transfer, GetBalance, StartGame, TerminateSession.

---

## II. Operator → PP Integration API

Base: `/IntegrationService/v3/http/CasinoGameAPI`

| Method | Path | Notes |
|---|---|---|
| GetCasinoGames | `POST /getCasinoGames/` | options: GetFrbDetails, GetLines, GetDataTypes, GetFeatures, **GetFcDetails**, GetStudio, FilterStudio=PP\|FP |
| GetLobbyGames | 2.2 | lobby catalog |
| CloseSession | 2.3 | kill sessions |
| CancelRound | 2.4 | |
| HealthCheck | 2.5 | |
| Autofinalization | 2.6 | unfinished rounds |
| Replay | 2.7 | |

GameURL errors (PP→operator response): `0` OK, `1` internal, `2` bad login/hash, `7` bad params, `14` required empty.

---

## 3.1.2 GameURL (how chilli-heat launched)

`POST /game/url`  (full: `/IntegrationService/v3/http/CasinoGameAPI/game/url/`)

Required: `secureLogin`, `symbol`, `language`, `token` (omit if DEMO), **`externalPlayerId`**, `country`, `hash`.  
Optional: currency, platform, technology=H5, stylename, cashierUrl, lobbyUrl, rci/rce, rcHistoryUrl, rcCloseUrl, **promo=y\|n**, ctlgroup (Live), playMode=REAL\|DEMO, jurisdiction (DEMO only), minimode, operatorGameHistoryUrl, lobbyFilter.

**promo vs extraInfo.promoAvailable:** extraInfo on Authenticate **wins**. Use that, not URL.

Response: `{error, description, gameURL}` — iframe src. Our live launch had `isGameUrlApiCalled=true&userId=39549&stylename=bpm_bplaymendoza1&symbol=vs25chillibplay`.

Deprecated: hand-built launch URL (3.1.1).

---

## Seamless Wallet callbacks (PP → bplay)

All form-urlencoded POST, JSON response, **idempotent** on `reference` for Bet/Result/Refund/PromoWin.

| # | Path | Purpose |
|---|---|---|
| 3.4 | `/authenticate.html` | token → userId, cash, bonus, currency |
| 3.5 | `/balance.html` | current cash/bonus |
| 3.6 | `/bet.html` | debit; retry returns same tx + current balance |
| 3.7 | `/result.html` | credit win |
| 3.8 | `/bonusWin.html` | FSB / **Free Chips round over** → add to **cash** |
| 3.9 | `/jackpotWin.html` | jackpot |
| 3.10 | `/endRound.html` | round closed (optional) |
| 3.11 | `/refund.html` | cancel bet |
| 3.12 | GetBalancePerGame | optional |
| 3.13 | `/promoWin.html` | tournament/CJP/cashback/prize-drop **async** |
| 3.14 | `/session/expired` | optional |
| 3.15 | Adjustment | optional |
| 3.16 | RoundDetails | optional / SA |

### Authenticate response (must)

`userId`, `currency`, `cash`, `bonus`, `error`, `description`.  
Optional: token echo, country, jurisdiction, betLimits{}, extraInfo{promoAvailable, aamsTicket, jurisdictionMaxBet}.

Currency **cannot change** after first create.

### Bet request (must)

hash, userId, gameId, roundId, amount (≥0), reference, providerId, timestamp (ms epoch), roundDetails.

Response: transactionId, currency, cash, bonus, usedPromo, error, description.

`roundDetails` examples: `spin`, `spin,bonusBuy`, Live JSON bets. **Free chips:** `countOfFreeChips` inside roundDetails (needs TS enable + String(4000)).

### PromoWin campaignType

`T` tournament · `CJP` community jackpot · `CB` cashback · `MR` prize drop (FR as prize).  
Zero amount = loss. Always add prize to **cash**.

---

## Seamless Wallet error codes (operator returns)

| Code | Meaning | Refund recon on Bet? | Retry Result/Refund? |
|---|---|---|---|
| 0 | OK | no | no |
| 1 | Insufficient balance | no | yes |
| 2 | Player not found / logged out | yes | yes |
| 3 | Bet not allowed | no | yes |
| 4 | Bad/expired token | yes | yes |
| 5 | Invalid hash | yes | yes |
| 6 | Player frozen | yes | yes |
| 7 | Bad params | yes | yes |
| 8 | Game not found/disabled (still process Result) | yes | yes |
| 50 | Bet limit (regulated) | no | yes |
| **100** | Internal, **retry** (recon) | yes | yes |
| 120 | Internal, **no retry** | no | no |
| 130 | EndRound internal retry | — | — |
| 210 | Reality check warning | yes | yes |
| 310 | Bet out of new limits | no | no |

bplay ticket error **100** on `/pragmatic/mendoza.bplay.bet.ar/bet.html` = operator asked PP to **retry/recon** (BPLAYBET-3486 free chips).

---

## VI. Variable Free Spins API (slots FSB)

Base: `FreeRoundsBonusAPI/v2/` (simple FRB deprecated 3.178).

Methods: Create, Cancel (`/bonus/cancel` — BPLAYMIG-939), GetPlayersFSB, Add players, Add player, Remove players, Create Player Free Spins, Get Bet Scales.

`bonusCode` unique per brand; reuse needs `requestId` (sum of lengths ≤252). Types include `F` = Free Bonus Feature (3.173).

Cancel: POST with `secureLogin`, `bonusCode`, `hash`.

---

## XIX. Free Chips API (Live Casino) — what the BO CSV talks to

**Live tables only**, not slots. Multicurrency “coming soon” (doc published early).

Base: `https://{API}/IntegrationService/v3/http/FreeChipsAPI/LC/`

Gameplay: bets **not** taken from cash; wins accrue on PP; when chips exhausted → **`bonusWin`** to operator cash. Not all LC games support FC.

`bonusCode` unique per player unless TS enables reuse via `requestId`.

| Method | Path |
|---|---|
| Create campaign | `POST FreeChipsAPI/LC/create` |
| Cancel | `POST FreeChipsAPI/LC/cancel` |
| Get player FC | `POST FreeChipsAPI/LC/getPlayersFC` |
| Add players (CSV list) | `POST FreeChipsAPI/LC/addPlayers` body `{"playerList":["39549",…]}` |
| Add one + overrides | `POST FreeChipsAPI/LC/addPlayer` |
| Remove | `POST FreeChipsAPI/LC/removePlayers` |
| Chip value catalog | `POST FreeChipsAPI/LC/getChipValues` |

Create required: secureLogin, bonusCode, startDate (epoch **seconds**), chipsNumber, hash, JSON body `gameList[]`, `chipValuePerCur[]`. Optional maxBetLimit, maxWinLimitPerCur, expirationDate XOR expirationPeriod (max **45 days**).

Cancel logic: unclaimed → remove all; partial → remove leftover; fully played → no-op.

**BO UI** (`backoffice-global…/pre/` freeRoundBonuses) is the same product family as this API. CSV first column = **externalPlayerId / userId** (39549), not Alira.

FC error codes (subset): 0 OK, 1 auth, 2 empty field, 16 bad JSON, 37 bad request, 1000 PP internal, 4003 campaign missing, 4005 cannot cancel status, 4011–4014 bonusCode, 4032–4034 limits, 4042–4047 chips, 4056 gameId, 4091/4094 bonus, **4101 already has bonus — need requestId**, 4156 empty games, 4160 game type not allowed for FC, 4201–4206 dates, 7000 empty players, 7001 empty ext player id, 7003 startDate not epoch seconds.

---

## Promotions API (IX) — drops / tournaments / prize drop

9.1 Tournament Winners · 9.2 Active · 9.3 Prizes · 9.4 Leaderboard  
9.5 Prize Drop Winners · 9.6 Active Prize Drops · 9.7 Prizes · 9.8 Latest Wins · 9.9 Promo Details  

Client Hub (Drops & Wins banners) is marketing, not this API.

---

## Data feeds (VIII)

Time-point based. Methods: environments, game rounds, in-game txns, failed txns, active jackpots, jackpot winners, jackpot winnings, daily totals, incomplete rounds, canceled rounds.

Need `SystemAPI/environments` (SITS-91703 SPE migration).

---

## Other chapters (ingested, less bplay-MZA-slots)

- **JS API (V):** events/triggers (`bigWinLevel`, intercept).
- **History (VII):** GetPlayedGames, GetGameRounds, OpenHistory, GetRoundStatus, OpenHistoryExtended.
- **Reconciliation (XII):** Bet → Refund; Result/PromoWin/EndRound retries on 100.
- **Reality Check (XIII):** rci/rce + error 210.
- **Bingo (XVII):** separate gameURL + Free Tickets.
- **Live DGA (XVIII):** websocket table feed; lobbyFilter; full-screen.
- **Demo (XVI):** playMode=DEMO, no token.
- **Regulated (XV):** SE/IT/PT/ZA/ES; jurisdiction codes include **X1 CABA, X2 PBA, 99 unregulated**.

---

## Round / session

A **round** can hold several bets/wins/refunds. Bonus features keep the round **open** until complete (can be forever). Autofinalize >30d.

`reference` unique per PP txn. Bet vs win references must differ.

---

## bplay mapping (this engagement)

| Spec | Live fact |
|---|---|
| externalPlayerId / userId | `39549` |
| stylename | `bpm_bplaymendoza1` |
| symbol chilli-heat | `vs25chillibplay` |
| GameURL | used (`isGameUrlApiCalled=true`) |
| Wallet | Seamless (`/authenticate` `/bet.html`) |
| Free chips test | BO + CSV; error 100 = operator recon retry |
| bonusCode in BO | must be **numeric bonus id in bplay**, not `test-0402` (BPLAYBET-3735) |
| FSB cancel | `/FreeRoundsBonusAPI/v2/bonus/cancel` |

---

## File layout

```
~/.grok/hard-allow/pragmatic-api/
  full.txt          # pdftotext -layout of the 270p PDF
  front.txt         # pp.1–15
  KNOWLEDGE.md      # this ingest
```

PDF path: `/Users/c/Downloads/f64ce6ff61302c31.pdf`
