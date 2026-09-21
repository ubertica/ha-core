# AUTONOMY — ha-aml

## Default (conductor)

1. Parse brief → write `BUILD-SPEC.md` into target plugin dir.
2. Run workflow `ha-aml` **or** `ctl.sh forge --spec ...`
3. Do not hand-spawn lane authors unless workflow down.
4. Verify: `ctl.sh selftest --name <NAME>`
5. Report paths + selftest.

## ctl.sh

```
bash ~/.grok/skills/ha-aml/scripts/ctl.sh forge \
  --name ha-aml --prefix aml --mode team \
  --purpose "..." --lanes lanes.json

bash ~/.grok/skills/ha-aml/scripts/ctl.sh selftest --name ha-aml
bash ~/.grok/skills/ha-aml/scripts/ctl.sh from-hackers   # dump checklist from gold
```

## Workflow phases

1. **Spec** — normalize brief → BUILD-SPEC + references drafts
2. **Scaffold** — dirs, plugin.json, _ha-law, scripts from templates
3. **Agents∥Skills** — emit all agent md + SKILL + commands (parallel ok)
4. **Workflows** — write `.rhai` (+ tick)
5. **Sync** — copy agents/skills to `~/.grok/{agents,skills}`
6. **Verify** — selftest; FAIL ⇒ fix loop once then HOLD

## Banned

Nested `grok -p`. Claiming DONE without selftest. Diverging from ha-hackers interconnect (disk bus + workflow conductor).
