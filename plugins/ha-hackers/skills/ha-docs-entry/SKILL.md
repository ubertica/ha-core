---
name: ha-docs-entry
description: >
  Dispatch the OpenAPI-as-entry specialist pair (hack-entry + hack-webhook)
  against a live /docs or swagger URL via the autonomous workflow.
  Use when the operator says study /docs, OpenAPI unauth, swagger public,
  docs-entry, unsigned webhook, /docs-entry, or wants an entry vector from
  an unauthenticated OpenAPI spec instead of the full 5-lane ha-hackers recon.
---

# ha-docs-entry

Canonical agents: `hack-entry`, `hack-webhook`, `hack-verify`  
Contract: `references/CONTRACT.md` · Methodology: `references/METHODOLOGY.md`  
Workflow: `~/.grok/workflows/docs-entry.rhai`  
Conductor: `~/.grok/skills/ha-hackers/references/AUTONOMY.md`

Do **not** spawn lanes by hand. Do **not** nested `grok -p`.

## Dispatch

```
python3 ~/.grok/skills/ha-hackers/scripts/dispatch.py plan \
  --target TARGET --out OUT --pack docs-entry \
  --proxy socks5h://127.0.0.1:10808
workflow name=ha-auto args={target, out, pack: "docs-entry", proxy, token_file?}
```

The workflow: preflight → skip READY → entry∥webhook remainder → **disk** `verify_evidence.py` → exploit+lead **only if** `go_count > 0`. Namespaced flags: `READY.docs-exploit` / `READY.docs-lead`.

JWT is optional (unauth pack). Proxy is required unless the operator said `--allow-direct`.

## Finding format

See CONTRACT.md. Evidence on disk or it is not a finding. Prober `confirmed_count` is untrusted.
