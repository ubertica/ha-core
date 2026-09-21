---
name: ha-auto
description: Autonomous hacker-team conductor. Plan → matching workflow → disk gate.
---

Follow `~/.grok/skills/ha-auto/SKILL.md` and `~/.grok/skills/ha-hackers/references/AUTONOMY.md`.

```
bash ~/.grok/skills/ha-hackers/scripts/ctl.sh auto --target TARGET --out OUT --pack auto
```

Then `workflow name=ha-auto` with those args. Skip READY. Exploit only if disk `go_count>0`. No hand-picked lanes. No nested grok -p.
