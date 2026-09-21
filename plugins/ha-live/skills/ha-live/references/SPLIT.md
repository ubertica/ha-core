# Split (non-negotiable)

| Layer | Where | Path |
|-------|--------|------|
| Ceremony, grants, this TUI, operator | **Mac** | `~/.grok/hard-allow` (keep). This repo: `/Users/c/dev/ha-live` |
| Loop that must not die, workers, bus, third-party egress | **AMS** `ssh ams` (root@51.15.18.106) | `/opt/ha-live` |

Mac sleeps. Third-party must not leave via Mac ISP.

Keep: HA grants, Mac SOCKS, `ha-orch-grok` / `ha-wire-v3` on Mac if already online.  
Build new: AMS process + `/opt/ha-live/bus` + Mac ctl that talks to AMS over `ssh ams` / rsync. No second HA ceremony on AMS; inherit token into `ha.env`.

## Two loopbacks (do not confuse)

| Who egresses | Proxy |
|--------------|--------|
| Mac TUI / local tools | `socks5h://127.0.0.1:10808` on **Mac** (`HA_PROXY`) |
| AMS remainder / AMS workers | SOCKS on **AMS** loopback. 10808 is **down**. Candidate: xray `127.0.0.1:18082` (protocol unconfirmed). Discover + probe before setting `HA_AMS_PROXY`. If none works: HOLD third-party egress in `proof/BLOCKER.md` — remainder still runs fail-closed. Do not tunnel third-party through the Mac ISP. |

`127.0.0.1:10808` on AMS is **not** the Mac Clash/V2Ray. Preflight checks both.

Optional: `HA_AMS_PROXY=direct` — AMS native egress (target sees `51.15.18.106`). OPSEC-ok vs Mac ISP; burns the VPS IP. Only after `scripts/ams-direct-probe.sh` GO.

## SSH

`Host ams` in `~/.ssh/config` → `root@51.15.18.106`, `IdentityFile ~/.ssh/id_ed25519`. Fallback: `ams-alt` port 48222 / persist key. BatchMode only.
