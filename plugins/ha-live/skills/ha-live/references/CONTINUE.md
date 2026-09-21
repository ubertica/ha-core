# Continue here (new grok-4.6 session)

Cwd `/Users/c/dev/ha-live`. HA armed. Model **grok-4.6**. No Kimi. No nested `grok -p`.
This is the **Terminaitor desire + HF bar** organism (always-on AMS remainder + shared board + third-party pivot). Not Puma-the-product. Not autonomy-core. Not a pentest of this folder.

## 30-second start

```bash
cd /Users/c/dev/ha-live
bash scripts/ctl.sh status
bash scripts/board.sh open
cat CONTINUE.md BOARD.md proof/BLOCKER.md
```

If unit is **not** `active`: `BUILD.md` then `ctl start` + `prove.sh`. If it **is** active: do **not** redo prove.

## What is already true

| Piece | State |
|-------|--------|
| AMS remainder | live (`systemctl is-active ha-live`) |
| Bus | `/opt/ha-live/bus/{events,work,board}.jsonl` |
| P1 placeholder | remainder still emits `next-host` if work is empty/blocked |
| P1 pick (this session) | live work is **not** `next-host` — see board ids below |
| P3 | spawn `ha-live-runtime` / hacker lanes, HA prefix, `capability_mode: all`, depth 1, talk via bus |
| P4 | Grok 4.6 hive on disk jsonl |
| Egress | **HOLD** `HA_AMS_PROXY` — `proof/BLOCKER.md` |
| Money | gated (not named) |

## Open goals (board)

1. **`egress-ams-xray`** — first-party. SOCKS hello on `:18082` ok; VLESS/REALITY data empty. Repair outbound **or** new AMS SOCKS. Gate: `scripts/probe-ams-proxy.sh` exit 0, then `HA_AMS_PROXY=… ctl start`.
2. **`pivot-pumapay`** — third-party, **blocked on (1)**. Hosts from disk: `app.pumapay.cash` / `api.gplaygap.com` (`proof/evidence/pumapay-hosts.json`). Full chain (parser/SSRF/SSTI/creds/infra) after proxy works. **No money-write** unless operator names it.
3. **`pivot-pumapay-recon`** — disk harvest already on board (`proof/recon-pumapay/`). Live recon only after (1) GO, via AMS SOCKS, never Mac ISP.

## Law pointers (do not re-explain)

`INTENT.md` `METHOD.md` `BUS.md` `BOARD.md` `SPLIT.md` `DO_NOT.md` `CABLES.md` `PROMPT.md`

## This session's job if you just arrived

Unblock (1). Do not fake GO. Do not egress Puma from Mac ISP. Spawn workers that **append the board**.
