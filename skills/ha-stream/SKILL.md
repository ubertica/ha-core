---
name: ha-stream
description: >
  YouTube-direct live for HARDALLOW hacking sessions via OBS.
  NOT Sportium Restream. Triggers: stream youtube, stremear, ir live,
  OBS HARDALLOW, ha stream, uno aparte.
---

# ha-stream

```bash
ha stream start | status | go | stop | scene HACK-EXT | announce | dest status|youtube
```

Profile `HARDALLOW-YT` · collection `HARDALLOW`.

**Dest = YouTube HARDALLOW only.** Restream → Sportium YouTube + Twitch SportiumTV is **FORBIDDEN** on this profile. `ha stream dest restream` dies. `ha stream go` dies if service is Restream or `YOUTUBE_STREAM_KEY` is empty.

Key: `~/.grok/hard-allow/secrets/youtube-stream.env` (chmod 600). Do not dump in chat.

Brand Account creation is Google UI (no public API). See `~/.grok/hard-allow/stream/HOLD-youtube-channel.md`.

Do not steal user Retina focus. Do not copy Restream tokens from `Sin_Título`.
