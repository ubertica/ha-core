# CONTRACT — ha-pp-consensus

- Read `~/.grok/agents/_ha-law.md` first.
- Use disk bus `~/.grok/pumapay-bus/consensus/` only for proposals/decisions.
- pp-docs and ppd-arch are the two voting peers. Conductor orchestrates only.
- Never solo decide scope/wave/ADR.
- Selftest must PASS.
- Output: decisions/*.json + append to consensus.jsonl + board events.
- No nested grok -p.
- Evidence on disk; no invented ACK.
