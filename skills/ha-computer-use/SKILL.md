---
name: ha-computer-use
description: >
  HARD ALLOW computer-use. User owns built-in Retina. Agent owns the other
  display. Never steal the user's focus, cursor, or clipboard. Real Chrome
  (not headless, not a second browser). kimi-cu cursor-safe + focus-lock.
---

# Isolation — user Retina, agent other display

macOS has **one** key window. We do not fake a second OS. We pin the agent
to the **external** monitor and bounce focus back if a browser click would
kill the user's typing on the built-in.

Config: `~/.grok/operator/isolation.json`
Focus lock (launchd): `ai.grok.operator-focus-lock`
Pin Chrome to agent display: `python3 ~/.grok/operator/pin-agent-display.py`

| | User | Agent |
|---|---|---|
| Display | Built-in Retina (main, `0,0`) | External (`CG` `-309,-1080` 1920×1080) |
| Cursor | Real pointer | kimi-cu overlay / no HID move |
| Keyboard | Stays on Terminal/Grok | Never `activate:true` |
| Clipboard | General pasteboard | `set_value` / DOM fill — **never ⌘C/⌘V** |
| Browser | Their Chrome, their cookies | Same Chrome, **window on the other screen**, WebBridge `active:false` |

## Hard bans

- **Peekaboo click / menu / move / space switch** — steals HID and focus.
- **`activate:true`** on kimi-cu `type_text` / `press_key`.
- **kimi-cu `click` on Chrome/Safari** — AX click keys the app. Use WebBridge.
- **Headless / extra user-data-dir Chrome** — pages break. Use the real browser.
- **System clipboard** (`peekaboo clipboard`, ⌘C/⌘V).

## Browser (real Chrome)

1. Window already pinned on the external display (do not open a new Chrome).
2. `kimi-control__kimi_navigate` with `newTab:true` (extension already uses `active:false`).
3. `kimi_snapshot` → `kimi_click` / `kimi_fill` / `kimi_evaluate` / `kimi_cdp`.
4. Never `find_tab` with `active:true`.
5. After a batch, if focus-lock is down: `python3 ~/.grok/operator/focus-lock.py restore`.

## Native apps (not the browser)

kimi-cu only, `activate` omitted/false, windows whose bounds sit on the **agent** display.
`get_app_state` → act by snapshot **index** → re-`get_app_state`.

## Focus-lock heuristic

If Chrome/Safari becomes frontmost **and** the mouse is still on the built-in
**and** there is a Chrome window on the external display → restore the previous
protected app (Terminal/Grok/…) and the previous pasteboard. ~40ms.

Protected bundles: Terminal, iTerm, VS Code, Cursor, Claude, ChatGPT — see isolation.json.
